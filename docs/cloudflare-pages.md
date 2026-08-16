# Deploying to Cloudflare Pages

This site is served by **Cloudflare Pages**, connected directly to the GitHub repo.
There is no build server to maintain: `index.html` is committed at the repo root and
served as-is.

## The pipeline

```
local machine  ──git push──▶  GitHub (bijoyr/portfolio-dashboard)  ──▶  Cloudflare Pages
                                                                         │
                              main branch ───────────────────────────▶  production
                                                                         www.trustfractals.com
                              any other branch / PR ─────────────────▶  preview
                                                                         <hash>.<project>.pages.dev
```

- **`main` is the production branch.** Every push to `main` deploys to `www.trustfractals.com`.
- **Every other branch and pull request gets its own preview deployment** at a unique
  `*.pages.dev` URL, and GitHub Actions CI runs on it. Merge to `main` to promote.
- GitHub Actions (`.github/workflows/ci.yml`) is the quality gate — build determinism +
  regression + rollup verification. Cloudflare Pages is the deploy. They are independent:
  CI green does not auto-block a Pages deploy unless you add branch protection (see below).

## Recommended day-to-day flow

```bash
git switch -c feature/thing      # branch off main
# ... edit src/app.html, then:
npm run build                    # regenerate index.html (NEVER hand-edit index.html)
npm test                         # local gate
git commit -am "…" && git push -u origin feature/thing
gh pr create                     # opens PR → CI runs + Cloudflare posts a preview URL
# review the preview, then merge → main auto-deploys to production
```

## Cloudflare Pages project settings

When connecting the repo in the Cloudflare dashboard (**Workers & Pages → Create → Pages →
Connect to Git**):

| Setting | Value |
|---|---|
| Repository | `bijoyr/portfolio-dashboard` |
| Production branch | `main` |
| Framework preset | None |
| Build command | *(leave empty)* |
| Build output directory | `/` |

No build command is needed because `index.html` is already the deterministic build output
(CI proves it matches source on every push). If you ever want Cloudflare to rebuild from
source instead, set the build command to `python3 scripts/build.py` and keep output `/`.

## Custom domain

`www.trustfractals.com` currently serves a placeholder. A domain can be attached to only one
Pages project at a time, so:

1. In the **old** placeholder project/service → **Custom domains** → remove
   `www.trustfractals.com` (and the apex `trustfractals.com` if it's there).
2. In this Pages project → **Custom domains** → **Set up a domain** → `www.trustfractals.com`.
   Because the zone is in the same Cloudflare account, the DNS record is created automatically.
3. Optional: attach the apex `trustfractals.com` too, or add a redirect rule apex → `www`.

## Protecting main

**Server-side** branch protection and rulesets require a public repo or GitHub Pro. This repo
is private on the free plan, so neither is available — GitHub returns 403. The two ways to get
a real server-side merge gate are to make the repo public or upgrade to Pro; do that and the
check to require is `build-and-test`.

Until then, protection is **client-side**, via a versioned pre-push hook that enforces the
build-determinism invariant before anything reaches `main`. Enable it once per clone:

```bash
git config core.hooksPath .githooks
```

The hook (`.githooks/pre-push`) rebuilds `index.html` and refuses the push if it no longer
matches source — the most common mistake. The full test suite still runs remotely in CI on
every PR; the hook is the fast local net. Bypass in an emergency with `git push --no-verify`.
