from pathlib import Path
import shutil

UPLOAD_DIR = Path("data/uploads")
CHROMA_DIR = Path("chroma_db")


def clear_knowledge_base():

    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)

    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)