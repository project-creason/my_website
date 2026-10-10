// Resume chatbot — talks to the existing Vercel endpoint.
// NOTE: the Vercel API must allow CORS from https://www.davidcreason.com
// (and https://davidcreason.com). See README.md.
(function () {
  const API_URL = "https://resume-bot-ae99.vercel.app/api/chat";
  const history = [];
  const box = document.getElementById("chat-box");
  const input = document.getElementById("user-input");
  const send = document.getElementById("send-btn");
  if (!box || !input || !send) return;

  // Minimal, safe markdown: escape everything, then allow **bold**, *italic*,
  // [text](https://link) and "- " / "* " bullets. Nothing else becomes HTML.
  function renderMarkdown(text) {
    const esc = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    return esc
      .replace(/^\s*[-*] /gm, "• ")
      .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
      .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>");
  }

  function addMsg(cls, text) {
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.textContent = text; // textContent, never innerHTML, so user input can't inject HTML
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
    return div;
  }

  async function sendMessage(textOverride) {
    const text = (textOverride ?? input.value).trim();
    if (!text) return;
    input.value = "";
    addMsg("user", text);
    history.push({ role: "user", content: text });

    const bot = document.createElement("div");
    bot.className = "msg bot typing";
    bot.innerHTML = "<span></span><span></span><span></span>";
    box.appendChild(bot);
    box.scrollTop = box.scrollHeight;
    send.disabled = true;

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: history }),
      });
      if (!res.ok) {
        // The server sends a short, visitor-friendly explanation (rate limit, empty question, etc.)
        const msg = (await res.text().catch(() => "")).slice(0, 300);
        bot.className = "msg bot";
        bot.textContent = msg || "Error connecting to the AI assistant. Please try again.";
        history.pop();
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let full = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (!full) { bot.className = "msg bot"; bot.textContent = ""; }
        full += decoder.decode(value, { stream: true });
        bot.innerHTML = renderMarkdown(full);
        box.scrollTop = box.scrollHeight;
      }
      history.push({ role: "assistant", content: full });
    } catch (err) {
      console.error(err);
      bot.className = "msg bot";
      bot.textContent = "Error connecting to the AI assistant. Please try again.";
    } finally {
      send.disabled = false;
    }
  }

  send.addEventListener("click", () => sendMessage());
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") sendMessage(); });
  document.querySelectorAll(".chip").forEach((chip) =>
    chip.addEventListener("click", () => sendMessage(chip.dataset.q))
  );
})();

// Draw attention to the assistant when someone arrives via "Try it" / "Ask my AI assistant".
(function () {
  const target = document.getElementById("ask");
  const chat = document.getElementById("chat-container");
  if (!target || !chat) return;

  function flash() {
    chat.classList.remove("flash");
    void chat.offsetWidth; // restart the animation if it's already run
    chat.classList.add("flash");
  }
  chat.addEventListener("animationend", () => chat.classList.remove("flash"));

  // Arrived from another page (e.g. /projects/ -> /#ask)
  if (location.hash === "#ask") setTimeout(flash, 450);

  // Same-page links: smooth scroll, then flash once it's in view
  document.querySelectorAll('a[href="#ask"], a[href="/#ask"]').forEach((a) =>
    a.addEventListener("click", (ev) => {
      ev.preventDefault();
      history.replaceState(null, "", "#ask");
      const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
      target.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
      setTimeout(flash, reduce ? 0 : 550);
    })
  );
})();
