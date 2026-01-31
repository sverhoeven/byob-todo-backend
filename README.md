# Bring your own backend - TODO web service

Web service for TODO list management.

Requires [uv](https://docs.astral.sh/uv/) to be installed on a Linux, macOS or WSL machine.

Run with:

```shell
./byod-todo-backend.py
```

Other commands:

```shell
# Format
uvx ruff format
# Lint
uvx ruff check
# Type check
uvx --with-requirements ./byod-todo-backend.py pyright
```