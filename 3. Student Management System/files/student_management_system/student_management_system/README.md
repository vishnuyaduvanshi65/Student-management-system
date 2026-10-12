# Student Management System (Python + SQLite)

A simple, beginner-friendly, console-based Student Management System built
with **pure Python** and **SQLite**. No frameworks, no APIs, no external
libraries — just clean, readable code that performs the four core CRUD
operations: **Create, Read, Update, Delete**.

This project is intentionally kept small and focused so every line can be
explained confidently in a Software Associate / Junior Developer interview.

---

## 1. Folder Structure

```
student_management_system/
│
├── main.py            # Entry point - menu UI, input validation, program flow
├── database.py         # All SQLite database operations (CRUD functions)
├── sample_data.py       # Optional script to pre-load sample students
├── students.db         # SQLite database file (auto-created on first run)
└── README.md            # Project documentation (this file)
```

**Why separate `database.py` from `main.py`?**
This is called **separation of concerns**. `main.py` only worries about
talking to the user (menus, input, printing). `database.py` only worries
about talking to SQLite (SQL queries). If you ever wanted to swap SQLite
for another database, you would only need to change `database.py` — the
menu code wouldn't need to change at all.

---

## 2. Database Design

**Database name:** `students.db`
**Table name:** `students`

| Column      | Type    | Constraint     |
|-------------|---------|----------------|
| student_id  | INTEGER | PRIMARY KEY    |
| name        | TEXT    | NOT NULL       |
| email       | TEXT    | NOT NULL       |
| phone       | TEXT    | NOT NULL       |
| course      | TEXT    | NOT NULL       |
| marks       | REAL    | NOT NULL (0-100, validated in Python) |

SQL used to create the table:

```sql
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,
    phone      TEXT NOT NULL,
    course     TEXT NOT NULL,
    marks      REAL NOT NULL
);
```

The table is created automatically the first time you run `main.py` — you
don't need to set anything up manually.

---

## 3. Installation & How to Run

### Requirements
- Python 3.6 or higher (SQLite support — `sqlite3` — comes built into
  Python's standard library, so **no `pip install` is needed at all**).

### Steps

1. Download / copy the `student_management_system` folder onto your computer.
2. Open a terminal (Command Prompt / PowerShell / Terminal) inside that folder.
3. (Optional but recommended) Load sample test data:
   ```bash
   python sample_data.py
   ```
4. Run the main application:
   ```bash
   python main.py
   ```
5. Follow the on-screen menu to Add, View/Search, Update, or Delete students.
6. Choose option `5` to exit the program safely.

The database file `students.db` will appear in the same folder — you can
open it with any SQLite viewer (e.g. "DB Browser for SQLite") to inspect
the raw data if you like.

---

## 4. Sample Test Data

Running `python sample_data.py` inserts these records:

| ID  | Name          | Email                        | Phone       | Course                  | Marks |
|-----|---------------|------------------------------|-------------|--------------------------|-------|
| 101 | Aarav Sharma  | aarav.sharma@example.com     | 9876543210  | Computer Science         | 88.5  |
| 102 | Priya Verma   | priya.verma@example.com      | 9123456780  | Information Technology   | 92.0  |
| 103 | Rohan Gupta   | rohan.gupta@example.com      | 9988776655  | Mechanical Engineering   | 74.25 |
| 104 | Sneha Iyer    | sneha.iyer@example.com       | 9012345678  | Electronics              | 65.0  |
| 105 | Karan Mehta   | karan.mehta@example.com      | 9765432109  | Computer Science         | 55.5  |

You can safely run `sample_data.py` multiple times — it will skip any
student ID that already exists instead of creating duplicates.

---

## 5. Application Flow

```
START
  |
  v
Main Menu
  1. Add Student
  2. View/Search Student
  3. Update Student
  4. Delete Student
  5. Exit
  |
  v
Perform selected operation
  |
  v
Return to Main Menu  (loop)
  |
  v
Exit (choice 5)
```

Each operation is a self-contained function in `main.py`
(`add_student()`, `view_students()`, `update_student()`, `delete_student()`),
which calls the matching function in `database.py` to actually touch the
database.

---

## 6. Project Architecture — How Python Talks to SQLite

This project follows a simple **two-layer architecture**:

```
 ┌─────────────────────────┐
 │        main.py           │   <- Presentation / UI layer
 │  (menus, input, display)  │      Talks to the USER
 └────────────┬─────────────┘
              │  calls functions like
              │  insert_student(), get_student_by_id(), etc.
              v
 ┌─────────────────────────┐
 │      database.py         │   <- Data Access layer
 │  (SQL queries via sqlite3)│      Talks to the DATABASE
 └────────────┬─────────────┘
              │  uses Python's built-in
              │  sqlite3 module
              v
 ┌─────────────────────────┐
 │      students.db          │   <- SQLite database file on disk
 └─────────────────────────┘
```

**How the communication actually works, step by step:**

1. Python has a **built-in module called `sqlite3`** (no installation
   required) that implements the Python DB-API and knows how to read/write
   SQLite's file-based database format.
2. `sqlite3.connect("students.db")` opens (or creates) the database file and
   returns a **Connection** object — this is the "pipe" between your Python
   program and the database file.
3. From the connection, we get a **Cursor** object (`connection.cursor()`).
   The cursor is what actually **executes SQL statements** and fetches
   results.
4. We write SQL as a string with `?` placeholders (e.g.
   `"SELECT * FROM students WHERE student_id = ?"`) and pass the real values
   separately as a tuple: `cursor.execute(sql, (student_id,))`.
   This is called a **parameterized query** — SQLite safely inserts the
   value into the query, which prevents **SQL Injection** attacks.
5. For `SELECT` queries, we call `cursor.fetchone()` (one row) or
   `cursor.fetchall()` (all matching rows) to get the results back as
   Python tuples.
6. For `INSERT` / `UPDATE` / `DELETE` queries, we call `connection.commit()`
   to permanently save the changes to the `.db` file. Without `commit()`,
   changes would be lost.
7. Finally, we call `connection.close()` to release the database file so
   other programs (or the next function call) can safely use it.

In short: **Python code → sqlite3 module → SQL commands → students.db file
on disk**, and the results travel back the same path in reverse.

---

## 7. Key Features & Requirements Covered

- ✅ Add, View/Search, Update, Delete students (4 CRUD operations only)
- ✅ `student_id` is enforced as a unique PRIMARY KEY
- ✅ Marks are validated to be between 0 and 100
- ✅ Required fields cannot be left empty
- ✅ Basic email and phone format validation
- ✅ Graceful handling of invalid input (the program never crashes on bad
  input — it just re-prompts the user)
- ✅ Proper "student not found" messages for search/update/delete
- ✅ 100% parameterized SQL queries (no string-formatted SQL)
- ✅ Database logic (`database.py`) fully separated from UI logic (`main.py`)
- ✅ Commented code throughout

---

## 8. Interview Questions & Answers (Based on This Project)

**Q1. Why did you use SQLite instead of MySQL or PostgreSQL for this project?**
A: SQLite is a lightweight, file-based, serverless database that comes
built into Python's standard library (`sqlite3` module). For a small
project like this, it needs zero setup or installation — the entire
database is just one `.db` file — which makes it perfect for learning,
prototyping, and small desktop applications.

**Q2. What is a parameterized query, and why did you use it instead of
string formatting?**
A: A parameterized query uses placeholders (`?`) in the SQL string instead
of directly inserting variables. The actual values are passed separately to
`cursor.execute()`. This prevents **SQL Injection**, because SQLite treats
the passed values purely as data, never as executable SQL code — even if a
user enters something like `'; DROP TABLE students; --`.

**Q3. Why is `student_id` the PRIMARY KEY, and what does that enforce?**
A: PRIMARY KEY guarantees two things automatically: the value must be
**unique** across all rows, and it **cannot be NULL**. This matches the
requirement that every student must have one, unique ID, and it lets
SQLite reject duplicate inserts for us (we catch that as a
`sqlite3.IntegrityError` in `insert_student()`).

**Q4. What is the difference between `cursor.fetchone()` and
`cursor.fetchall()`?**
A: `fetchone()` returns a single matching row (or `None` if there isn't
one) — used when we search by student_id since IDs are unique. `fetchall()`
returns a list of all matching rows — used when we display every student
in the table.

**Q5. Why do you call `connection.commit()` after INSERT/UPDATE/DELETE but
not after SELECT?**
A: `commit()` permanently saves changes made to the database file. SELECT
statements don't change any data — they only read it — so there's nothing
to save, and calling commit() would have no effect.

**Q6. How did you separate concerns in this project, and why does that
matter?**
A: `database.py` contains only database/SQL logic, and `main.py` contains
only the menu, user input, and display logic. This is a simplified version
of a layered architecture. It matters because it makes the code easier to
test, easier to read, and easier to change — for example, we could swap
SQLite for another database by editing only `database.py`.

**Q7. How do you prevent the program from crashing when a user enters
invalid input (e.g. text instead of a number)?**
A: Every input field has its own validation function (e.g.
`get_valid_integer()`, `get_valid_marks()`) that loops with a `try/except`
or a condition check until valid input is given. This means bad input
never reaches the database layer, and the program never throws an
unhandled exception.

**Q8. How does your program handle the case when a student ID is not
found during search, update, or delete?**
A: `database.get_student_by_id()` returns `None` if no row matches. In
`main.py`, every operation checks `if row is None`/`if not row` first and
prints a clear "No student found with ID X" message instead of proceeding,
so there's never a crash or silent failure.

**Q9. Why did marks validation happen in Python instead of as a database
CHECK constraint?**
A: SQLite does support CHECK constraints, and that would also be a valid
approach. Here, I chose to validate in Python (`0 <= marks <= 100`) so I
could give the user a friendly, immediate re-prompt message rather than
catching a database-level constraint error. In a larger production system,
I'd typically use both — a database constraint as a safety net, plus
application-level validation for good user experience.

**Q10. What would you change if this project needed to support multiple
users accessing the database at the same time (concurrency)?**
A: SQLite handles light concurrent access but isn't designed for many
simultaneous writers, since it locks the whole database file during
writes. For a true multi-user system, I would migrate to a
client-server database like PostgreSQL or MySQL, keep the same layered
architecture (only `database.py` would change), and likely wrap the
console UI in a proper GUI or web interface.

---

## 9. Notes

This project deliberately does **not** include authentication, dashboards,
attendance tracking, APIs, or AI features — it is scoped tightly to the
four CRUD operations so it stays simple to explain end-to-end in an
interview.
