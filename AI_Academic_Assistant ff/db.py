import os
import hashlib
import secrets
import sqlite3

# Try importing psycopg2
try:
    import psycopg2
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

class DB:
    _connection = None
    _is_sqlite = False

    @classmethod
    def get_connection(cls):
        if cls._connection is not None:
            return cls._connection
        
        # Try connecting to PostgreSQL
        if HAS_POSTGRES:
            try:
                cls._connection = psycopg2.connect(
                    host="localhost",
                    database="academic_ai",
                    user="postgres",
                    password="your_password",
                    port="5432"
                )
                cls._is_sqlite = False
                print("Connected to PostgreSQL database.")
                return cls._connection
            except Exception as e:
                print(f"PostgreSQL connection failed: {e}. Falling back to SQLite.")
        
        # Fallback to SQLite
        cls._connection = sqlite3.connect("academic_ai.db", check_same_thread=False)
        cls._is_sqlite = True
        print("Connected to SQLite database.")
        return cls._connection

    @classmethod
    def get_cursor(cls):
        conn = cls.get_connection()
        return conn.cursor()

# Run table initialization on database check
def init_db():
    conn = DB.get_connection()
    cursor = DB.get_cursor()
    
    if DB._is_sqlite:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            department TEXT
        )
        """)
    else:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            salt VARCHAR(64) NOT NULL,
            department VARCHAR(100)
        )
        """)
    conn.commit()

# Hash a password with salt using standard library PBKDF2
def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    pwd_bytes = password.encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100000)
    return key.hex(), salt

# Register new faculty
def register_faculty(name, email, password, department):
    conn = DB.get_connection()
    cursor = DB.get_cursor()
    
    password_hash, salt = hash_password(password)
    
    placeholder = "?" if DB._is_sqlite else "%s"
    query = f"""
    INSERT INTO faculty (name, email, password_hash, salt, department)
    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
    """
    try:
        cursor.execute(query, (name, email, password_hash, salt, department))
        conn.commit()
        return True, "Registration successful."
    except Exception as e:
        err_msg = str(e)
        if "UNIQUE" in err_msg.upper():
            return False, "Email already registered."
        return False, f"Registration failed: {err_msg}"

# Verify credentials
def verify_faculty(email, password):
    conn = DB.get_connection()
    cursor = DB.get_cursor()
    
    placeholder = "?" if DB._is_sqlite else "%s"
    query = f"SELECT name, password_hash, salt, department FROM faculty WHERE email = {placeholder}"
    
    try:
        cursor.execute(query, (email,))
        row = cursor.fetchone()
        if not row:
            return None, "Invalid email or password."
        
        name, stored_hash, salt, department = row
        password_hash, _ = hash_password(password, salt)
        
        if password_hash == stored_hash:
            return {
                "name": name,
                "email": email,
                "department": department
            }, "Login successful."
        else:
            return None, "Invalid email or password."
    except Exception as e:
        return None, f"Database error: {str(e)}"

# Run initialization immediately when db is imported/loaded
init_db()