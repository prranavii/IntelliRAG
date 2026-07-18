from pathlib import Path
import shutil

UPLOAD_DIR = Path("data/uploads")


def save_uploaded_files(uploaded_files):
    """
    Save uploaded PDFs.
    Clear old uploads before saving new ones.
    """

    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    saved_paths = []

    for uploaded_file in uploaded_files:
        file_path = UPLOAD_DIR / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        saved_paths.append(file_path)

    return saved_paths


def get_uploaded_files():
    """
    Return a list of uploaded file names.
    """

    if not UPLOAD_DIR.exists():
        return []

    return sorted(
        [
            file.name
            for file in UPLOAD_DIR.iterdir()
            if file.is_file()
        ]
    )