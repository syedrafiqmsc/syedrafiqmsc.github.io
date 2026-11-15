
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# DATABASE CONNECTION
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="chatbot"
)

cur = con.cursor()

# DISPLAY STUDENTS
def show_students():
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    print("\nSTUDENT DETAILS")
    print("-" * 65)

    for row in rows:
        print(row)

# ADD STUDENT
def add_student():
    sid = int(input("Student ID: "))
    name = input("Student Name: ")
    cls = input("Class: ")
    gender = input("Gender: ")

    sql = "INSERT INTO students VALUES (%s,%s,%s,%s)"
    cur.execute(sql, (sid, name, cls, gender))
    con.commit()

    print("Student added successfully")

# RECORD CHATBOT USAGE
def add_usage():
    uid = int(input("Usage ID: "))
    sid = int(input("Student ID: "))
    bot = input("Chatbot Name: ")
    hours = float(input("Usage Hours: "))
    frequency = input("Frequency (Daily/Weekly): ")
    purpose = input("Purpose: ")

    sql = "INSERT INTO chatbot_usage VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (uid, sid, bot, hours, frequency, purpose))
    con.commit()

    print("Usage record added")

# ADD LEARNING PREFERENCE
def add_preference():
    pid = int(input("Preference ID: "))
    sid = int(input("Student ID: "))
    method = input("Learning Method: ")
    subject = input("Subject: ")

    sql = "INSERT INTO preferences VALUES (%s,%s,%s,%s)"
    cur.execute(sql, (pid, sid, method, subject))
    con.commit()

    print("Preference added successfully")

# ADD STUDENT FEEDBACK
def add_feedback():
    fid = int(input("Feedback ID: "))
    sid = int(input("Student ID: "))
    benefit = input("Learning Benefit: ")
    rating = int(input("Satisfaction (1-5): "))
    comments = input("Comments: ")

    sql = "INSERT INTO feedback VALUES (%s,%s,%s,%s,%s)"
    cur.execute(sql, (fid, sid, benefit, rating, comments))
    con.commit()

    print("Feedback added successfully")

# DISPLAY USAGE REPORT
def usage_report():
    query = """
    SELECT s.student_name, u.chatbot_name,
    u.usage_hours, u.usage_frequency, u.purpose
    FROM students s
    JOIN chatbot_usage u
    ON s.student_id=u.student_id
    """

    cur.execute(query)
    rows = cur.fetchall()

    print("\nCHATBOT USAGE REPORT")
    print("-" * 75)

    for row in rows:
        print(row)

# DISPLAY PREFERENCES
def preference_report():
    query = """
    SELECT s.student_name,p.learning_method,p.subject
    FROM students s
    JOIN preferences p
    ON s.student_id=p.student_id
    """

    cur.execute(query)

    print("\nLEARNING PREFERENCES")

    for row in cur.fetchall():
        print(row)

# DISPLAY FEEDBACK
def feedback_report():
    query = """
    SELECT s.student_name,f.learning_benefit,
    f.satisfaction,f.comments
    FROM students s
    JOIN feedback f
    ON s.student_id=f.student_id
    """

    cur.execute(query)

    print("\nSTUDENT FEEDBACK")

    for row in cur.fetchall():
        print(row)

# ANALYSIS USING PANDAS
def analysis():
    query = """
    SELECT chatbot_name,usage_hours,usage_frequency
    FROM chatbot_usage
    """

    df = pd.read_sql(query, con)

    print("\nCHATBOT USAGE ANALYSIS")
    print(df)

    print("\nCHATBOT WISE USAGE")
    print(df.groupby("chatbot_name")["usage_hours"].sum())

    print("\nFREQUENCY ANALYSIS")
    print(df["usage_frequency"].value_counts())

    print("\nAVERAGE USAGE HOURS")
    print(df["usage_hours"].mean())

    # CHART 1: CHATBOT USAGE
    bot = df.groupby("chatbot_name")["usage_hours"].sum()

    bot.plot(kind="bar", title="Chatbot Usage Hours")
    plt.xlabel("Chatbot Name")
    plt.ylabel("Usage Hours")
    plt.tight_layout()
    plt.show()

    # CHART 2: USAGE FREQUENCY
    freq = df["usage_frequency"].value_counts()

    freq.plot(kind="bar", title="Usage Frequency")
    plt.xlabel("Frequency")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.show()

    # CHART 3: LEARNING PURPOSE
    query = """
    SELECT purpose,COUNT(*) AS total
    FROM chatbot_usage
    GROUP BY purpose
    """

    purpose_df = pd.read_sql(query, con)

    purpose_df.plot(
        x="purpose",
        y="total",
        kind="bar",
        legend=False,
        title="Purpose of Chatbot Usage"
    )

    plt.xlabel("Learning Purpose")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.show()

# SATISFACTION ANALYSIS
def satisfaction_analysis():
    query = """
    SELECT satisfaction,COUNT(*) AS total
    FROM feedback
    GROUP BY satisfaction
    ORDER BY satisfaction
    """

    df = pd.read_sql(query, con)

    print("\nSATISFACTION ANALYSIS")
    print(df)

    df.plot(
        x="satisfaction",
        y="total",
        kind="bar",
        legend=False,
        title="Student Satisfaction"
    )

    plt.xlabel("Rating")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.show()

# SEARCH STUDENT
def search_student():
    sid = int(input("Enter Student ID: "))

    cur.execute(
        "SELECT * FROM students WHERE student_id=%s",
        (sid,)
    )

    row = cur.fetchone()

    if row:
        print("Student Found:", row)
    else:
        print("Student not found")

# DELETE STUDENT
def delete_student():
    sid = int(input("Enter Student ID: "))

    cur.execute(
        "DELETE FROM feedback WHERE student_id=%s",
        (sid,)
    )

    cur.execute(
        "DELETE FROM preferences WHERE student_id=%s",
        (sid,)
    )

    cur.execute(
        "DELETE FROM chatbot_usage WHERE student_id=%s",
        (sid,)
    )

    cur.execute(
        "DELETE FROM students WHERE student_id=%s",
        (sid,)
    )

    con.commit()

    print("Student records deleted")

# MAIN MENU
while True:

    print("\n================================")
    print(" AI CHATBOT LEARNING ANALYSIS")
    print("================================")
    print("1. Display Students")
    print("2. Add Student")
    print("3. Record Chatbot Usage")
    print("4. Add Learning Preference")
    print("5. Add Student Feedback")
    print("6. Chatbot Usage Report")
    print("7. Learning Preferences")
    print("8. Student Feedback")
    print("9. Pandas Analysis and Charts")
    print("10. Satisfaction Analysis")
    print("11. Search Student")
    print("12. Delete Student")
    print("13. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        show_students()

    elif choice == "2":
        add_student()

    elif choice == "3":
        add_usage()

    elif choice == "4":
        add_preference()

    elif choice == "5":
        add_feedback()

    elif choice == "6":
        usage_report()

    elif choice == "7":
        preference_report()

    elif choice == "8":
        feedback_report()

    elif choice == "9":
        analysis()

    elif choice == "10":
        satisfaction_analysis()

    elif choice == "11":
        search_student()

    elif choice == "12":
        delete_student()

    elif choice == "13":
        print("Thank you for using the project")
        break

    else:
        print("Invalid choice")

cur.close()
con.close()
print("Database connection closed")
