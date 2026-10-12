"""
sample_data.py

Ye file kuch demo students database me daal deti hai,
taki tum turant test kar sako.

Run: python sample_data.py
"""

import database

demo_students = [
    (101, "Aarav Sharma", "aarav@example.com", "9876543210", "Computer Science", 88.5),
    (102, "Priya Verma", "priya@example.com", "9123456780", "Information Technology", 92.0),
    (103, "Rohan Gupta", "rohan@example.com", "9988776655", "Mechanical", 74.25),
    (104, "Sneha Iyer", "sneha@example.com", "9012345678", "Electronics", 65.0),
    (105, "Karan Mehta", "karan@example.com", "9765432109", "Computer Science", 55.5),
]

database.create_table()

for s in demo_students:
    added = database.add_student(*s)
    if added:
        print("Added:", s[1])
    else:
        print("Pehle se hai:", s[1])

print("\nDemo data ready hai! Ab 'python main.py' chalao.")
