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

# Project settings
CXX_PROJECT_NAME = vehicle_client
CXX_SRC_DIR = vehicle_client
CXX_BUILD_DIR = vehicle_client/build

# C++ build target
build:
	mkdir -p $(CXX_BUILD_DIR)
	cd $(CXX_BUILD_DIR) && cmake ../$(CXX_SRC_DIR)
	cd $(CXX_BUILD_DIR) && make

# C++ run target
run-cxx: build
	cd $(CXX_BUILD_DIR) && ./$(CXX_BUILD_DIR)/$(CXX_PROJECT_NAME)

# Clean C++ build artifacts
clean-cxx:
	rm -rf $(CXX_BUILD_DIR)


# Clean all
clean: clean-cxx
	rm -rf server/__pycache__ server/*.egg-info
