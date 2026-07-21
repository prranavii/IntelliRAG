import time
from pathlib import Path

UPLOAD_DIR = Path("data/uploads")
CHROMA_DIR = Path("chroma_db")
REPOS_DIR = Path("data/repos")
WEBSITES_DIR = Path("data/websites")


def delete_path_recursive(path):
    path = Path(path)
    if not path.exists():
        return
    for item in list(path.iterdir()):
        if item.is_file():
            try:
                item.unlink()
            except Exception:
                pass
        elif item.is_dir():
            delete_path_recursive(item)
    try:
        path.rmdir()
    except Exception:
        pass


def robust_cleanup(directory_path, delete_dir_itself=True):
    path = Path(directory_path)
    if not path.exists():
        return

    if delete_dir_itself:
        # Move locked directory out of the way on Windows by renaming it to a trash path
        trash_path = path.parent / f"{path.name}_trash_{int(time.time() * 1000)}"
        try:
            path.rename(trash_path)
            delete_path_recursive(trash_path)
        except Exception:
            # Fallback to in-place recursive deletion if rename is blocked
            delete_path_recursive(path)
    else:
        # Keep directory itself and delete only contents in-place
        delete_path_recursive(path)


def clear_knowledge_base():
    # Clean uploads folder contents (never delete uploads folder itself)
    robust_cleanup(UPLOAD_DIR, delete_dir_itself=False)

    # Clean chroma db directory (rename & delete trash)
    robust_cleanup(CHROMA_DIR, delete_dir_itself=True)

    # Clean repos and website downloads (rename & delete trash)
    robust_cleanup(REPOS_DIR, delete_dir_itself=True)
    robust_cleanup(WEBSITES_DIR, delete_dir_itself=True)

    # Recreate uploads folder if missing
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)