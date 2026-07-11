import os
import uuid
from functools import wraps
from pathlib import Path

from flask import redirect, session, url_for
from werkzeug.utils import secure_filename

from config import ALLOWED_EXTENSIONS, UPLOAD_DIR


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file):
    if not file or not file.filename:
        return None, "No image file selected."

    if not allowed_file(file.filename):
        return None, "Invalid file type. Use JPG, PNG, or WEBP."

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file.save(UPLOAD_DIR / filename)
    return filename, None


def delete_upload(filename):
    if not filename:
        return
    path = UPLOAD_DIR / filename
    if path.exists():
        path.unlink()
