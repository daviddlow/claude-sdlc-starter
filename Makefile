# Single-command targets are the Stage 4 play "Give Claude a feedback loop":
# if checking the work takes a sequence of commands and environment
# knowledge, wrap it so one command exits non-zero on failure.
# CLAUDE.md lists these with an example of healthy output.

PYTHONPATH := src
export PYTHONPATH

.PHONY: build test lint run

build:
	python3 -m compileall -q src tests
	@echo "Build succeeded"

test:
	python3 -m unittest discover -s tests -v

lint:
	@if command -v ruff >/dev/null 2>&1; then \
		ruff check src tests; \
	else \
		python3 -m compileall -q src tests && echo "lint: ruff not installed, syntax check only"; \
	fi

run:
	python3 -m claims_api.demo
