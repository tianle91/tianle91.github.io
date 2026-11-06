# Site checks and project-directory sync. GitHub Pages publishes master server-side.

SITE    := https://tianle91.com
SYNC    := python3 scripts/sync_staticsites.py

.DEFAULT_GOAL := help
.PHONY: help sync check check-sync check-posts check-staticsites verify

help: ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync: ## Regenerate index.md from StaticSites/sites.json
	$(SYNC)

check: check-sync check-posts check-staticsites ## Check the homepage, posts and every static project

check-sync:
	$(SYNC) --check
	python3 -m unittest discover -s scripts -p 'test_*.py'

check-posts:
	@bad=$$(ls _posts | grep -vE '^[0-9]{4}-[0-9]{2}-[0-9]{2}-' || true); \
	if [ -n "$$bad" ]; then \
	  echo "These _posts filenames don't match YYYY-MM-DD-title and won't publish:"; \
	  echo "$$bad"; exit 1; \
	fi; \
	echo "Post filenames OK."

check-staticsites: ## Test and build every static project from committed inputs
	$(MAKE) -C StaticSites test STATUSES=off

verify: ## After pushing: check the Pages build and that every map returns 200
	@gh api repos/tianle91/tianle91.github.io/pages/builds/latest \
	  --jq '"build: \(.status)  commit: \(.commit)  error: \(.error.message // "none")"'
	@python3 -c "import json; \
	print('\n'.join(s['output'] for s in json.load(open('StaticSites/sites.json'))))" \
	  | while read -r out; do \
	      curl -s -o /dev/null -w "%{http_code}  $(SITE)/StaticSites/$$out\n" \
	        "$(SITE)/StaticSites/$$out"; \
	    done
