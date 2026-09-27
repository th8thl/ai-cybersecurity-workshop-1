import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .ai_client import AIClientError, get_chat_client, model_prompt
from .models import ChatMessage
from .prompt_security import defended_response_for, redact_sensitive_output


PROVIDER_OPTIONS = ["mock", "gemini", "qwen"]


def _selected_provider(value):
    provider = (value or settings.AI_PROVIDER or "mock").lower()
    if provider not in PROVIDER_OPTIONS:
        return "mock"
    return provider


def _history(request):
    history = request.session.setdefault("chat_history", [])
    cleaned_history = [
        item
        for item in history
        if not (
            item.get("role") == "assistant"
            and item.get("content", "").startswith("Gemini request failed for model")
        )
    ]
    request.session["chat_history"] = cleaned_history
    if len(cleaned_history) != len(history):
        request.session.modified = True
    return cleaned_history


def _session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key or ""


def _store_message(request, role, content, provider="", model=""):
    ChatMessage.objects.create(
        session_key=_session_key(request),
        role=role,
        content=content,
        provider=provider or "",
        model=model or "",
    )


def index(request):
    history = _history(request)
    blocked = False
    provider = None
    model = None
    error = None
    selected_provider = _selected_provider(request.POST.get("provider"))
    try:
        active_client = get_chat_client(selected_provider)
    except AIClientError:
        active_client = get_chat_client("mock")

    if request.method == "POST":
        message = request.POST.get("message", "").strip()
        if message:
            prior_history = history[-3:]
            history.append({"role": "user", "content": message})
            _store_message(request, "user", message)
            defended_text = defended_response_for(message)
            if defended_text:
                reply = defended_text
                provider = "input-guardrail"
                blocked = True
            else:
                try:
                    result = active_client.complete(message, prior_history)
                    provider = result.provider
                    model = result.model
                    reply = redact_sensitive_output(result.text, settings.SYNTHETIC_SECRET)
                except AIClientError as exc:
                    provider = active_client.provider
                    error = str(exc)
                    reply = error
            if error is None:
                history.append({"role": "assistant", "content": reply})
                _store_message(request, "assistant", reply, provider, model)
            request.session.modified = True

    return render(
        request,
        "chatbot/index.html",
        {
            "history": history,
            "blocked": blocked,
            "provider": provider,
            "model": model,
            "error": error,
            "configured_provider": active_client.provider,
            "selected_provider": selected_provider,
            "provider_options": PROVIDER_OPTIONS,
            "gemini_key_loaded": bool(settings.GEMINI_API_KEY),
            "synthetic_secret": settings.SYNTHETIC_SECRET,
            "theme": settings.CHATBOT_THEME,
            "app_status_label": "Reference solution",
        },
    )


@require_POST
def prompt_preview(request):
    history = _history(request)
    payload = json.loads(request.body or "{}")
    message = payload.get("message", "").strip()
    selected_provider = _selected_provider(payload.get("provider"))

    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)

    defended_text = defended_response_for(message)
    if defended_text:
        prompt = "Input guardrail would block this message before a model prompt is rendered or sent."
        blocked = True
    else:
        prior_history = history[-3:]
        prompt = model_prompt(message, prior_history)
        blocked = False

    return JsonResponse(
        {
            "prompt": prompt,
            "selected_provider": selected_provider,
            "blocked": blocked,
            "status": "prompt-preview",
        }
    )


@require_POST
def chat(request):
    history = _history(request)
    payload = json.loads(request.body or "{}")
    message = payload.get("message", "").strip()
    selected_provider = _selected_provider(payload.get("provider"))

    if not message:
        return JsonResponse({"error": "Message is required."}, status=400)

    prior_history = history[-3:]
    user_item = {"role": "user", "content": message}
    history.append(user_item)
    _store_message(request, "user", message)

    blocked = False
    error = None
    provider = None
    model = None
    attempts = []
    prompt = None
    try:
        active_client = get_chat_client(selected_provider)
    except AIClientError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    defended_text = defended_response_for(message)
    if defended_text:
        reply = defended_text
        provider = "input-guardrail"
        blocked = True
        prompt = "Input guardrail blocked this message before a model prompt was rendered or sent."
    else:
        try:
            result = active_client.complete(message, prior_history)
            provider = result.provider
            model = result.model
            attempts = result.attempts or []
            prompt = result.prompt
            reply = redact_sensitive_output(result.text, settings.SYNTHETIC_SECRET)
        except AIClientError as exc:
            provider = active_client.provider
            error = str(exc)
            reply = error

    assistant_item = {"role": "assistant", "content": reply}
    if error is None:
        history.append(assistant_item)
        _store_message(request, "assistant", reply, provider, model)
    request.session.modified = True

    return JsonResponse(
        {
            "user": user_item,
            "assistant": assistant_item,
            "blocked": blocked,
            "error": error,
            "provider": provider,
            "model": model,
            "attempts": attempts,
            "prompt": prompt,
            "configured_provider": active_client.provider,
            "selected_provider": selected_provider,
            "provider_options": PROVIDER_OPTIONS,
            "gemini_key_loaded": bool(settings.GEMINI_API_KEY),
        }
    )


@require_POST
def reset_chat(request):
    ChatMessage.objects.filter(session_key=_session_key(request)).delete()
    request.session["chat_history"] = []
    request.session.modified = True
    return redirect("index")





