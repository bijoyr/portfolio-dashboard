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

## Optional: branch protection (make CI a merge gate)

To require the CI check to pass before anything reaches production:

```bash
gh api -X PUT repos/bijoyr/portfolio-dashboard/branches/main/protection \
  -f 'required_status_checks[strict]=true' \
  -f 'required_status_checks[contexts][]=build-and-test' \
  -F 'enforce_admins=false' \
  -F 'required_pull_request_reviews=null' \
  -F 'restrictions=null'
```

This forces changes through a PR whose CI passes — worth it once more than one person, or
one machine, touches the repo.
