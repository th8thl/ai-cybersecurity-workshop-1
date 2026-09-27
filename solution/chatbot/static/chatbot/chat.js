const chatLog = document.querySelector("#chat-log");
const chatForm = document.querySelector("#chat-form");
const messageInput = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const stopButton = document.querySelector("#stop-button");
const requestTimer = document.querySelector("#request-timer");
const notice = document.querySelector("#notice");
const configuredProvider = document.querySelector("#configured-provider");
const geminiKeyLoaded = document.querySelector("#gemini-key-loaded");
const providerSelect = document.querySelector("#provider-select");
const debugToggle = document.querySelector("#debug-toggle");
const debugPanel = document.querySelector("#debug-panel");
const debugOutput = document.querySelector("#debug-output");
const debugPrompt = document.querySelector("#debug-prompt");
const promptModal = document.querySelector("#prompt-modal");
const promptModalContent = document.querySelector("#prompt-modal-content");
const openPromptModal = document.querySelector("#open-prompt-modal");
const closePromptModal = document.querySelector("#close-prompt-modal");
let activeController = null;
let timerIntervalId = null;
let activeRequestStartedAt = 0;
let latestPrompt = "No prompt rendered yet.";

function getCookie(name) {
  const cookies = document.cookie ? document.cookie.split(";") : [];
  for (const cookie of cookies) {
    const [key, ...value] = cookie.trim().split("=");
    if (key === name) {
      return decodeURIComponent(value.join("="));
    }
  }
  return "";
}

function setWaiting(isWaiting) {
  messageInput.disabled = isWaiting;
  sendButton.disabled = isWaiting;
  stopButton.hidden = !isWaiting;
  requestTimer.hidden = !isWaiting;
  if (!isWaiting) {
    requestTimer.textContent = "0.0s";
  }
}

function clearEmptyState() {
  const emptyState = chatLog.querySelector(".empty-state");
  if (emptyState) {
    emptyState.remove();
  }
}

function escapeHtml(text) {
  return text
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderInlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

function renderMarkdown(markdown) {
  const blocks = [];
  const lines = markdown.split(/\r?\n/);
  let paragraph = [];
  let listItems = [];
  let codeLines = [];
  let inCodeBlock = false;

  function flushParagraph() {
    if (paragraph.length) {
      blocks.push(`<p>${renderInlineMarkdown(paragraph.join(" "))}</p>`);
      paragraph = [];
    }
  }

  function flushList() {
    if (listItems.length) {
      blocks.push(`<ul>${listItems.map((item) => `<li>${renderInlineMarkdown(item)}</li>`).join("")}</ul>`);
      listItems = [];
    }
  }

  function flushCodeBlock() {
    if (codeLines.length) {
      blocks.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
      codeLines = [];
    }
  }

  for (const line of lines) {
    if (line.trim().startsWith("```")) {
      if (inCodeBlock) {
        flushCodeBlock();
        inCodeBlock = false;
      } else {
        flushParagraph();
        flushList();
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      codeLines.push(line);
      continue;
    }

    if (!line.trim()) {
      flushParagraph();
      flushList();
      continue;
    }

    const listMatch = line.match(/^\s*[-*]\s+(.+)$/);
    if (listMatch) {
      flushParagraph();
      listItems.push(listMatch[1]);
      continue;
    }

    flushList();
    paragraph.push(line.trim());
  }

  flushParagraph();
  flushList();
  flushCodeBlock();
  return blocks.join("");
}

function appendMessage(role, content, extraClass = "") {
  clearEmptyState();
  const article = document.createElement("article");
  article.className = `message ${role} ${extraClass}`.trim();

  const label = document.createElement("span");
  label.textContent = role;

  const body = document.createElement("div");
  body.className = "message-body";
  if (role === "assistant") {
    body.innerHTML = renderMarkdown(content);
  } else {
    body.textContent = content;
  }

  article.append(label, body);
  chatLog.append(article);
  chatLog.scrollTop = chatLog.scrollHeight;
  return article;
}

function appendTypingIndicator() {
  clearEmptyState();
  const article = document.createElement("article");
  article.className = "message assistant typing-message";
  article.innerHTML = `
    <span>assistant</span>
    <div class="typing-bubble" aria-label="Assistant is responding">
      <span></span><span></span><span></span>
    </div>
  `;
  chatLog.append(article);
  chatLog.scrollTop = chatLog.scrollHeight;
  return article;
}

function formatElapsed(elapsedMs) {
  return `${(elapsedMs / 1000).toFixed(1)}s`;
}

function updateNotice(data) {
  notice.className = "notice";
  if (data.error) {
    notice.classList.add("error");
    notice.textContent = data.error;
  } else if (data.provider) {
    notice.textContent = `Response provider: ${data.provider}${data.model ? ` / ${data.model}` : ""}`;
  } else {
    notice.textContent = "";
  }
}

function updateDebug(data, elapsedMs) {
  configuredProvider.textContent = data.configured_provider ?? "unknown";
  geminiKeyLoaded.textContent = String(data.gemini_key_loaded);
  latestPrompt = data.prompt || latestPrompt || "No prompt rendered yet.";
  debugPrompt.textContent = latestPrompt;
  promptModalContent.textContent = latestPrompt;

  const summary = {
    elapsed_ms: Math.round(elapsedMs),
    status: data.status,
    selected_provider: data.selected_provider ?? providerSelect.value,
    provider: data.provider,
    model: data.model,
    blocked: data.blocked,
    error: data.error,
    attempts: data.attempts ?? [],
  };
  debugOutput.textContent = JSON.stringify(summary, null, 2);
}

async function updatePromptPreview(message, provider) {
  const response = await fetch(document.body.dataset.promptPreviewUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ message, provider }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Prompt preview failed.");
  }
  latestPrompt = data.prompt || "No prompt rendered yet.";
  debugPrompt.textContent = latestPrompt;
  promptModalContent.textContent = latestPrompt;
  updateDebug(
    {
      status: data.status || "prompt-preview",
      selected_provider: data.selected_provider ?? provider,
      provider: configuredProvider.textContent,
      gemini_key_loaded: geminiKeyLoaded.textContent,
      blocked: data.blocked,
      attempts: [],
      prompt: latestPrompt,
    },
    0
  );
}

function syncDebugVisibility() {
  document.body.classList.toggle("show-debug", debugToggle.checked);
  debugPanel.hidden = !debugToggle.checked;
}

document.querySelectorAll(".markdown-source").forEach((node) => {
  node.innerHTML = renderMarkdown(node.textContent);
  node.classList.remove("markdown-source");
});

debugToggle.addEventListener("change", syncDebugVisibility);

openPromptModal.addEventListener("click", () => {
  promptModalContent.textContent = latestPrompt;
  if (typeof promptModal.showModal === "function") {
    promptModal.showModal();
  }
});

closePromptModal.addEventListener("click", () => {
  promptModal.close();
});

promptModal.addEventListener("click", (event) => {
  if (event.target === promptModal) {
    promptModal.close();
  }
});

stopButton.addEventListener("click", () => {
  if (activeController) {
    activeController.abort();
  }
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = messageInput.value.trim();
  if (!message) {
    return;
  }
  appendMessage("user", message);
  messageInput.value = "";
  notice.textContent = "";
  setWaiting(true);
  const typingIndicator = appendTypingIndicator();
  const startedAt = performance.now();
  activeRequestStartedAt = startedAt;
  activeController = new AbortController();

  updateDebug(
    {
      status: "request-started",
      selected_provider: providerSelect.value,
      provider: configuredProvider.textContent,
      gemini_key_loaded: geminiKeyLoaded.textContent,
      attempts: [],
    },
    0
  );

  updatePromptPreview(message, providerSelect.value).catch((error) => {
    latestPrompt = `Prompt preview failed: ${error.message}`;
    debugPrompt.textContent = latestPrompt;
    promptModalContent.textContent = latestPrompt;
  });

  timerIntervalId = window.setInterval(() => {
    const elapsedMs = performance.now() - activeRequestStartedAt;
    requestTimer.textContent = formatElapsed(elapsedMs);
    updateDebug(
      {
        status: "request-in-flight",
        selected_provider: providerSelect.value,
        provider: configuredProvider.textContent,
        gemini_key_loaded: geminiKeyLoaded.textContent,
        attempts: [],
      },
      elapsedMs
    );
  }, 1000);

  try {
    const response = await fetch(document.body.dataset.chatUrl, {
      method: "POST",
      signal: activeController.signal,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ message, provider: providerSelect.value }),
    });
    const data = await response.json();
    typingIndicator.remove();

    if (!response.ok) {
      throw new Error(data.error || "Chat request failed.");
    }

    appendMessage("assistant", data.assistant.content, data.error ? "error-message" : "");
    updateNotice(data);
    updateDebug(data, performance.now() - startedAt);
  } catch (error) {
    const message =
      error.name === "AbortError"
        ? "Chat request stopped by the user. The provider call may still finish on the server, but this browser stopped waiting."
        : error.message;
    typingIndicator.remove();
    appendMessage("assistant", message, "error-message");
    notice.className = "notice error";
    notice.textContent = message;
    updateDebug({ status: "request-failed", error: message, selected_provider: providerSelect.value }, performance.now() - startedAt);
  } finally {
    window.clearInterval(timerIntervalId);
    timerIntervalId = null;
    activeController = null;
    setWaiting(false);
    messageInput.focus();
  }
});

syncDebugVisibility();

