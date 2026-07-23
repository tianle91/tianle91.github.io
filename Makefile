# Site chores. There is no build step here — GitHub Pages builds the site
# server-side from master (see AGENTS.md). These targets only cover the things
# you do by hand: bumping the StaticSites submodule, regenerating index.md's
# Interactive list from its manifest, and checking the result.

SITE    := https://tianle91.com
MSG     ?= bump StaticSites
SYNC    := python3 scripts/sync_staticsites.py

.DEFAULT_GOAL := help
.PHONY: help sync update publish check check-sync check-posts verify

help: ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync: ## Regenerate index.md from the currently pinned submodule
	$(SYNC)

update: ## Bump StaticSites to latest main and regenerate index.md
	$(SYNC) --update-submodule
	@git --no-pager diff --stat -- StaticSites index.md

publish: update ## Bump, regenerate, commit and push (publishes an updated map)
	@if git diff --quiet -- StaticSites index.md; then \
	  echo "Nothing to publish — StaticSites is already at the latest commit."; \
	else \
	  git commit -m '$(MSG)' -- StaticSites index.md && git push; \
	fi

check: check-sync check-posts ## Run the same checks CI runs

check-sync:
	$(SYNC) --check

check-posts:
	@bad=$$(ls _posts | grep -vE '^[0-9]{4}-[0-9]{2}-[0-9]{2}-' || true); \
	if [ -n "$$bad" ]; then \
	  echo "These _posts filenames don't match YYYY-MM-DD-title and won't publish:"; \
	  echo "$$bad"; exit 1; \
	fi; \
	echo "Post filenames OK."

verify: ## After pushing: check the Pages build and that every map returns 200
	@gh api repos/tianle91/tianle91.github.io/pages/builds/latest \
	  --jq '"build: \(.status)  commit: \(.commit)  error: \(.error.message // "none")"'
	@python3 -c "import json; \
	print('\n'.join(s['output'] for s in json.load(open('StaticSites/sites.json'))))" \
	  | while read -r out; do \
	      curl -s -o /dev/null -w "%{http_code}  $(SITE)/StaticSites/$$out\n" \
	        "$(SITE)/StaticSites/$$out"; \
	    done
