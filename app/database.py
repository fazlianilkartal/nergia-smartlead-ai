import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_URL"]
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                eposta TEXT NOT NULL DEFAULT '',
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Eski kayitlari koruyarak e-posta sutununu ekle.
        sutunlar = {satir[1] for satir in db.execute("PRAGMA table_info(leads)")}
        if "eposta" not in sutunlar:
            db.execute("ALTER TABLE leads ADD COLUMN eposta TEXT NOT NULL DEFAULT ''")

        db.commit()

    app.teardown_appcontext(close_db)


def lead_ekle(isim, telefon, mesaj=None, eposta=""):
    db = get_db()

    db.execute(
        "INSERT INTO leads (isim, telefon, mesaj, eposta) VALUES (?, ?, ?, ?)",
        (isim, telefon, mesaj, eposta)
    )

    db.commit()


def tum_leadler():
    db = get_db()

    kayitlar = db.execute(
        """
        SELECT id, isim, telefon, mesaj, eposta, tarih
        FROM leads
        ORDER BY id DESC
        """
    ).fetchall()

    return [dict(kayit) for kayit in kayitlar]