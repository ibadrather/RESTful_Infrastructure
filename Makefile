format:
	clear
	@echo "Running ruff formatter..."
	ruff format --line-length=120 server --exclude=.venv
	@echo "Running ruff linter..."
	ruff check --line-length=120 server --exclude=.venv

sync:
	cd server && uv sync

setup:
	clear
	@echo "Setting up the project..."
	pip install uv
	uv pip compile server/pyproject.toml -o requirements.txt
	uv pip sync requirements.txt
	rm requirements.txt

dev-setup:
	clear
	@echo "Setting up the project with dev and test dependencies..."
	pip install uv
	uv pip compile server/pyproject.toml -o requirements.txt
	uv pip compile server/pyproject.toml --extra dev -o dev-requirements.txt
	uv pip sync requirements.txt dev-requirements.txt
	rm requirements.txt dev-requirements.txt

	@echo "Setting up pre-commit..."
	uv pip install pre-commit
	pre-commit install

test:
	clear
	@echo "Running tests..."
	pytest server/tests


run:
	. server/.venv/bin/activate && python server/main.py
