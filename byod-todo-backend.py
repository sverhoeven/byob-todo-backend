#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "fastapi", "uvicorn"
# ]
# ///
# Above is inline script metadata
# See https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Generator
import json

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


@dataclass
class Todo:
    title: str
    done: bool = False


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


@contextmanager
def todos_store(file=Path("todos.json")) -> Generator[list[Todo], None, None]:
    todos: list[Todo] = []
    if file.exists():
        todos = [Todo(**item) for item in json.loads(file.read_text())]
    yield todos
    file.write_text(json.dumps([asdict(todo) for todo in todos], indent=2))


@app.get("/")
def get_todos(done: bool | None = None) -> list[Todo]:
    with todos_store() as todos:
        if done is None:
            return todos
        return [todo for todo in todos if todo.done == done]


@app.post("/")
def create_todo(todo: Todo):
    with todos_store() as todos:
        todos.append(todo)


@contextmanager
def get_todo(title: str) -> Generator[Todo, None, None]:
    with todos_store() as todos:
        todo = next((todo for todo in todos if todo.title == title), None)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        else:
            yield todo


@app.delete("/{title}")
def delete_todo(title: str):
    with todos_store() as todos, get_todo(title) as todo:
        todos.remove(todo)


@app.put("/{title}")
def set_done(title: str, done: bool):
    with get_todo(title) as todo:
        todo.done = done


def main() -> None:
    url = (
        "https://sverhoeven.github.io/byob-todo-frontend/?backend=http://localhost:8000"
    )
    link = f"\x1b]8;;{url}\x1b\\{url}\x1b]8;;\x1b\\"
    print(f"""\
Starting TODO backend service ...
Open TODO frontend at:
{link}
(Press CTRL+C to quit)
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")


if __name__ == "__main__":
    main()
