import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("users.db")
    #drop table
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            age INTEGER,
            otp INTEGER,
            user TEXT,
            password TEXT
        )
    """)
    #create table to store fertilizer details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fertilizer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            name TEXT
        )
    """)
    conn.commit()
    conn.close()

# Register a new user
def register_user(name, email,age,otp,user, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, age, otp,user, password) VALUES (?, ?, ?, ?, ?, ?)", (name, email, age, otp,user, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

# Validate login credentials
def validate_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def valid_user(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def fetch_details(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_otp(email,otp):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET otp = ? WHERE email = ?", (otp, email))
    conn.commit()
    conn.close()

def fetch_otp(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT otp FROM users WHERE email = ?", (email,))
    otp = cursor.fetchone()
    conn.close()
    return otp

def update_password(email,password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE email = ?", (password, email))
    conn.commit()
    conn.close()

def fetch_password(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    password = cursor.fetchone()
    conn.close()
    return password