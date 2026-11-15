
# SOCIAL MEDIA USAGE AND DIGITAL ADDICTION ANALYSIS

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. MYSQL CONNECTION

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="socialmedia"
)

cur = con.cursor()

print("DATABASE CONNECTED SUCCESSFULLY")


# 2. GET DATA FROM MYSQL

def get_data(q):
    cur.execute(q)
    data = cur.fetchall()
    columns = [i[0] for i in cur.description]
    return pd.DataFrame(data, columns=columns)


# 3. DISPLAY STUDENTS

def show_students():
    df = get_data("SELECT * FROM students")
    print(df.to_string(index=False))


# 4. DISPLAY PLATFORMS

def show_platforms():
    df = get_data("SELECT * FROM platforms")
    print(df.to_string(index=False))


# 5. DISPLAY USAGE RECORDS

def show_usage():
    q = """SELECT s.student_name,p.platform_name,
           u.usage_date,u.screen_hours,u.daily_sessions
           FROM usage_records u
           JOIN students s ON u.student_id=s.student_id
           JOIN platforms p ON u.platform_id=p.platform_id"""
    df = get_data(q)
    print(df.to_string(index=False))


# 6. DISPLAY WELLBEING

def show_wellbeing():
    q = """SELECT s.student_name,w.sleep_hours,
           w.study_hours,w.concentration
           FROM wellbeing w
           JOIN students s ON w.student_id=s.student_id"""
    df = get_data(q)
    print(df.to_string(index=False))


# 7. PLATFORM WISE USAGE

def platform_usage():
    q = """SELECT p.platform_name,
           SUM(u.screen_hours) AS Total_Hours
           FROM platforms p
           JOIN usage_records u
           ON p.platform_id=u.platform_id
           GROUP BY p.platform_id,p.platform_name"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="platform_name",y="Total_Hours",
            kind="bar",legend=False)
    plt.title("Platform Wise Screen Time")
    plt.xlabel("Social Media Platforms")
    plt.ylabel("Total Hours")
    plt.tight_layout()
    plt.show()


# 8. STUDENT SCREEN TIME

def student_usage():
    q = """SELECT s.student_name,
           SUM(u.screen_hours) AS Total_Hours
           FROM students s JOIN usage_records u
           ON s.student_id=u.student_id
           GROUP BY s.student_id,s.student_name
           ORDER BY Total_Hours DESC"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="student_name",y="Total_Hours",
            kind="bar",legend=False)
    plt.title("Student Wise Screen Time")
    plt.xlabel("Students")
    plt.ylabel("Hours")
    plt.tight_layout()
    plt.show()


# 9. SLEEP HOURS ANALYSIS

def sleep_analysis():
    q = """SELECT s.student_name,w.sleep_hours
           FROM students s JOIN wellbeing w
           ON s.student_id=w.student_id"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="student_name",y="sleep_hours",
            kind="bar",legend=False)
    plt.title("Student Sleep Hours")
    plt.xlabel("Students")
    plt.ylabel("Sleep Hours")
    plt.tight_layout()
    plt.show()


# 10. STUDY HOURS ANALYSIS

def study_analysis():
    q = """SELECT s.student_name,w.study_hours
           FROM students s JOIN wellbeing w
           ON s.student_id=w.student_id"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="student_name",y="study_hours",
            kind="bar",legend=False)
    plt.title("Student Study Hours")
    plt.xlabel("Students")
    plt.ylabel("Study Hours")
    plt.tight_layout()
    plt.show()


# 11. DAILY SCREEN TIME ANALYSIS

def daily_analysis():
    q = """SELECT usage_date,
           SUM(screen_hours) AS Total_Hours
           FROM usage_records
           GROUP BY usage_date
           ORDER BY usage_date"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="usage_date",y="Total_Hours",
            kind="line",marker="o",legend=False)
    plt.title("Daily Social Media Usage")
    plt.xlabel("Date")
    plt.ylabel("Total Hours")
    plt.tight_layout()
    plt.show()


# 12. HIGH SCREEN TIME STUDENTS

def high_usage():
    q = """SELECT s.student_name,
           SUM(u.screen_hours) AS Total_Hours
           FROM students s JOIN usage_records u
           ON s.student_id=u.student_id
           GROUP BY s.student_id,s.student_name
           HAVING Total_Hours>3
           ORDER BY Total_Hours DESC"""
    df = get_data(q)
    print(df.to_string(index=False))


# 13. DISPLAY ALL REPORTS

def all_reports():
    show_students()
    show_platforms()
    show_usage()
    show_wellbeing()
    platform_usage()
    student_usage()
    sleep_analysis()
    study_analysis()
    daily_analysis()
    high_usage()


# 14. MAIN MENU

def main_menu():

    while True:

        print("\n" + "=" * 45)
        print(" SOCIAL MEDIA USAGE ANALYSIS SYSTEM")
        print("=" * 45)

        print("1. Display Students")
        print("2. Display Platforms")
        print("3. Display Usage Records")
        print("4. Display Digital Wellbeing")
        print("5. Platform Wise Usage")
        print("6. Student Screen Time")
        print("7. Sleep Hours Analysis")
        print("8. Study Hours Analysis")
        print("9. Daily Screen Time Analysis")
        print("10. High Screen Time Students")
        print("11. Display All Reports")
        print("0. Exit")

        ch = input("\nEnter Your Choice: ")

        if ch == "1":
            show_students()

        elif ch == "2":
            show_platforms()

        elif ch == "3":
            show_usage()

        elif ch == "4":
            show_wellbeing()

        elif ch == "5":
            platform_usage()

        elif ch == "6":
            student_usage()

        elif ch == "7":
            sleep_analysis()

        elif ch == "8":
            study_analysis()

        elif ch == "9":
            daily_analysis()

        elif ch == "10":
            high_usage()

        elif ch == "11":
            all_reports()

        elif ch == "0":
            print("Thank You!")
            break

        else:
            print("Invalid Choice! Try Again.")


# 15. START PROGRAM

try:
    main_menu()

except Exception as e:
    print("Error:", e)

finally:
    if con.is_connected():
        cur.close()
        con.close()
        print("Database Connection Closed")
