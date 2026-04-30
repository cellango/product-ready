.PHONY: dev dev-raw test test-watch pip-compile pip-sync provision deploy vault-edit vault-encrypt logs ssh

# ── Local development ─────────────────────────────────────────────────────────

## Start the bot locally in Docker (Socket Mode — no public URL needed).
## Requires SLACK_APP_TOKEN in .env
dev:
	docker-compose up --build

## Run the bot directly (no Docker) — fastest iteration loop.
## Requires a Python venv with `pip install -r requirements.txt -r requirements-dev.txt`
dev-raw:
	python -m slack_bot.app

# ── Tests ─────────────────────────────────────────────────────────────────────

## Run the full test suite.
test:
	python3 -m pytest tests/ -v

## Run tests and re-run on file change (requires pytest-watch).
test-watch:
	ptw tests/ -- -v

# ── Dependency management ─────────────────────────────────────────────────────

## Compile pinned lock files from *.in sources.
## Run this after editing requirements.in or requirements-dev.in, then commit both *.txt files.
pip-compile:
	pip-compile requirements.in --generate-hashes --quiet --output-file requirements.txt
	pip-compile requirements-dev.in --generate-hashes --quiet --output-file requirements-dev.txt
	@echo "Lock files updated. Commit requirements.txt and requirements-dev.txt."

## Install exact pinned dev dependencies into the current virtualenv.
pip-sync:
	pip-sync requirements-dev.txt

# ── Infrastructure ────────────────────────────────────────────────────────────

## First-time server setup. Run once after creating the Hetzner server.
## Prerequisites: A record for `domain` pointing at the server IP.
provision:
	cd infra && ansible-playbook provision.yml --ask-vault-pass

## Deploy the latest code to production.
deploy:
	cd infra && ansible-playbook deploy.yml --ask-vault-pass

## Edit the Ansible Vault (secrets file).
vault-edit:
	cd infra && ansible-vault edit inventory/group_vars/vault.yml

## Encrypt the vault file (run after filling in secrets for the first time).
vault-encrypt:
	cd infra && ansible-vault encrypt inventory/group_vars/vault.yml

# ── Server operations ─────────────────────────────────────────────────────────

## Tail production logs (reads SERVER_IP from infra/inventory/production.ini).
logs:
	ssh root@$(shell grep 'ansible_host' infra/inventory/production.ini | awk '{print $$2}' | cut -d= -f2) \
	    "docker logs -f product-ready-bot --tail 100"

## SSH into the production server.
ssh:
	ssh root@$(shell grep 'ansible_host' infra/inventory/production.ini | awk '{print $$2}' | cut -d= -f2)
