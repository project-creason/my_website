// POST /api/send-scope — emails a ScopeOut scope summary.
// Protections: origin check, Cloudflare Turnstile, honeypot, one recipient, size and length limits,
// per-visitor rate limit, and the email is rendered here from plain data (no visitor-supplied HTML).
const { render } = require("../lib/email-template.js");

const ORIGINS = (process.env.ALLOWED_ORIGINS || "https://www.davidcreason.com,https://davidcreason.com").split(",").map(s => s.trim());
const LOGO_URL = process.env.LOGO_URL || "https://www.davidcreason.com/scopeout/scopeout-logo-email.png";
const PAGE_URL = "https://www.davidcreason.com/scopeout/";
const LINK_RE = /https?:|www\.|:\/\/|\b[a-z0-9-]+\.(com|net|org|io|co|ru|xyz|info|biz|ly|link|app|site|top)\b/i;
const strings = v => typeof v === "string" ? [v] : Array.isArray(v) ? v.flatMap(strings) : v && typeof v === "object" ? Object.values(v).flatMap(strings) : [];
const EMAIL_RE = /^[^\s@<>()\[\],;:"]{1,64}@[A-Za-z0-9.-]{1,190}\.[A-Za-z]{2,24}$/;

// Best-effort rate limit (per warm instance): 4 sends per visitor per hour, 40 per instance per day.
const hits = new Map(); let day = { start: Date.now(), count: 0 };
function limited(ip) {
  const now = Date.now();
  if (now - day.start > 864e5) day = { start: now, count: 0 };
  if (day.count >= 40) return true;
  const recent = (hits.get(ip) || []).filter(t => now - t < 36e5);
  if (recent.length >= 4) { hits.set(ip, recent); return true; }
  recent.push(now); hits.set(ip, recent); day.count++; return false;
}

async function verifyTurnstile(token, ip) {
  const body = new URLSearchParams({ secret: process.env.TURNSTILE_SECRET_KEY, response: token || "" });
  if (ip) body.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  const j = await r.json().catch(() => ({}));
  return !!j.success;
}

async function sendMail(msg) {
  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(msg)
  });
  if (!r.ok) throw new Error(`Resend ${r.status}: ${(await r.text()).slice(0, 300)}`);
}

module.exports = async (req, res) => {
  const origin = req.headers.origin || "";
  if (ORIGINS.includes(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  }
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ ok: false, error: "Use POST." });
  if (!ORIGINS.includes(origin)) return res.status(403).json({ ok: false, error: "This form only works from davidcreason.com." });
  const missing = ["RESEND_API_KEY", "TURNSTILE_SECRET_KEY", "MAIL_FROM", "SALES_NOTIFY_TO"].filter(k => !process.env[k]);
  if (missing.length) { console.error("Missing env:", missing.join(", ")); return res.status(503).json({ ok: false, error: "Email isn't set up yet." }); }

  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch { b = null; } }
  if (!b || typeof b !== "object" || JSON.stringify(b).length > 20000) return res.status(400).json({ ok: false, error: "That request couldn't be read." });

  // Honeypot: people never see this field, bots fill it. Pretend success.
  if (b.website) return res.status(200).json({ ok: true });

  const to = String(b.to || "").trim();
  if (!EMAIL_RE.test(to) || to.length > 254) return res.status(400).json({ ok: false, error: "Enter a valid email address." });
  if (b.mode !== "seller" && !b.consent) return res.status(400).json({ ok: false, error: "Tick the box to agree to the follow-up." });
  // Rep emails carry free text, so in this public demo they only go to approved inboxes.
  if (b.mode === "seller") {
    const allow = (process.env.SELLER_TO_ALLOWLIST || process.env.SALES_NOTIFY_TO).split(",").map(s => s.trim().toLowerCase());
    if (!allow.includes(to.toLowerCase())) return res.status(403).json({ ok: false, error: "In this demo, rep emails only go to approved inboxes." });
  }
  // No links anywhere: names, companies, notes and scope text are plain text only.
  if ([b.name, b.scope].flatMap(strings).some(s => LINK_RE.test(s))) return res.status(400).json({ ok: false, error: "Remove links or web addresses and try again." });

  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return res.status(429).json({ ok: false, error: "Too many emails from here. Try again in an hour." });
  if (!(await verifyTurnstile(b.token, ip))) return res.status(400).json({ ok: false, error: "The human check didn't pass. Refresh the page and try again." });

  const data = { ...(b.scope || {}), mode: b.mode === "seller" ? "seller" : "buyer", recipientName: b.name, pageUrl: PAGE_URL };
  const mail = render(data, { logoUrl: LOGO_URL });
  try {
    await sendMail({ from: process.env.MAIL_FROM, to: [to], reply_to: process.env.SALES_NOTIFY_TO, subject: mail.subject, html: mail.html, text: mail.text });
    const d = mail.data;
    await sendMail({
      from: process.env.MAIL_FROM, to: [process.env.SALES_NOTIFY_TO], reply_to: to,
      subject: `${d.mode === "seller" ? "Scope sent" : "New scope request"}: ${d.company || d.recipientName || to} (${d.product} ${d.plan})`,
      text: [`${d.mode === "seller" ? "A rep sent this scope to" : "A visitor asked for this scope"}: ${d.recipientName || "(no name)"} <${to}>`,
        d.wantsCall ? "They also asked for a call." : "", "", mail.text].filter(x => x !== null).join("\n")
    });
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error(e);
    return res.status(502).json({ ok: false, error: "The email service didn't accept the message. Try again shortly." });
  }
};
