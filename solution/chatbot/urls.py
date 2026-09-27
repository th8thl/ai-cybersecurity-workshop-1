from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("prompt-preview/", views.prompt_preview, name="prompt_preview"),
    path("chat/", views.chat, name="chat"),
    path("reset/", views.reset_chat, name="reset_chat"),
]
