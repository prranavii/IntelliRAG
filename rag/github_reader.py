from pathlib import Path
from langchain_core.documents import Document

IGNORE_DIRS = {
    ".git",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build"
}

SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".cpp",
    ".c",
    ".js",
    ".ts",
    ".md",
    ".txt"
}


def load_repository(repo_path):

    documents = []

    repo_path = Path(repo_path)

    for file in repo_path.rglob("*"):

        if any(part in IGNORE_DIRS for part in file.parts):
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:

            text = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": str(file),
                        "filename": file.name,
                        "extension": file.suffix,
                        "folder": str(file.parent)
                    }
                )
            )

        except Exception:
            pass

    return documents