// Contact form: posts to the resume-bot Vercel project, which emails David via Gmail.
(function () {
  const ENDPOINT = "https://resume-bot-ae99.vercel.app/api/contact";
  const form = document.getElementById("form");
  if (!form) return;
  const status = form.querySelector(".form-status");
  const button = form.querySelector('button[type="submit"]');
  const started = Date.now();

  function show(msg, kind) {
    status.textContent = msg;
    status.className = "form-status " + (kind || "");
  }

  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    data.elapsed = Date.now() - started;

    if (!data.name.trim() || !form.email.checkValidity() || !data.email.trim() || data.message.trim().length < 10) {
      show("Please add your name, a valid email, and a message of at least 10 characters.", "error");
      return;
    }
    // When Cloudflare Turnstile is on, its widget adds a hidden "cf-turnstile-response" field to the form.
    if (form.querySelector(".cf-turnstile") && !data["cf-turnstile-response"]) {
      show("Please complete the quick verification above the Send button.", "error");
      return;
    }

    button.disabled = true;
    show("Sending…");
    try {
      const res = await fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const body = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(body.error || "Something went wrong. Please try again.");
      form.reset();
      show("Thanks! Your message is on its way, and I'll get back to you soon.", "ok");
    } catch (err) {
      show(err.message || "Something went wrong. Please try again.", "error");
    } finally {
      button.disabled = false;
      // A Turnstile token works once; get a fresh one for any next attempt.
      if (window.turnstile && form.querySelector(".cf-turnstile")) window.turnstile.reset(form.querySelector(".cf-turnstile"));
    }
  });
})();
