PROJECT := toronto-infrastructure-map
BUILD_SCRIPT := src/build_site.py
DATA_INPUTS := data/projects.json
SNAPSHOT_SCRIPT := src/snapshot_site.py

include ../artifact-project.mk

.PHONY: click-test
click-test: deps
	$(PY) src/check_clicks.py $(if $(BROWSER_EXECUTABLE),--browser-executable "$(BROWSER_EXECUTABLE)")

.PHONY: share-test
share-test: deps
	$(PY) src/check_share.py $(if $(BROWSER_EXECUTABLE),--browser-executable "$(BROWSER_EXECUTABLE)")
