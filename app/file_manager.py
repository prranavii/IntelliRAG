from rag.config import UPLOAD_DIR


def save_uploaded_files(uploaded_files):
    """
    Save uploaded PDFs.
    Clear old uploads before saving new ones.
    """
    # Ensure upload directory exists
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Remove existing files instead of deleting the directory
    for item in UPLOAD_DIR.iterdir():
        if item.is_file():
            try:
                item.unlink()
            except Exception:
                # Handle Windows file locking: ignore files that are locked/in-use
                pass

    saved_paths = []

    for uploaded_file in uploaded_files:
        base_path = UPLOAD_DIR / uploaded_file.name
        file_path = base_path
        
        # Handle file locking gracefully by trying fallback indexed filenames if write is blocked
        written = False
        attempts = 0
        while not written and attempts < 10:
            if attempts > 0:
                stem = base_path.stem
                suffix = base_path.suffix
                file_path = UPLOAD_DIR / f"{stem}_{attempts}{suffix}"
            
            try:
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                saved_paths.append(file_path)
                written = True
            except PermissionError:
                attempts += 1
            except Exception:
                raise

        # Final fallback: try writing directly, letting exceptions bubble up if still locked after 10 attempts
        if not written:
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