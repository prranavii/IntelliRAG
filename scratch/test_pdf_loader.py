import os
import platform
import tempfile
from pathlib import Path

# Print OS and temp directory info
print("Platform system:", platform.system())
print("Temp directory:", tempfile.gettempdir())

# Local config mockup
if platform.system() == "Windows":
    UPLOAD_DIR = Path("data/uploads")
else:
    temp_base = Path(tempfile.gettempdir())
    UPLOAD_DIR = temp_base / "data" / "uploads"

print("UPLOAD_DIR path:", UPLOAD_DIR)
print("UPLOAD_DIR resolved:", UPLOAD_DIR.resolve())
print("UPLOAD_DIR exists?:", UPLOAD_DIR.exists())

if UPLOAD_DIR.exists():
    print("Files in UPLOAD_DIR:", os.listdir(UPLOAD_DIR))
else:
    print("Directory does not exist!")
