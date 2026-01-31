#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "fastapi", "uvicorn"
# ]
# ///
# Above is inline script metadata
# See https://docs.astral.sh/uv/guides/scripts/#declaring-script-dependencies
from dataclasses import dataclass

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

todos: list[Todo] = []


@app.get("/")
def get_todos(done: bool | None = None) -> list[Todo]:
    if done is None:
        return todos
    return [todo for todo in todos if todo.done == done]


@app.post("/")
def create_todo(todo: Todo):
    todos.append(todo)


def get_todo(title: str) -> Todo:
    for todo in todos:
        if todo.title == title:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")


@app.delete("/{title}")
def delete_todo(title: str):
    todos.remove(get_todo(title))


@app.put("/{title}")
def set_done(title: str, done: bool):
    todo = get_todo(title)
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
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        # , log_level="error"
    )


if __name__ == "__main__":
    main()
