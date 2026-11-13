
import mysql.connector
import matplotlib.pyplot as plt

# 1. Database Connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="stu"
)
cur = con.cursor()

# 2. Check Student Exists
def student_exists(adm):
    cur.execute("SELECT admission_no FROM students WHERE admission_no=%s", (adm,))
    return cur.fetchone() is not None

# 3. Add Student
def add_student():
    adm = input("Admission Number: ")
    name = input("Student Name: ")
    gender = input("Gender: ")
    cid = input("Class ID: ")

    cur.execute("INSERT INTO students (admission_no, student_name, gender, class_id) VALUES (%s,%s,%s,%s)", (adm, name, gender, cid))
    con.commit()
    print("Student Added Successfully!")

# 4. Display Students
def display_students():
    cur.execute("SELECT * FROM students")
    for row in cur.fetchall():
        print(row)

# 5. Search Student
def search_student():
    adm = input("Admission Number: ")

    cur.execute("SELECT * FROM students WHERE admission_no=%s", (adm,))
    row = cur.fetchone()

    if row:
        print(row)
    else:
        print("Student Not Found!")

# 6. Update Student
def update_student():
    adm = input("Admission Number: ")

    if student_exists(adm):
        name = input("New Student Name: ")
        cur.execute("UPDATE students SET student_name=%s WHERE admission_no=%s", (name, adm))
        con.commit()
        print("Student Updated!")
    else:
        print("Admission Number Does Not Exist!")

# 7. Delete Student
def delete_student():
    adm = input("Admission Number: ")

    if student_exists(adm):
        cur.execute("DELETE FROM students WHERE admission_no=%s", (adm,))
        con.commit()
        print("Student Deleted!")
    else:
        print("Admission Number Does Not Exist!")

# 8. Add Marks
def add_marks():
    adm = input("Admission Number: ")

    if student_exists(adm):
        sid = input("Subject ID: ")
        exam = input("Exam Name: ")
        marks = input("Marks Obtained: ")

        cur.execute("INSERT INTO marks (admission_no, subject_id, exam_name, marks_obtained) VALUES (%s,%s,%s,%s)", (adm, sid, exam, marks))
        con.commit()
        print("Marks Added!")
    else:
        print("Admission Number Does Not Exist!")

# 9. Add Attendance
def add_attendance():
    adm = input("Admission Number: ")

    if student_exists(adm):
        date = input("Date (YYYY-MM-DD): ")
        status = input("Present/Absent/Leave: ")

        cur.execute("INSERT INTO attendance (admission_no, attendance_date, status) VALUES (%s,%s,%s)", (adm, date, status))
        con.commit()
        print("Attendance Added!")
    else:
        print("Admission Number Does Not Exist!")

# 10. Student Marks Report
def student_report():
    adm = input("Admission Number: ")

    if student_exists(adm):
        cur.execute("SELECT * FROM marks WHERE admission_no=%s", (adm,))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No Marks Found!")
    else:
        print("Admission Number Does Not Exist!")

# 11. Attendance Report
def attendance_report():
    adm = input("Admission Number: ")

    if student_exists(adm):
        cur.execute("SELECT status, COUNT(*) FROM attendance WHERE admission_no=%s GROUP BY status", (adm,))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No Attendance Records Found!")
    else:
        print("Admission Number Does Not Exist!")


# 12. Student Marks Chart
def marks_chart():
    adm = input("Admission Number: ")

    if student_exists(adm):
        cur.execute("SELECT sub.subject_name, m.marks_obtained FROM marks m JOIN subjects sub ON m.subject_id=sub.subject_id WHERE m.admission_no=%s", (adm,))
        rows = cur.fetchall()

        if rows:
            subjects = [row[0] for row in rows]
            marks = [float(row[1]) for row in rows]

            # Bar Chart
            plt.figure()
            plt.bar(subjects, marks)
            plt.title("Student Marks - Bar Chart")
            plt.xlabel("Subjects")
            plt.ylabel("Marks")
            plt.ylim(0, 100)
            plt.show()

            # Line Chart
            plt.figure()
            plt.plot(subjects, marks, marker='o')
            plt.title("Student Marks - Line Chart")
            plt.xlabel("Subjects")
            plt.ylabel("Marks")
            plt.ylim(0, 100)
            plt.grid()
            plt.show()

            # Histogram
            plt.figure()
            plt.hist(marks, bins=5, edgecolor='black')
            plt.title("Student Marks - Histogram")
            plt.xlabel("Marks")
            plt.ylabel("Number of Subjects")
            plt.show()

        else:
            print("No Marks Found!")

    else:
        print("Admission Number Does Not Exist!")


# 13. Main Menu
while True:
    print("\nSTUDENT MANAGEMENT SYSTEM")
    print("1. Add Student")
    print("2. Display Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Add Marks")
    print("7. Add Attendance")
    print("8. Student Marks Report")
    print("9. Attendance Report")
    print("10. Student Marks Chart")
    print("0. Exit")

    choice = input("Enter Choice: ")

    try:
        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            add_marks()
        elif choice == "7":
            add_attendance()
        elif choice == "8":
            student_report()
        elif choice == "9":
            attendance_report()
        elif choice == "10":
            marks_chart()
        elif choice == "0":
            break
        else:
            print("Invalid Choice!")

    except Exception as e:
        con.rollback()
        print("Error:", e)

cur.close()
con.close()
print("Program Closed!")
