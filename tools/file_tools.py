import os
from langchain.tools import tool

WORKSPACE = "workspace"


@tool
def create_file(input: str) -> str:
    """
    Create a file in the workspace.

    Input format:
    filename|||content

    Example:
    hello.py|||print("Hello World")
    """
    filename, content = input.split("|||")
    path = os.path.join(WORKSPACE, filename.strip())

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(content)

    return f"{filename} created successfully."


@tool
def read_file(filename: str) -> str:
    """
    Read a file from the workspace and return its contents.
    """
    path = os.path.join(WORKSPACE, filename.strip())

    if not os.path.exists(path):
        return "File not found."

    with open(path, "r") as f:
        return f.read()