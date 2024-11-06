# RESTful Infrastructure Server Documentation

This guide will walk you through setting up, testing, and running the server component of the RESTful Infrastructure application. You’ll find both `Makefile` targets and direct commands to ensure flexibility in usage.

If you want to read more about Database please go to `server/database/README.md`

---

## Dependencies

To set up and run the server, make sure you have the following dependencies installed:

1. **Python >=3.11+**

2. **pip**  (Python package installer)

3. **uv**  – a tool for managing dependencies and virtual environments.Install `uv` with:

```bash
pip install uv
```

Create a new virtual environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Initial Setup

To prepare the server for development or production, follow the steps below (All commands are expected to be run from the root folder where the `server/` directory sits):

### 1. Basic Setup (Production)

This setup installs only the core dependencies for running the server. Use this if you do not need development or testing tools.

- **Makefile Target** :

```bash
make py-setup
```

- **Direct Command** :

```bash
uv pip compile server/pyproject.toml -o requirements.txt && \
uv pip sync requirements.txt && \
rm requirements.txt
```

### 2. Development Setup (Recommended for development)

For development, you’ll need additional tools for testing, linting, and pre-commit hooks.

- **Makefile Target** :

```bash
make py-dev-setup
```

- **Direct Command** :

```bash
uv pip compile server/pyproject.toml -o requirements.txt && \
uv pip compile server/pyproject.toml --extra dev -o dev-requirements.txt && \
uv pip sync requirements.txt dev-requirements.txt && \
rm requirements.txt dev-requirements.txt && \
uv pip install pre-commit && \
pre-commit install
```

---

## Running the Server
Once dependencies are installed, you can start the API server. The server’s main file, `server/main.py`, launches the API.

- **Makefile Target** :

```bash
make run-api
```

- **Direct Command** :

```bash
python server/main.py
```

> **Note** : If using a frontend with the API, see the optional frontend section below.

---

## Running the Frontend (Optional)

An optional Streamlit frontend is available for visual interaction with the API. This frontend is mainly for demonstration purposes.

- **Makefile Target** :

```bash
make run-frontend
```

- **Direct Command** :

```bash
streamlit run server/frontend.py
```

---

## Code Quality and Formatting
Maintain code quality using `ruff` for both formatting and linting.
### Format and Lint
This command reformats the code and checks for style issues based on `ruff` configurations.

- **Makefile Target** :

```bash
make format
```

- **Direct Command** :

```bash
ruff format --line-length=120 server --exclude=.venv && \
ruff check --line-length=120 server --exclude=.venv
```

---

## Testing
Run the test suite to validate the server's functionality. Tests are located in the `server/tests` directory and use `pytest`.
- **Makefile Target** :

```bash
make test-server
```

- **Direct Command** :

```bash
pytest server/tests
```

---

## Dependency Synchronization
To ensure all dependencies are aligned with the latest configurations in `server/pyproject.toml`, use the `sync` command.
- **Makefile Target** :

```bash
make sync
```

- **Direct Command** :

```bash
cd server && uv sync
```

---
