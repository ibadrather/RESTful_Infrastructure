format:
	clear
	@echo "Running ruff formatter..."
	ruff format --line-length=120 server --exclude=.venv
	@echo "Running ruff linter..."
	ruff check --line-length=120 server --exclude=.venv

sync:
	cd server && uv sync
