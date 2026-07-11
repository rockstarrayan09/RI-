import os
from pathlib import Path


from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

PERSISTENT_DIR = os.getenv("PERSISTENT_DIR", "").strip()
STORAGE_DIR = Path(PERSISTENT_DIR) if PERSISTENT_DIR else BASE_DIR

DATA_DIR = STORAGE_DIR / "data"
UPLOAD_DIR = STORAGE_DIR / "uploads" / "certificates"
EXCEL_PATH = Path(os.getenv("EXCEL_PATH", "").strip() or DATA_DIR / "records.xlsx")
DB_PATH = DATA_DIR / "services.db"

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production").strip()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin").strip()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123").strip()

# Second admin account (requested login)
ADMIN_USERNAME_2 = os.getenv("ADMIN_USERNAME_2", "rayan").strip()
ADMIN_PASSWORD_2 = os.getenv("ADMIN_PASSWORD_2", "281185").strip()

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

COMPANY_NAME = "RI ENTERPRISES"
FOUNDER_NAME = "RAFEEQ AHMED HUSSAIN"
CEO_NAME = "VAIZA IRFANA"
MD_NAME = "RAIHAN AHMED HUSSAIN"
COMPANY_TAGLINE = "Professional online government service support"
