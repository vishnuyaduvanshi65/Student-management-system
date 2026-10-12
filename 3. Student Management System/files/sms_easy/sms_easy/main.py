"""
main.py

Ye hai humara MAIN program. Isko run karke menu khulega.
Command: python main.py
"""

import database


def add_student_menu():
    print("\n--- Add Student ---")

    # Student ID number hi honi chahiye
    while True:
        sid = input("Student ID: ")
        if sid.isdigit():
            sid = int(sid)
            break
        print("ID sirf number me daalo!")

    # Check karo ID pehle se to nahi hai
    if database.get_student(sid):
        print("Ye ID pehle se hai! Alag ID try karo.")
        return

    name = input("Name: ")
    while name.strip() == "":
        name = input("Name khali nahi ho sakta, phir se daalo: ")

    email = input("Email: ")
    phone = input("Phone: ")
    course = input("Course: ")

    # Marks 0 se 100 ke beech honi chahiye
    while True:
        try:
            marks = float(input("Marks (0-100): "))
            if 0 <= marks <= 100:
                break
            print("Marks 0 se 100 ke beech honi chahiye!")
        except ValueError:
            print("Sahi number daalo!")

    ok = database.add_student(sid, name, email, phone, course, marks)
    if ok:
        print("Student add ho gaya!")
    else:
        print("Kuch gadbad hui, add nahi hua.")


def view_students_menu():
    print("\n--- View / Search ---")
    print("1. Sab students dekho")
    print("2. ID se search karo")
    ch = input("Choice: ")

    if ch == "1":
        all_students = database.get_all_students()
        if len(all_students) == 0:
            print("Koi student nahi mila.")
        else:
            for s in all_students:
                show_student(s)

    elif ch == "2":
        sid = input("Student ID daalo: ")
        if sid.isdigit():
            student = database.get_student(int(sid))
            if student:
                show_student(student)
            else:
                print("Ye ID nahi mili.")
        else:
            print("Sahi ID number daalo.")
    else:
        print("Galat choice.")


def show_student(s):
    # s ek tuple hai: (id, name, email, phone, course, marks)
    print("------------------------")
    print("ID     :", s[0])
    print("Name   :", s[1])
    print("Email  :", s[2])
    print("Phone  :", s[3])
    print("Course :", s[4])
    print("Marks  :", s[5])
    print("------------------------")


def update_student_menu():
    print("\n--- Update Student ---")
    sid = input("Kis Student ki ID update karni hai: ")

    if not sid.isdigit():
        print("Sahi ID number daalo.")
        return

    sid = int(sid)
    student = database.get_student(sid)

    if not student:
        print("Ye ID nahi mili.")
        return

    print("\nAbhi ki details:")
    show_student(student)

    print("\nNayi details daalo (khali chodo agar change nahi karna):")

    name = input(f"Name [{student[1]}]: ") or student[1]
    email = input(f"Email [{student[2]}]: ") or student[2]
    phone = input(f"Phone [{student[3]}]: ") or student[3]
    course = input(f"Course [{student[4]}]: ") or student[4]

    marks_input = input(f"Marks [{student[5]}]: ")
    if marks_input == "":
        marks = student[5]
    else:
        try:
            marks = float(marks_input)
            if not (0 <= marks <= 100):
                print("Marks 0-100 ke beech honi chahiye. Update cancel.")
                return
        except ValueError:
            print("Galat marks value. Update cancel.")
            return

    ok = database.update_student(sid, name, email, phone, course, marks)
    if ok:
        print("Update ho gaya!")
    else:
        print("Update nahi hua.")


def delete_student_menu():
    print("\n--- Delete Student ---")
    sid = input("Kis Student ki ID delete karni hai: ")

    if not sid.isdigit():
        print("Sahi ID number daalo.")
        return

    sid = int(sid)
    student = database.get_student(sid)

    if not student:
        print("Ye ID nahi mili.")
        return

    print("\nYe student delete hoga:")
    show_student(student)

    confirm = input("Pakka delete karna hai? (y/n): ").lower()
    if confirm == "y":
        database.delete_student(sid)
        print("Student delete ho gaya.")
    else:
        print("Delete cancel kar diya.")


def main():
    database.create_table()  # table bana lo agar nahi hai

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View/Search Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = input("Apna choice daalo (1-5): ")

        if choice == "1":
            add_student_menu()
        elif choice == "2":
            view_students_menu()
        elif choice == "3":
            update_student_menu()
        elif choice == "4":
            delete_student_menu()
        elif choice == "5":
            print("Bye bye! Program band ho raha hai.")
            break
        else:
            print("Galat choice, 1-5 me se koi ek daalo.")


if __name__ == "__main__":
    main()
