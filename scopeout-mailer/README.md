# ScopeOut mailer

A single Vercel function that emails ScopeOut scope summaries for the demo at
`https://www.davidcreason.com/scopeout/`.

## Deploy

1. Vercel → Add New → Project → import `my_website` → **Root Directory: `scopeout-mailer`** → Deploy.
2. Settings → Environment Variables:

| Name | Value |
| --- | --- |
| `RESEND_API_KEY` | Resend API key with **Sending access** for `mail.davidcreason.com` |
| `TURNSTILE_SECRET_KEY` | Cloudflare Turnstile secret key |
| `MAIL_FROM` | `ScopeOut Demo <scopeout@mail.davidcreason.com>` |
| `SALES_NOTIFY_TO` | Where "new scope" notifications go (and where replies land) |
| `SELLER_TO_ALLOWLIST` | Optional. Comma-separated inboxes the rep form may send to. Defaults to `SALES_NOTIFY_TO` |
| `ALLOWED_ORIGINS` | Optional. Defaults to `https://www.davidcreason.com,https://davidcreason.com` |

3. Redeploy, then put the function URL (`https://<project>.vercel.app/api/send-scope`) and the Turnstile
   **site** key in `/scopeout/config.js`.

## What it guards against

- Requests from other websites (origin check)
- Bots (Cloudflare Turnstile and a hidden honeypot field)
- Bulk sending (one recipient per request, 4 per visitor per hour, 40 per day per instance, plus Resend's daily cap)
- Content injection (the email is built here from plain data; visitor text is length-limited, escaped, and may not contain links)
- Free-text misuse (the rep form, which has a note field, only sends to `SELLER_TO_ALLOWLIST`)

`lib/email-template.js` is the same template the page uses for its preview. Keep the two copies identical.
