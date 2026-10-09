# davidcreason.com

Personal site for David Creason. Plain static HTML/CSS/JS, hosted free on GitHub Pages.

## Adding or updating a project

All content lives in `build.py`: the `PROJECTS` list (title, status `active`/`past`, summary, tags, image, links),
`PROFILE`, and `EDUCATION`. Edit it, then run:

```bash
python3 build.py
git add -A && git commit -m "Update projects" && git push
```

Project images go in `assets/projects/` (800x500 works well). Each project gets a detail page at `/projects/<slug>/`;
write its body in the `detail_page(...)` calls near the bottom of `build.py`.

```
index.html                     Home: hero, active + past projects, AI assistant, contact CTA
projects/                      Project index and one page per project
contact/index.html             Contact, resume, LinkedIn
home/, data-viz/...            Redirects from old URLs
404.html                       Not-found page
assets/                        style.css, chat.js, headshot, favicon, project images
build.py                       Generates all of the above
CNAME                          Custom domain for GitHub Pages
```

URLs match the old Google Sites paths, so existing links keep working.

## Publish

1. Create a **public** repo on GitHub (e.g. `davidcreason.com`) and push these files to `main`:
   ```bash
   git init && git add . && git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/<you>/davidcreason.com.git
   git push -u origin main
   ```
2. Repo **Settings → Pages**: Source = *Deploy from a branch*, Branch = `main`, folder `/ (root)`.
   Custom domain should already read `www.davidcreason.com` (from the `CNAME` file).
3. **Verify the domain**: GitHub profile **Settings → Pages → Add a domain** → `davidcreason.com`, then add the TXT record it gives you at your registrar.
4. **Remove the domain from Google Sites first** (Google Sites → Settings → Custom domains), then at your registrar:
   - Delete the old `www` CNAME that points to `ghs.googlehosted.com`.
   - `www`  CNAME → `<you>.github.io`
   - `@` (apex) A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Optional `@` AAAA → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
5. Once the DNS check passes in Pages settings (minutes to a few hours), tick **Enforce HTTPS**.

## Chatbot (important)

`assets/chat.js` calls `https://resume-bot-ae99.vercel.app/api/chat`. On Google Sites the widget ran on a
`googleusercontent.com` origin; now it runs on `www.davidcreason.com`. If the Vercel function restricts CORS,
add these to its allowed origins (the `Access-Control-Allow-Origin` header and the `OPTIONS` preflight response):

- `https://www.davidcreason.com`
- `https://davidcreason.com`

Checked 2026-10-09: a request from `https://www.davidcreason.com` passed CORS, so it should work as-is.
If the bare `davidcreason.com` ever serves the page directly, confirm that origin too.

## Editing

Edit the HTML directly and push; Pages redeploys in about a minute. Shared header/footer are repeated in each page,
so a nav change touches every `index.html`.
