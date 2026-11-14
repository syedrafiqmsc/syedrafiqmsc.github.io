
# EMPLOYEE PAYROLL MANAGEMENT SYSTEM
# Python + MySQL + Matplotlib

import mysql.connector
import matplotlib.pyplot as plt

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="emp"
)

cur = con.cursor()


# 1. ADD EMPLOYEE
def add_employee():
    eid = int(input("Employee ID: "))
    name = input("Employee Name: ")
    gender = input("Gender: ")
    dept = input("Department: ")
    desig = input("Designation: ")
    mobile = input("Mobile Number: ")

    sql = "INSERT INTO employees VALUES (%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (eid, name, gender, dept, desig, mobile))
    con.commit()

    print("Employee Added Successfully!")


# 2. VIEW EMPLOYEES
def view_employees():
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()

    print("\nEMPLOYEE DETAILS")
    for row in rows:
        print(row)


# 3. CALCULATE AND SAVE SALARY
def calculate_salary():
    sid = int(input("Salary ID: "))
    eid = int(input("Employee ID: "))
    month = input("Pay Month (YYYY-MM-DD): ")

    basic = float(input("Basic Salary: "))
    hra = float(input("HRA: "))
    da = float(input("DA: "))
    allowance = float(input("Other Allowances: "))

    pf = float(input("PF: "))
    tax = float(input("Tax: "))
    deduction = float(input("Other Deductions: "))

    gross = basic + hra + da + allowance
    total_ded = pf + tax + deduction
    net = gross - total_ded

    sql = """INSERT INTO payroll VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    values = (sid, eid, month, basic, hra, da,
              allowance, pf, tax, deduction,
              gross, total_ded, net)

    cur.execute(sql, values)
    con.commit()

    print("\n===== SALARY SLIP =====")
    print("Gross Salary:", gross)
    print("Total Deductions:", total_ded)
    print("Net Salary:", net)
    print("Salary Saved Successfully!")


# 4. VIEW PAYROLL
def view_payroll():
    sql = """SELECT e.emp_name, p.pay_month,
             p.basic_salary, p.gross_salary,
             p.total_deduction, p.net_salary
             FROM employees e
             JOIN payroll p ON e.emp_id=p.emp_id"""

    cur.execute(sql)
    rows = cur.fetchall()

    print("\nEMPLOYEE PAYROLL DETAILS")
    for row in rows:
        print(row)


# 5. SEARCH EMPLOYEE
def search_employee():
    eid = int(input("Enter Employee ID: "))

    cur.execute(
        "SELECT * FROM employees WHERE emp_id=%s",
        (eid,)
    )

    row = cur.fetchone()

    if row:
        print("Employee Details:", row)
    else:
        print("Employee Not Found!")


# 6. DISPLAY ALL THREE CHARTS
def display_charts():
    sql = """SELECT e.emp_name, p.net_salary
             FROM employees e
             JOIN payroll p ON e.emp_id=p.emp_id
             ORDER BY p.salary_id"""

    cur.execute(sql)
    rows = cur.fetchall()

    if not rows:
        print("No Salary Records Available!")
        return

    names = [row[0] for row in rows]
    salaries = [float(row[1]) for row in rows]

    # BAR CHART
    plt.figure(figsize=(8, 4))
    plt.bar(names, salaries)
    plt.title("Employee Net Salary - Bar Chart")
    plt.xlabel("Employee Name")
    plt.ylabel("Net Salary")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    # LINE CHART
    plt.figure(figsize=(8, 4))
    plt.plot(names, salaries, marker='o')
    plt.title("Employee Net Salary - Line Chart")
    plt.xlabel("Employee Name")
    plt.ylabel("Net Salary")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    # HISTOGRAM
    plt.figure(figsize=(8, 4))
    plt.hist(salaries, bins=5, edgecolor='black')
    plt.title("Employee Salary Distribution")
    plt.xlabel("Net Salary")
    plt.ylabel("Number of Employees")
    plt.tight_layout()
    plt.show()


# MAIN MENU
while True:

    print("\n===== EMPLOYEE PAYROLL MANAGEMENT SYSTEM =====")
    print("1. Add Employee")
    print("2. View Employees")
    print("3. Calculate and Save Salary")
    print("4. View Payroll")
    print("5. Search Employee")
    print("6. Display All Charts")
    print("7. Exit")

    choice = input("Enter Choice: ")

    try:

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            calculate_salary()

        elif choice == "4":
            view_payroll()

        elif choice == "5":
            search_employee()

        elif choice == "6":
            display_charts()

        elif choice == "7":
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")

    except mysql.connector.Error as err:
        con.rollback()
        print("Database Error:", err)

    except ValueError:
        print("Please Enter Valid Numeric Values!")

cur.close()
con.close()
