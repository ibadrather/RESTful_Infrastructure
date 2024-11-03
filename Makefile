################
# Python Targets
################

format:
	clear
	@echo "Running ruff formatter..."
	ruff format --line-length=120 server --exclude=.venv
	@echo "Running ruff linter..."
	ruff check --line-length=120 server --exclude=.venv

sync:
	cd server && uv sync

py-setup:
	clear
	@echo "Setting up the project..."

	# python dependencies
	pip install uv
	uv pip compile server/pyproject.toml -o requirements.txt
	uv pip sync requirements.txt
	rm requirements.txt

py-dev-setup:
	clear
	@echo "Setting up the project with dev and test dependencies..."

	# python dependencies
	pip install uv
	uv pip compile server/pyproject.toml -o requirements.txt
	uv pip compile server/pyproject.toml --extra dev -o dev-requirements.txt
	uv pip sync requirements.txt dev-requirements.txt
	rm requirements.txt dev-requirements.txt

	@echo "Setting up pre-commit..."
	uv pip install pre-commit
	pre-commit install

test-server:
	clear
	@echo "Running tests..."
	pytest server/tests

run-api:
	python server/main.py

################
# C++ Targets
################
build-run-client:
	@if [ -d "vehicle_client/build" ]; then rm -r vehicle_client/build; fi
	mkdir -p vehicle_client/build
	cd vehicle_client/build && cmake .. && make && ./vehicle_client

build-run-client-scratch:
	rm -rf vehicle_client/build
	mkdir -p vehicle_client/build
	cd vehicle_client/build && cmake .. && make && ./vehicle_client

format-cpp:
	find vehicle_client/ \( -name "*.cpp" -o -name "*.hpp" \) -not -name "json.hpp" -not -path "vehicle_client/build/*" -exec clang-format -i {} +
