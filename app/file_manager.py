from pathlib import Path

UPLOAD_DIR = Path("data/uploads")


def save_uploaded_files(uploaded_files):

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old PDFs
    for pdf in UPLOAD_DIR.glob("*.pdf"):
        pdf.unlink()

    saved_files = []

    for uploaded_file in uploaded_files:

        file_path = UPLOAD_DIR / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        saved_files.append(uploaded_file.name)

    return saved_files


def get_uploaded_files():

    if not UPLOAD_DIR.exists():
        return []

    return [pdf.name for pdf in UPLOAD_DIR.glob("*.pdf")]