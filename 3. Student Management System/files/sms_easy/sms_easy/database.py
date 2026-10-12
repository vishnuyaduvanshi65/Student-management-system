"""
database.py

Ye file sirf database ka kaam karti hai.
Yaha hum SQLite database ke saath connect karte hain aur
data add/read/update/delete karte hain.

Simple funda: "database.py" = database ka kaam
             "main.py"      = menu aur user se baat cheet ka kaam
"""

import sqlite3


def connect():
    # Ye function database se connection kholta hai
    # Agar "students.db" file exist nahi karti, to SQLite khud bana deta hai
    conn = sqlite3.connect("students.db")
    return conn


def create_table():
    # Table banate hain agar pehle se nahi bana hai
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            course TEXT,
            marks REAL
        )
    """)

    conn.commit()
    conn.close()


def add_student(student_id, name, email, phone, course, marks):
    # Naya student add karna
    # "?" use karte hain taki SQL Injection na ho (safe tarika)
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
            (student_id, name, email, phone, course, marks)
        )
        conn.commit()
        conn.close()
        return True   # add ho gaya
    except sqlite3.IntegrityError:
        # Ye tab hota hai jab same student_id pehle se hai
        conn.close()
        return False  # add nahi hua


def get_all_students():
    # Sare students ki list nikalna
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()
    return data


def get_student(student_id):
    # Ek student ko uski ID se dhundna
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    data = cur.fetchone()
    conn.close()
    return data


def update_student(student_id, name, email, phone, course, marks):
    # Student ki details update karna
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students
        SET name=?, email=?, phone=?, course=?, marks=?
        WHERE student_id=?
    """, (name, email, phone, course, marks, student_id))
    conn.commit()
    changed = cur.rowcount   # kitne row update huye
    conn.close()
    return changed > 0


def delete_student(student_id):
    # Student ko delete karna
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    changed = cur.rowcount
    conn.close()
    return changed > 0
