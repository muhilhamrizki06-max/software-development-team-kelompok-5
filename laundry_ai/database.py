import pymysql
from flask import g
import config

def _connect (dengan_db=True):
    return pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB if dengan_db else None,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        
    )
    
def db():
    """Koneksi database untuk yang sedang berjalan."""
    if "db" not in g:
        g.db = _connect()
        return g.db
    
def close_db(_=None):
    d = g.pop("db", None)
    if d:
        d.close()
        
def init_db():
    """Buat Database dan tabel jika belum ada."""
    # 1. membuat database nya dulu
    c = _connect(dengan_db=False)
    c.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {config.MYSQL_DB} CHARACTER SET utf8mb4")
    c.commit()
    c.close()
    
    # 2. membuat tabel nya
    c = _connect()
    c.cursor().execute("""
                        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('owner','karyawan') NOT NULL,
            aktif TINYINT NOT NULL DEFAULT 1
        )
    """)
    c.commit()
    c.close()