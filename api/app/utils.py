import hashlib
import os

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}


def allowed_file(filename: str) -> bool:
    """
    Check if the file has an allowed image extension.
    """
    if not filename:
        return False

    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS


async def get_file_hash(file):
    """
    Generate a new filename using MD5 hash of file content,
    keeping the original extension.
    """
    # Read file content (UploadFile.read is async)
    file_content = await file.read()

    # Generate MD5 hash
    md5_hash = hashlib.md5(file_content).hexdigest()

    # Reset file pointer so it can be read again later
    await file.seek(0)

    # Keep original extension
    _, ext = os.path.splitext(file.filename)

    return f"{md5_hash}{ext}"
