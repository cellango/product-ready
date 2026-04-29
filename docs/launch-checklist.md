# Launch Checklist — v1.2.0

Steps you need to complete before making the repo public and submitting to the skill registry.
All automated work (code, tests, adapters, docs) is already done.

---

## 1. Encrypt the Ansible Vault

The file `infra/inventory/group_vars/vault.yml` contains production secret placeholders.
Encrypt it before committing it to a public repo:

```bash
cd infra
ansible-vault encrypt inventory/group_vars/vault.yml
# Choose a strong password and store it in your password manager
```

Verify it's encrypted:
```bash
head -1 infra/inventory/group_vars/vault.yml
# Should start with: $ANSIBLE_VAULT;1.1;AES256
```

---

## 2. Fill in production secrets (Ansible Vault)

```bash
cd infra
ansible-vault edit inventory/group_vars/vault.yml
```

Replace every `REPLACE-ME` value:
- `vault_slack_bot_token` — from Slack App > OAuth & Permissions
- `vault_slack_signing_secret` — from Slack App > Basic Information
- `vault_anthropic_api_key` OR `vault_openai_api_key`
- `vault_jira_base_url`, `vault_jira_email`, `vault_jira_api_token`, `vault_jira_project_key`

---

## 3. Update `infra/inventory/group_vars/all.yml`

```yaml
domain:       bot.yourcompany.com    # ← real domain pointing at your Hetzner server
certbot_email: ops@yourcompany.com   # ← real email for Let's Encrypt alerts
```

---

## 4. Update `infra/inventory/production.ini`

```ini
[hetzner]
prod ansible_host=YOUR_HETZNER_IP   # ← real IP from Hetzner console
```

---

## 5. Update `slack-app-manifest.json`

Replace `YOUR_HOST` with your actual domain:
```bash
sed -i '' 's/YOUR_HOST/bot.yourcompany.com/g' slack-app-manifest.json
```

Then in your Slack App dashboard:
- Go to **App Manifest** → paste the updated manifest
- Go to **Event Subscriptions** → verify `https://bot.yourcompany.com/slack/events`
- Go to **Interactivity** → verify `https://bot.yourcompany.com/slack/interactive`

---

## 6. Create the Hetzner server

In [Hetzner Cloud Console](https://console.hetzner.cloud):
1. **New server** → Ubuntu 24.04, CX22 (2 vCPU, 4 GB RAM, ~€4/mo)
2. Add your SSH public key during creation
3. Note the server IP → update `production.ini`
4. Set an A record: `bot.yourcompany.com` → server IP (allow 5–10 min to propagate)

---

## 7. Provision the server

```bash
make provision
# Enter vault password when prompted
# Takes ~5 minutes on a fresh server
```

Verify:
```bash
curl https://bot.yourcompany.com/health
# Should return: {"status": "ok", "active_threads": 0}
```

---

## 8. Configure the Slack app

In your Slack workspace:
1. Go to [api.slack.com/apps](https://api.slack.com/apps) → your app
2. **Install App** → Install to Workspace → copy `Bot User OAuth Token` (xoxb-...)
3. Add to vault: `vault_slack_bot_token`
4. Enable **Socket Mode** off (you're using HTTP mode in production)
5. Verify all slash commands point to `https://bot.yourcompany.com/slack/events`

Test:
```bash
# In any Slack channel where the bot is installed
/product-ready
# Bot should respond with Tier 3 first interaction
```

---

## 9. Make the GitHub repo public

At https://github.com/cellango/product-ready:
1. **Settings** → **General** → **Danger Zone** → **Change visibility** → Public
2. Verify CI badge resolves: [![CI](https://github.com/cellango/product-ready/actions/workflows/ci.yml/badge.svg)](https://github.com/cellango/product-ready/actions)

---

## 10. Create the GitHub Release

```bash
cd /Users/clementellango/CascadeProjects/product-ready
git tag v1.2.0
git push origin v1.2.0
```

Then on GitHub:
1. Go to **Releases** → **Create a new release**
2. Tag: `v1.2.0`
3. Title: `v1.2.0 — AI-native Spec-Driven Development`
4. Body: paste contents of `docs/release-notes-v1.2.0.md`
5. Publish release

---

## 11. Submit to the Anthropic skill registry

1. Fork: https://github.com/anthropics/skills
2. Create directory `skills/product-ready/` in your fork
3. Copy files:
   ```bash
   cp adapters/anthropic/SKILL.md  /path/to/fork/skills/product-ready/SKILL.md
   cp infra/skill-registry/README.md /path/to/fork/skills/product-ready/README.md
   ```
4. Open a PR with:
   - **Title:** `Add product-ready skill — AI-native Spec-Driven Development for Product Owners`
   - **Body:**
     ```
     ## Summary
     Product Ready is an AI-native Spec-Driven Development skill for Product Owners.
     It guides users from a vague idea to a complete BDD Spec, scores spec quality
     across 5 dimensions, and generates AI-ready prompts from each scenario.

     ## Features
     - 13-step adaptive workflow (Lightweight / Standard / Full)
     - 8 enforced guardrails including Spec Integrity gate
     - Spec Quality Score: Complete / Partial / Incomplete
     - Step 5b: Generate from Spec (one AI prompt block per BDD scenario)
     - Three-tier First Interaction rule (no menus, no intros unless needed)

     ## Testing
     - 135 tests, all passing
     - Structural integrity tests enforce all guardrails and the SDD model

     ## License
     Apache 2.0

     ## Source
     https://github.com/cellango/product-ready
     ```

---

## 12. Community posts

Use `docs/product-ready-positioning.md` as the source for all posts.

**Product Hunt:**
- Name: Product Ready
- Tagline: AI-native Spec-Driven Development for Product Owners
- Description: first two sections of the positioning doc

**Reddit (r/ProductManagement, r/artificial):**
> We built an open-source AI skill that makes Spec-Driven Development practical for Product Owners.
> The chain: PRD → BDD Spec (THE SPEC) → [AI: Tests + Code] → Acceptance.
> Key insight: the BDD Spec is scored for quality before any AI generation is allowed.
> https://github.com/cellango/product-ready

**Lenny's Newsletter Slack, Mind the Product community:**
> Anyone else finding that AI coding tools are great at generating code from clear specs,
> but the bottleneck is now writing specs that are actually AI-ready?
> We built something that solves this: [link]

---

## Status tracker

- [ ] Vault encrypted
- [ ] Production secrets filled in
- [ ] `all.yml` updated with real domain
- [ ] `production.ini` updated with server IP
- [ ] `slack-app-manifest.json` updated with domain
- [ ] Hetzner server created and A record set
- [ ] `make provision` completed successfully
- [ ] `/health` returns 200
- [ ] Slack app configured and bot responds to `/product-ready`
- [ ] GitHub repo made public
- [ ] `git tag v1.2.0 && git push origin v1.2.0`
- [ ] GitHub Release created
- [ ] PR submitted to anthropics/skills
- [ ] Community posts published
