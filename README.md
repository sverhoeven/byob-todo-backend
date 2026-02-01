# Bring your own backend - TODO web service

Web service for TODO list management.

Companion of the [BYOB TODO frontend](https://github.com/sverhoeven/byob-todo-frontend).

Requires [uv](https://docs.astral.sh/uv/) to be installed on a Linux, macOS or WSL machine.

Run with:

```shell
# From GitHub
uv run https://raw.githubusercontent.com/sverhoeven/byob-todo-backend/refs/heads/main/byod-todo-backend.py
# or using local clone
./byod-todo-backend.py
```

The todos are persisted in a `todos.json` file in the current working directory.
Got [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

Other commands:

```shell
# Format
uvx ruff format
# Lint
uvx ruff check
# Type check
uvx --with-requirements ./byod-todo-backend.py pyright
```
