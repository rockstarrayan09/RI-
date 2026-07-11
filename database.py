import sqlite3
from datetime import datetime

from config import DB_PATH, DATA_DIR


SEED_SERVICES = [
    ("Income Certificate", 150, None),
    ("Community Certificate", 200, None),
    ("Nativity Certificate", 150, None),
    ("Residence Certificate", 100, None),
    ("OBC Certificate", 250, None),
]

DEFAULT_SITE_SETTINGS = {
    "company_name": "RI ENTERPRISES",
    "founder_name": "RAFEEQ AHMED HUSSAIN",
    "ceo_name": "VAIZA IRFANA",
    "md_name": "RAIHAN AHMED HUSSAIN",
    "company_tagline": "Professional online government service support",
    "home_kicker": "Government Service Support Centre",
    "home_title": "Welcome to RI ENTERPRISES",
    "home_intro": "Please click any service below to view documents, check the sample certificate, and submit customer details.",
    "services_heading": "Online Services",
    "services_subtitle": "Choose the service you need.",
    "admin_warning": "This admin portal only belongs to RAIHAN AHMED HUSSAIN. Not for everyone. Please go to the home screen.",
}


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            image_filename TEXT,
            created_at TEXT NOT NULL,
            government_amount REAL NOT NULL DEFAULT 0
        )
        """
    )
    # Migration: add government_amount column to any existing database
    # created before this field existed.
    existing_columns = {row["name"] for row in conn.execute("PRAGMA table_info(services)")}
    if "government_amount" not in existing_columns:
        conn.execute(
            "ALTER TABLE services ADD COLUMN government_amount REAL NOT NULL DEFAULT 0"
        )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            is_mandatory INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS service_documents (
            service_id INTEGER NOT NULL,
            document_id INTEGER NOT NULL,
            PRIMARY KEY (service_id, document_id),
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
            FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS site_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    for key, value in DEFAULT_SITE_SETTINGS.items():
        conn.execute(
            "INSERT OR IGNORE INTO site_settings (key, value) VALUES (?, ?)",
            (key, value),
        )
    count = conn.execute("SELECT COUNT(*) FROM services").fetchone()[0]
    if count == 0:
        now = datetime.now().isoformat()
        for name, amount, image in SEED_SERVICES:
            conn.execute(
                "INSERT INTO services (name, amount, image_filename, created_at) VALUES (?, ?, ?, ?)",
                (name, amount, image, now),
            )
    conn.commit()
    conn.close()


def get_site_settings():
    conn = get_connection()
    rows = conn.execute("SELECT key, value FROM site_settings").fetchall()
    conn.close()
    settings = DEFAULT_SITE_SETTINGS.copy()
    settings.update({row["key"]: row["value"] for row in rows})
    return settings


def update_site_settings(settings):
    conn = get_connection()
    for key in DEFAULT_SITE_SETTINGS:
        value = (settings.get(key) or "").strip()
        if not value:
            value = DEFAULT_SITE_SETTINGS[key]
        conn.execute(
            """
            INSERT INTO site_settings (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
    conn.commit()
    conn.close()


def get_all_services():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM services ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_service(service_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM services WHERE id = ?", (service_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def _set_service_documents(conn, service_id, document_ids):
    conn.execute("DELETE FROM service_documents WHERE service_id = ?", (service_id,))
    for document_id in document_ids or []:
        if document_id:
            conn.execute(
                "INSERT OR IGNORE INTO service_documents (service_id, document_id) VALUES (?, ?)",
                (service_id, document_id),
            )


def create_service(name, amount, image_filename, document_ids=None, government_amount=0):
    conn = get_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute(
        """
        INSERT INTO services (name, amount, image_filename, created_at, government_amount)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, amount, image_filename, now, government_amount),
    )
    service_id = cursor.lastrowid
    _set_service_documents(conn, service_id, document_ids)
    conn.commit()
    conn.close()
    return service_id


def update_service(
    service_id,
    name,
    amount,
    image_filename=None,
    document_ids=None,
    government_amount=0,
):
    conn = get_connection()
    if image_filename:
        conn.execute(
            """
            UPDATE services
            SET name = ?, amount = ?, image_filename = ?, government_amount = ?
            WHERE id = ?
            """,
            (name, amount, image_filename, government_amount, service_id),
        )
    else:
        conn.execute(
            "UPDATE services SET name = ?, amount = ?, government_amount = ? WHERE id = ?",
            (name, amount, government_amount, service_id),
        )
    _set_service_documents(conn, service_id, document_ids)
    conn.commit()
    conn.close()


def delete_service(service_id):
    conn = get_connection()
    conn.execute("DELETE FROM service_documents WHERE service_id = ?", (service_id,))
    conn.execute("DELETE FROM services WHERE id = ?", (service_id,))
    conn.commit()
    conn.close()


def get_all_documents():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM documents ORDER BY name").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_document(document_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM documents WHERE id = ?", (document_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_document(name, description, is_mandatory=True):
    conn = get_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute(
        "INSERT INTO documents (name, description, is_mandatory, created_at) VALUES (?, ?, ?, ?)",
        (name, description, 1 if is_mandatory else 0, now),
    )
    document_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return document_id


def update_document(document_id, name, description, is_mandatory=True):
    conn = get_connection()
    conn.execute(
        "UPDATE documents SET name = ?, description = ?, is_mandatory = ? WHERE id = ?",
        (name, description, 1 if is_mandatory else 0, document_id),
    )
    conn.commit()
    conn.close()


def delete_document(document_id):
    conn = get_connection()
    conn.execute("DELETE FROM service_documents WHERE document_id = ?", (document_id,))
    conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
    conn.commit()
    conn.close()


def get_service_document_ids(service_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT document_id FROM service_documents WHERE service_id = ?",
        (service_id,),
    ).fetchall()
    conn.close()
    return [row["document_id"] for row in rows]


def get_documents_for_service(service_id):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT d.*
        FROM documents d
        INNER JOIN service_documents sd ON sd.document_id = d.id
        WHERE sd.service_id = ?
        ORDER BY d.name
        """,
        (service_id,),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
