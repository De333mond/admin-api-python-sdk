DTO_OUT=src/admin_api/api/dto/__init__.py

.PHONY: lint format typecheck test check dto_generate

ruff_check:
	uv run ruff check .

ruff_fix:
	uv run ruff check . --fix

format:
	uv run ruff format .

typecheck:
	uv run mypy src

test:
	uv run pytest

check: lint typecheck test

dto_generate:
	uv run datamodel-codegen \
		--input openapi.json \
		--input-file-type openapi \
		--output $(DTO_OUT) \
		--output-model-type pydantic_v2.BaseModel \
		--use-standard-collections \
		--use-union-operator \
		--target-python-version 3.11 \
		--use-subclass-enum \
		--collapse-root-models \
		--output-datetime-class datetime \
		--formatters ruff-format \
		--use-title-as-name
