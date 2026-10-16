/* ScopeOut scope email. One template, used by the page (preview) and by the mail server (real send).
   It takes plain data, never HTML, so nothing a visitor types can change the email's markup. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.ScopeOutEmail = factory();
})(typeof self !== "undefined" ? self : this, function () {
  const C = { bg: "#F4F6FA", card: "#FFFFFF", ink: "#141B2D", muted: "#566079", line: "#DCE2EC", accent: "#1E4ECF", soft: "#E6ECFB", prod: "#0E9AA7", warnBg: "#FBEEDA", warn: "#8A4B00" };
  const FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";
  const esc = v => String(v == null ? "" : v).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const str = (v, max) => String(v == null ? "" : v).replace(/<[^>]*>/g, "").replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "").trim().slice(0, max);
  const list = (v, max) => (Array.isArray(v) ? v : []).slice(0, max);

  /* Coerce untrusted input into the shape the template expects, with hard length limits. */
  function clean(d) {
    d = d && typeof d === "object" ? d : {};
    return {
      mode: d.mode === "seller" ? "seller" : "buyer",
      brand: d.brand && typeof d.brand === "object" ? { name: str(d.brand.name, 40), accent: /^#[0-9a-f]{6}$/i.test(d.brand.accent || "") ? d.brand.accent : "", soft: /^#[0-9a-f]{6}$/i.test(d.brand.soft || "") ? d.brand.soft : "" } : null,
      recipientName: str(d.recipientName, 80),
      company: str(d.company, 100),
      product: str(d.product, 60) || "your",
      plan: str(d.plan, 40),
      stats: list(d.stats, 3).map(s => ({ label: str(s && s.label, 30), value: str(s && s.value, 24), sub: str(s && s.sub, 60) })).filter(s => s.label && s.value),
      highlights: list(d.highlights, 6).map(h => ({ label: str(h && h.label, 30), text: str(h && h.text, 240) })).filter(h => h.label && h.text),
      lines: list(d.lines, 20).map(l => ({ name: str(l && l.name, 60), detail: str(l && l.detail, 160), qty: str(l && l.qty, 16), added: !!(l && l.added) })).filter(l => l.name),
      reasons: list(d.reasons, 8).map(r => str(r, 160)).filter(Boolean),
      investment: str(d.investment, 80),
      investmentNote: str(d.investmentNote, 200),
      notes: list(d.notes, 5).map(n => ({ tag: str(n && n.tag, 24), msg: str(n && n.msg, 240) })).filter(n => n.msg),
      note: str(d.note, 600),
      wantsCall: !!d.wantsCall,
      demoFooter: str(d.demoFooter, 300),
      pageUrl: str(d.pageUrl, 200)
    };
  }

  function render(input, opts) {
    const d = clean(input), o = opts || {};
    const B = d.brand && d.brand.name ? d.brand : null, A = (B && B.accent) || C.accent, S = (B && B.soft) || C.soft;
    const first = d.recipientName.split(/\s+/)[0];
    const subject = d.mode === "seller"
      ? `${d.company || "Your"} ${d.product} scope${d.plan ? `: ${d.plan} plan` : ""}`
      : `Your ${d.product} scope${d.plan ? `: ${d.plan} plan` : ""}`;
    const intro = d.mode === "seller"
      ? (d.note || `As promised, here's the scope we put together${d.company ? ` for ${d.company}` : ""}. Reply with any questions and I'll walk you through it.`)
      : `Here's the scope you built${d.company ? ` for ${d.company}` : ""}. A solutions engineer will review it and follow up within one business day${d.wantsCall ? " to set up your call" : ""}.`;

    const h2 = t => `<tr><td style="padding:24px 32px 8px;font:600 12px ${FONT};letter-spacing:.08em;text-transform:uppercase;color:${C.muted}">${esc(t)}</td></tr>`;
    const stats = d.stats.length ? `<tr><td style="padding:8px 32px 4px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse"><tr>${d.stats.map(s =>
      `<td valign="top" style="padding:14px 12px 14px 0;border-top:2px solid ${A};width:${Math.floor(100 / d.stats.length)}%">
        <div style="font:600 11px ${FONT};letter-spacing:.08em;text-transform:uppercase;color:${C.muted}">${esc(s.label)}</div>
        <div style="font:700 26px/1.15 ${FONT};color:${C.ink};margin-top:4px">${esc(s.value)}</div>
        ${s.sub ? `<div style="font:13px ${FONT};color:${C.muted};margin-top:2px">${esc(s.sub)}</div>` : ""}</td>`).join("")}</tr></table></td></tr>` : "";
    const highlights = d.highlights.length ? h2("At a glance") + `<tr><td style="padding:0 32px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse">${d.highlights.map(x =>
      `<tr><td valign="top" style="padding:9px 12px 9px 0;border-top:1px solid ${C.line};font:600 13px ${FONT};color:${C.muted};width:130px">${esc(x.label)}</td><td style="padding:9px 0;border-top:1px solid ${C.line};font:15px/1.45 ${FONT};color:${C.ink}">${esc(x.text)}</td></tr>`).join("")}</table></td></tr>` : "";
    const lines = d.lines.length ? h2("What's included") + `<tr><td style="padding:0 32px"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse">${d.lines.map(l =>
      `<tr><td valign="top" style="padding:9px 12px 9px 0;border-top:1px solid ${C.line};font:600 15px ${FONT};color:${C.ink}">${esc(l.name)}${l.added ? ` <span style="display:inline-block;font:600 11px ${FONT};color:${A};background:${S};border-radius:999px;padding:2px 8px;margin-left:4px;vertical-align:2px">Recommended</span>` : ""}<div style="font:400 13px/1.4 ${FONT};color:${C.muted};margin-top:2px">${esc(l.detail)}</div></td><td valign="top" align="right" style="padding:9px 0;border-top:1px solid ${C.line};font:15px ${FONT};color:${C.ink};white-space:nowrap">${esc(l.qty)}</td></tr>`).join("")}</table></td></tr>` : "";
    const reasons = d.reasons.length ? h2(`Why ${d.plan || "this plan"}`) + `<tr><td style="padding:0 32px"><ul style="margin:0;padding-left:20px;font:15px/1.55 ${FONT};color:${C.ink}">${d.reasons.map(r => `<li style="margin:2px 0">${esc(r)}</li>`).join("")}</ul></td></tr>` : "";
    const invest = d.investment ? h2("Investment") + `<tr><td style="padding:0 32px"><div style="font:700 22px ${FONT};color:${C.ink}">${esc(d.investment)}</div>${d.investmentNote ? `<div style="font:13px/1.45 ${FONT};color:${C.muted};margin-top:4px">${esc(d.investmentNote)}</div>` : ""}</td></tr>` : "";
    const notes = d.notes.length ? h2("Worth knowing") + `<tr><td style="padding:0 32px">${d.notes.map(n =>
      `<div style="background:${S};border-radius:6px;padding:10px 12px;margin:0 0 6px;font:14px/1.45 ${FONT};color:${C.ink}">${n.tag ? `<strong style="color:${A}">${esc(n.tag)}:</strong> ` : ""}${esc(n.msg)}</div>`).join("")}</td></tr>` : "";
    const logo = B
      ? `<span style="font:700 24px ${FONT};color:${A}">${esc(B.name)}</span>`
      : o.logoUrl
      ? `<img src="${esc(o.logoUrl)}" width="150" height="34" alt="ScopeOut" style="display:block;border:0;outline:none;height:auto;width:150px">`
      : `<span style="font:700 22px ${FONT};color:${C.ink}">Scope<span style="color:${C.accent}">Out</span></span>`;

    const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>${esc(subject)}</title></head>
<body style="margin:0;padding:0;background:${C.bg}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">${esc(d.plan ? `${d.plan} plan, ready for your review.` : "Your scope is ready.")}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.bg};border-collapse:collapse"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:${C.card};border:1px solid ${C.line};border-radius:10px;border-collapse:separate">
<tr><td style="padding:24px 32px 18px;border-bottom:1px solid ${C.line}"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td>${logo}</td><td align="right" style="font:13px ${FONT};color:${C.muted}">Scope summary</td></tr></table></td></tr>
<tr><td style="padding:28px 32px 4px;font:700 26px/1.2 ${FONT};color:${C.ink}">Your ${esc(d.product)} scope${d.plan ? `: <span style="color:${A}">${esc(d.plan)}</span>` : ""}</td></tr>
<tr><td style="padding:10px 32px 4px;font:15px/1.55 ${FONT};color:${C.ink}">${first ? `Hi ${esc(first)},<br><br>` : ""}${esc(intro).replace(/\n/g, "<br>")}</td></tr>
${stats}${highlights}${lines}${reasons}${invest}${notes}
<tr><td style="padding:26px 32px 28px"><div style="background:${C.bg};border-radius:8px;padding:14px 16px;font:15px/1.5 ${FONT};color:${C.ink}"><strong>Questions?</strong> Just reply to this email and it goes straight to your solutions engineer.</div></td></tr>
</table>
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px"><tr><td style="padding:16px 32px;font:12px/1.5 ${FONT};color:${C.muted}" align="center">
${B ? "Powered by" : "Sent with"} <strong style="color:${C.ink}">Scope<span style="color:${C.accent}">Out</span></strong> · Scope it right the first time.<br>${esc(d.demoFooter)}${d.mode === "buyer" && d.pageUrl ? `<br>You asked for this summary at ${esc(d.pageUrl.replace(/^https?:\/\//, ""))}.` : ""}
</td></tr></table>
</td></tr></table></body></html>`;

    const t = [];
    t.push(`Your ${d.product} scope${d.plan ? `: ${d.plan}` : ""}`, "");
    if (first) t.push(`Hi ${first},`, "");
    t.push(intro, "");
    d.stats.forEach(s => t.push(`${s.label}: ${s.value}${s.sub ? ` (${s.sub})` : ""}`));
    if (d.highlights.length) { t.push("", "AT A GLANCE"); d.highlights.forEach(x => t.push(`- ${x.label}: ${x.text}`)); }
    if (d.lines.length) { t.push("", "WHAT'S INCLUDED"); d.lines.forEach(l => t.push(`- ${l.name}${l.added ? " [recommended]" : ""}: ${l.detail} (${l.qty})`)); }
    if (d.reasons.length) { t.push("", `WHY ${(d.plan || "this plan").toUpperCase()}`); d.reasons.forEach(r => t.push(`- ${r}`)); }
    if (d.investment) { t.push("", "INVESTMENT", d.investment + (d.investmentNote ? ` (${d.investmentNote})` : "")); }
    if (d.notes.length) { t.push("", "WORTH KNOWING"); d.notes.forEach(n => t.push(`- ${n.tag ? n.tag + ": " : ""}${n.msg}`)); }
    t.push("", "Questions? Just reply to this email.", "", "Sent with ScopeOut. Scope it right the first time.", d.demoFooter);
    return { subject, html, text: t.join("\n"), data: d };
  }
  return { render, clean };
});
