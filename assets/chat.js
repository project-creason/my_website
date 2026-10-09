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
      if (!res.ok) throw new Error("HTTP " + res.status);

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let full = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (!full) { bot.className = "msg bot"; bot.textContent = ""; }
        full += decoder.decode(value, { stream: true });
        bot.textContent = full;
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
