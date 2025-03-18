import sqlite3

# ฟังก์ชันเชื่อมต่อกับฐานข้อมูล SQLite
def get_db_connection():
    conn = sqlite3.connect('OCR_receipt.db')
    conn.row_factory = sqlite3.Row  # เพื่อให้สามารถเข้าถึงค่าผ่านชื่อคอลัมน์
    return conn

# ฟังก์ชันสร้างตาราง
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # สร้างตาราง history_extract
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history_extract (
        receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name VARCHAR(255),
        date_time DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        receipt_number VARCHAR(255),
        vat DECIMAL(10, 2),
        total DECIMAL(10, 2),
        image_receipt varchar(255)
    )
    ''')
    
    # สร้างตาราง items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        receipt_number VARCHAR(255),
        created_item DATETIME DEFAULT CURRENT_TIMESTAMP,
        item_name VARCHAR(255),
        quantity INTEGER,
        price DECIMAL(10, 2)
    )
    ''')
    
    conn.commit()
    conn.close()
