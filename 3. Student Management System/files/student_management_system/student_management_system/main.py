"""
main.py
-------------
This is the entry point of the Student Management System.
It shows a text menu, takes user input, validates it, and calls the
functions in database.py to actually talk to the SQLite database.

Run this file to start the program:
    python main.py
"""

import database


# ---------------------------------------------------------------------------
# INPUT HELPER / VALIDATION FUNCTIONS
# Keeping validation in small reusable functions keeps the menu functions
# clean and avoids repeating the same "while True: try/except" code everywhere.
# ---------------------------------------------------------------------------

def get_non_empty_string(prompt):
    """Keeps asking until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_valid_email(prompt):
    """Very simple email validation: must contain '@' and '.' """
    while True:
        value = input(prompt).strip()
        if "@" in value and "." in value and len(value) >= 5:
            return value
        print("Please enter a valid email address (e.g. name@example.com).")


def get_valid_phone(prompt):
    """Phone number must contain only digits and be 7-15 digits long."""
    while True:
        value = input(prompt).strip()
        if value.isdigit() and 7 <= len(value) <= 15:
            return value
        print("Please enter a valid phone number (digits only, 7-15 digits).")


def get_valid_integer(prompt):
    """Keeps asking until the user enters a valid whole number (for Student ID)."""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a valid numeric Student ID.")


def get_valid_marks(prompt):
    """Marks must be a number between 0 and 100 (inclusive)."""
    while True:
        value = input(prompt).strip()
        try:
            marks = float(value)
            if 0 <= marks <= 100:
                return marks
            else:
                print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number for marks.")


def get_yes_no(prompt):
    """Used for confirmation prompts (e.g. before deleting a student)."""
    while True:
        value = input(prompt).strip().lower()
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")


def print_student(row):
    """
    Nicely prints a single student row.
    row = (student_id, name, email, phone, course, marks)
    """
    print("-" * 40)
    print(f"Student ID : {row[0]}")
    print(f"Name       : {row[1]}")
    print(f"Email      : {row[2]}")
    print(f"Phone      : {row[3]}")
    print(f"Course     : {row[4]}")
    print(f"Marks      : {row[5]}")
    print("-" * 40)


# ---------------------------------------------------------------------------
# CRUD MENU FUNCTIONS
# ---------------------------------------------------------------------------

def add_student():
    """1. CREATE - Add a new student to the database."""
    print("\n--- Add New Student ---")

    student_id = get_valid_integer("Enter Student ID: ")

    # Check uniqueness up-front so we can give a clear message
    if database.get_student_by_id(student_id) is not None:
        print(f"A student with ID {student_id} already exists. Cannot add duplicate.")
        return

    name = get_non_empty_string("Enter Name: ")
    email = get_valid_email("Enter Email: ")
    phone = get_valid_phone("Enter Phone: ")
    course = get_non_empty_string("Enter Course: ")
    marks = get_valid_marks("Enter Marks (0-100): ")

    success = database.insert_student(student_id, name, email, phone, course, marks)

    if success:
        print(f"Student '{name}' added successfully!")
    else:
        print("Could not add student. Student ID may already exist.")


def view_students():
    """2. READ - View all students or search for one by Student ID."""
    print("\n--- View / Search Student ---")
    print("1. View All Students")
    print("2. Search Student by ID")
    choice = input("Choose an option (1-2): ").strip()

    if choice == "1":
        rows = database.get_all_students()
        if not rows:
            print("No students found in the database.")
        else:
            print(f"\nTotal Students: {len(rows)}")
            for row in rows:
                print_student(row)

    elif choice == "2":
        student_id = get_valid_integer("Enter Student ID to search: ")
        row = database.get_student_by_id(student_id)
        if row:
            print("\nStudent Found:")
            print_student(row)
        else:
            print(f"No student found with ID {student_id}.")

    else:
        print("Invalid choice. Returning to main menu.")


def update_student():
    """3. UPDATE - Search by ID, then update editable fields."""
    print("\n--- Update Student ---")
    student_id = get_valid_integer("Enter Student ID to update: ")

    row = database.get_student_by_id(student_id)
    if not row:
        print(f"No student found with ID {student_id}.")
        return

    print("\nCurrent Details:")
    print_student(row)

    print("\nEnter new details below.")
    print("(Press Enter without typing anything to keep the current value)\n")

    # For update, we allow "keep current value" by pressing Enter.
    # This is more user-friendly than forcing re-entry of every field.
    name = input(f"Name [{row[1]}]: ").strip() or row[1]
    email_input = input(f"Email [{row[2]}]: ").strip()
    email = email_input if email_input else row[2]
    phone_input = input(f"Phone [{row[3]}]: ").strip()
    phone = phone_input if phone_input else row[3]
    course = input(f"Course [{row[4]}]: ").strip() or row[4]
    marks_input = input(f"Marks [{row[5]}]: ").strip()
    marks = float(marks_input) if marks_input else row[5]

    # Basic validation even for the "changed" fields
    if email_input and ("@" not in email or "." not in email):
        print("Invalid email format. Update cancelled.")
        return
    if phone_input and not phone_input.isdigit():
        print("Invalid phone number. Update cancelled.")
        return
    if marks_input:
        try:
            marks = float(marks_input)
            if not (0 <= marks <= 100):
                print("Marks must be between 0 and 100. Update cancelled.")
                return
        except ValueError:
            print("Invalid marks value. Update cancelled.")
            return

    updated = database.update_student(student_id, name, email, phone, course, marks)

    if updated:
        print("Student record updated successfully!")
    else:
        print("Update failed. Student may have been deleted by another process.")


def delete_student():
    """4. DELETE - Search by ID, show details, confirm, then delete."""
    print("\n--- Delete Student ---")
    student_id = get_valid_integer("Enter Student ID to delete: ")

    row = database.get_student_by_id(student_id)
    if not row:
        print(f"No student found with ID {student_id}.")
        return

    print("\nStudent to be deleted:")
    print_student(row)

    confirm = get_yes_no("Are you sure you want to delete this student? (y/n): ")

    if confirm:
        deleted = database.delete_student(student_id)
        if deleted:
            print("Student deleted successfully.")
        else:
            print("Delete failed. Please try again.")
    else:
        print("Delete cancelled.")


# ---------------------------------------------------------------------------
# MAIN MENU LOOP
# ---------------------------------------------------------------------------

def main():
    # Make sure the table exists before the menu starts
    database.create_table()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View/Search Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            print("Thank you for using the Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


# This ensures main() only runs when this file is executed directly,
# not when it's imported by another script.
if __name__ == "__main__":
    main()
