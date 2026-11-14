
import mysql.connector
import matplotlib.pyplot as plt

# Database Connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="upi"
)

cur = con.cursor()


# 1. Add Payment
def add_payment():
    tid = int(input("Transaction ID: "))
    cid = int(input("Customer ID: "))
    method = input("Payment Method: ")
    amount = float(input("Amount: "))
    date = input("Date (YYYY-MM-DD): ")
    status = input("Status (Success/Failed): ").title()

    sql = """INSERT INTO payments
    VALUES (%s,%s,%s,%s,%s,%s)"""

    cur.execute(sql, (tid, cid, method, amount, date, status))
    con.commit()

    print("Payment added successfully!")


# 2. Display Payments
def display_payments():
    cur.execute("""
    SELECT p.transaction_id, c.customer_name,
    p.payment_method, p.amount,
    p.transaction_date, p.status
    FROM payments p JOIN customers c
    ON p.customer_id=c.customer_id
    """)

    records = cur.fetchall()

    if records:
        for row in records:
            print(row)
    else:
        print("No payment records found!")


# 3. Search Payment
def search_payment():
    tid = int(input("Enter Transaction ID: "))

    cur.execute(
        "SELECT * FROM payments WHERE transaction_id=%s",
        (tid,)
    )

    row = cur.fetchone()

    if row:
        print(row)
    else:
        print("Transaction not found!")


# 4. Update Payment Status
def update_status():
    tid = int(input("Transaction ID: "))
    status = input("New Status (Success/Failed): ").title()

    cur.execute(
        "UPDATE payments SET status=%s WHERE transaction_id=%s",
        (status, tid)
    )

    con.commit()

    if cur.rowcount:
        print("Record updated successfully!")
    else:
        print("Transaction not found!")


# 5. Delete Payment
def delete_payment():
    tid = int(input("Transaction ID to delete: "))

    cur.execute(
        "DELETE FROM payments WHERE transaction_id=%s",
        (tid,)
    )

    con.commit()

    if cur.rowcount:
        print("Record deleted successfully!")
    else:
        print("Transaction not found!")


# 6. Payment Method Bar Chart
def method_chart():
    cur.execute("""
    SELECT payment_method, COUNT(*)
    FROM payments
    GROUP BY payment_method
    """)

    data = cur.fetchall()

    if not data:
        print("No payment records found!")
        return

    methods = [row[0] for row in data]
    totals = [row[1] for row in data]

    plt.bar(methods, totals)
    plt.title("Transactions by Payment Method")
    plt.xlabel("Payment Method")
    plt.ylabel("Number of Transactions")
    plt.tight_layout()
    plt.show()


# 7. Monthly Payment Trend
def monthly_chart():
    cur.execute("""
    SELECT DATE_FORMAT(transaction_date,'%Y-%m'),
    SUM(amount)
    FROM payments
    WHERE status='Success'
    GROUP BY DATE_FORMAT(transaction_date,'%Y-%m')
    ORDER BY DATE_FORMAT(transaction_date,'%Y-%m')
    """)

    data = cur.fetchall()

    if not data:
        print("No successful transactions found!")
        return

    months = [row[0] for row in data]
    amounts = [float(row[1]) for row in data]

    plt.plot(months, amounts, marker='o')
    plt.title("Monthly Successful Payment Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# 8. Amount Report
def amount_report():
    cur.execute("""
    SELECT SUM(amount), AVG(amount),
    MAX(amount), MIN(amount)
    FROM payments
    """)

    result = cur.fetchone()

    print("Total Amount:", result[0])
    print("Average Amount:", round(float(result[1]), 2)
          if result[1] is not None else 0)
    print("Maximum Amount:", result[2])
    print("Minimum Amount:", result[3])


# Main Menu
while True:

    print("\n===== UPI AND DIGITAL PAYMENT ANALYSIS =====")
    print("1. Add Payment")
    print("2. Display Payments")
    print("3. Search Payment")
    print("4. Update Payment Status")
    print("5. Delete Payment")
    print("6. Payment Method Bar Chart")
    print("7. Monthly Trend Line Chart")
    print("8. Amount Report")
    print("9. Exit")

    choice = input("Enter Choice: ")

    try:
        if choice == "1":
            add_payment()

        elif choice == "2":
            display_payments()

        elif choice == "3":
            search_payment()

        elif choice == "4":
            update_status()

        elif choice == "5":
            delete_payment()

        elif choice == "6":
            method_chart()

        elif choice == "7":
            monthly_chart()

        elif choice == "8":
            amount_report()

        elif choice == "9":
            break

        else:
            print("Invalid Choice!")

    except mysql.connector.Error as e:
        con.rollback()
        print("Database Error:", e)

    except ValueError:
        print("Enter valid numeric values!")

cur.close()
con.close()

print("Program closed successfully!")
