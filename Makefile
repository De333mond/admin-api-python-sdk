PROTO_DIR=src/admin_api/grpc/_protos
OUT_DIR=src/admin_api/grpc/_generated
PROTO_FILES=$(shell find $(PROTO_DIR) -name "*.proto")

.PHONY: lint format typecheck test check grpc_generate grpc_clean grpc_regen

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

grpc_generate:
	@mkdir -p $(OUT_DIR)
	uv run python -m grpc_tools.protoc \
		-I $(PROTO_DIR) \
		--python_out=$(OUT_DIR) \
		--grpc_python_out=$(OUT_DIR) \
		--mypy_out=$(OUT_DIR) \
		$(PROTO_FILES)

	find $(OUT_DIR) -name '*.py' -exec \
		sed -Ei 's/^from ([a-zA-Z_][a-zA-Z0-9_]*) import/from ..\1 import/' {} \;

grpc_clean:
	rm -rf $(OUT_DIR)/*

make grpc_regen: 
	make grpc_clean grpc_generate

