"""
database.py
-------------
This file handles ALL communication with the SQLite database.
Keeping database code separate from the menu/UI code (main.py) makes the
project easier to read, test, and explain in an interview.

Every function here does ONE job:
    - connect to the database
    - create the table (if needed)
    - insert / read / update / delete a student row

We always use PARAMETERIZED QUERIES (the "?" placeholders) instead of
building SQL strings with Python f-strings. This prevents SQL Injection
attacks and is considered a best practice even in beginner projects.
"""

import sqlite3

DB_NAME = "students.db"


def create_connection():
    """
    Creates and returns a connection object to the SQLite database.
    If the file 'students.db' does not exist, SQLite creates it automatically.
    """
    connection = sqlite3.connect(DB_NAME)
    return connection


def create_table():
    """
    Creates the 'students' table if it does not already exist.
    This function is safe to call every time the program starts.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            email      TEXT NOT NULL,
            phone      TEXT NOT NULL,
            course     TEXT NOT NULL,
            marks      REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def insert_student(student_id, name, email, phone, course, marks):
    """
    Inserts a new student record into the database.
    Returns True if successful, False if the student_id already exists.
    """
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (student_id, name, email, phone, course, marks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, name, email, phone, course, marks))
        connection.commit()
        success = True
    except sqlite3.IntegrityError:
        # This error happens when student_id (PRIMARY KEY) already exists
        success = False
    finally:
        connection.close()

    return success


def get_all_students():
    """
    Returns a list of all student rows in the table.
    Each row is a tuple: (student_id, name, email, phone, course, marks)
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students ORDER BY student_id")
    rows = cursor.fetchall()

    connection.close()
    return rows


def get_student_by_id(student_id):
    """
    Returns a single student row matching the given student_id,
    or None if no student is found.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()

    connection.close()
    return row


def update_student(student_id, name, email, phone, course, marks):
    """
    Updates an existing student's details.
    Returns True if a row was updated, False if no matching student_id existed.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, email = ?, phone = ?, course = ?, marks = ?
        WHERE student_id = ?
    """, (name, email, phone, course, marks, student_id))

    connection.commit()
    updated = cursor.rowcount > 0  # rowcount tells us how many rows changed
    connection.close()

    return updated


def delete_student(student_id):
    """
    Deletes a student record by student_id.
    Returns True if a row was deleted, False if no matching student_id existed.
    """
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    return deleted
