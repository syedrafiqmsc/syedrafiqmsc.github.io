
# CYBERCRIME AWARENESS AND ANALYSIS SYSTEM
# Database: crime
# Password: tiger

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# CONNECT TO MYSQL DATABASE

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="crime"
)

cur = con.cursor()

# 1. DISPLAY ALL CYBERCRIME INCIDENTS

def display_incidents():
    query = """
    SELECT i.incident_id, c.category_name,
           i.incident_date, i.state,
           i.loss_amount, i.case_status
    FROM incidents i
    JOIN categories c
    ON i.category_id = c.category_id
    ORDER BY i.incident_id
    """
    df = pd.read_sql_query(query, con)
    print("\nCYBERCRIME INCIDENT DETAILS")
    print(df.to_string(index=False))


# 2. ADD NEW CYBERCRIME INCIDENT

def add_incident():
    try:
        print("\nAVAILABLE CYBERCRIME CATEGORIES")
        cur.execute("SELECT * FROM categories")
        for row in cur.fetchall():
            print(row)

        iid = int(input("Enter Incident ID: "))
        cid = int(input("Enter Category ID: "))
        date = input("Enter Date (YYYY-MM-DD): ")
        state = input("Enter State: ")
        loss = float(input("Enter Financial Loss: "))
        status = input("Enter Case Status: ")

        query = """
        INSERT INTO incidents
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cur.execute(query, (iid, cid, date,
                            state, loss, status))
        con.commit()

        print("Incident added successfully!")

    except mysql.connector.Error as e:
        con.rollback()
        print("Database Error:", e)
    except ValueError:
        print("Invalid input. Please enter correct values.")


# 3. DISPLAY CATEGORY-WISE CRIME STATISTICS

def category_analysis():
    query = """
    SELECT c.category_name,
           COUNT(i.incident_id) AS total_incidents
    FROM categories c
    LEFT JOIN incidents i
    ON c.category_id = i.category_id
    GROUP BY c.category_id, c.category_name
    ORDER BY c.category_id
    """
    df = pd.read_sql_query(query, con)
    print("\nCATEGORY-WISE CRIME ANALYSIS")
    print(df.to_string(index=False))


# 4. BAR CHART - CATEGORY-WISE CRIMES

def bar_chart():
    query = """
    SELECT c.category_name,
           COUNT(i.incident_id) AS total
    FROM categories c
    LEFT JOIN incidents i
    ON c.category_id = i.category_id
    GROUP BY c.category_id, c.category_name
    """
    df = pd.read_sql_query(query, con)

    plt.figure(figsize=(10, 5))
    plt.bar(df["category_name"], df["total"])
    plt.title("Category-wise Cybercrime Incidents")
    plt.xlabel("Cybercrime Category")
    plt.ylabel("Number of Incidents")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# 5. LINE CHART - MONTHLY CRIME REPORTS

def line_chart():
    query = """
    SELECT DATE_FORMAT(incident_date, '%Y-%m') AS month,
           COUNT(*) AS total
    FROM incidents
    GROUP BY DATE_FORMAT(incident_date, '%Y-%m')
    ORDER BY month
    """
    df = pd.read_sql_query(query, con)

    plt.figure(figsize=(9, 5))
    plt.plot(df["month"], df["total"],
             marker="o", linewidth=2)
    plt.title("Monthly Cybercrime Incidents")
    plt.xlabel("Month")
    plt.ylabel("Number of Incidents")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 6. HISTOGRAM - FINANCIAL LOSS

def histogram():
    query = """
    SELECT loss_amount FROM incidents
    """
    df = pd.read_sql_query(query, con)

    plt.figure(figsize=(8, 5))
    plt.hist(df["loss_amount"], bins=5,
             edgecolor="black")
    plt.title("Distribution of Financial Loss")
    plt.xlabel("Financial Loss (Rupees)")
    plt.ylabel("Number of Incidents")
    plt.tight_layout()
    plt.show()


# 7. DISPLAY AWARENESS TIPS

def awareness_tips():
    query = """
    SELECT tip_id, tip_title, tip_description
    FROM awareness_tips
    """
    df = pd.read_sql_query(query, con)

    print("\nONLINE SAFETY AWARENESS TIPS")
    print(df.to_string(index=False))


# 8. TOTAL FINANCIAL LOSS

def total_loss():
    cur.execute(
        "SELECT SUM(loss_amount) FROM incidents"
    )
    result = cur.fetchone()[0]

    print("\nTOTAL FINANCIAL LOSS: Rs.",
          result if result is not None else 0)


# 9. CASE STATUS ANALYSIS

def case_analysis():
    query = """
    SELECT case_status, COUNT(*) AS total_cases
    FROM incidents
    GROUP BY case_status
    """
    df = pd.read_sql_query(query, con)

    print("\nCASE STATUS ANALYSIS")
    print(df.to_string(index=False))


# MAIN MENU

while True:
    print("\n================================")
    print(" CYBERCRIME AWARENESS SYSTEM")
    print("================================")
    print("1. Display All Incidents")
    print("2. Add New Incident")
    print("3. Category-wise Crime Analysis")
    print("4. Bar Chart")
    print("5. Line Chart")
    print("6. Histogram")
    print("7. Online Safety Awareness Tips")
    print("8. Total Financial Loss")
    print("9. Case Status Analysis")
    print("10. Exit")

    try:
        choice = int(input("\nEnter Your Choice: "))

        if choice == 1:
            display_incidents()

        elif choice == 2:
            add_incident()

        elif choice == 3:
            category_analysis()

        elif choice == 4:
            bar_chart()

        elif choice == 5:
            line_chart()

        elif choice == 6:
            histogram()

        elif choice == 7:
            awareness_tips()

        elif choice == 8:
            total_loss()

        elif choice == 9:
            case_analysis()

        elif choice == 10:
            print("Thank you for using the system!")
            break

        else:
            print("Invalid Choice!")

    except ValueError:
        print("Please enter a valid menu number.")

cur.close()
con.close()
