"""
sample_data.py
-------------
Optional helper script to quickly fill the database with sample students
for testing and demo purposes.

Run it once with:
    python sample_data.py
"""

import database

sample_students = [
    (101, "Aarav Sharma",   "aarav.sharma@example.com",   "9876543210", "Computer Science", 88.5),
    (102, "Priya Verma",    "priya.verma@example.com",    "9123456780", "Information Technology", 92.0),
    (103, "Rohan Gupta",    "rohan.gupta@example.com",    "9988776655", "Mechanical Engineering", 74.25),
    (104, "Sneha Iyer",     "sneha.iyer@example.com",     "9012345678", "Electronics", 65.0),
    (105, "Karan Mehta",    "karan.mehta@example.com",    "9765432109", "Computer Science", 55.5),
]

def load_sample_data():
    database.create_table()
    added = 0
    skipped = 0

    for student in sample_students:
        success = database.insert_student(*student)
        if success:
            added += 1
        else:
            skipped += 1  # already exists

    print(f"Sample data load complete. Added: {added}, Skipped (already exist): {skipped}")


if __name__ == "__main__":
    load_sample_data()
