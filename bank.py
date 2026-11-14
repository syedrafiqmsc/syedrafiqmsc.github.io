
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONNECT TO MYSQL

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="bank"
)

cur = con.cursor()

# 2. FUNCTION TO DISPLAY DATAFRAME

def display_data(sql, values=None):

    cur.execute(sql, values or ())
    rows = cur.fetchall()

    columns = [col[0] for col in cur.description]

    if rows:
        df = pd.DataFrame(rows, columns=columns)
        print(df.to_string(index=False))
    else:
        print("No Records Found!")


# 3. MAIN MENU

while True:

    print("\n========== BANK MANAGEMENT SYSTEM ==========")
    print("1. Display Customers")
    print("2. Display Accounts")
    print("3. Add New Customer")
    print("4. Deposit Amount")
    print("5. Withdraw Amount")
    print("6. Check Account Balance")
    print("7. Display Transactions")
    print("8. Transaction History")
    print("9. Display Charts")
    print("10. Exit")

    try:
        ch = int(input("Enter Choice: "))
    except ValueError:
        print("Enter a valid number!")
        continue

    # 4. DISPLAY CUSTOMERS

    if ch == 1:

        display_data("SELECT * FROM customers")

    # 5. DISPLAY ACCOUNTS

    elif ch == 2:

        display_data("SELECT * FROM accounts")

    # 6. ADD NEW CUSTOMER

    elif ch == 3:

        cid = int(input("Customer ID: "))
        name = input("Customer Name: ")
        gender = input("Gender: ")
        phone = input("Phone Number: ")
        city = input("City: ")

        sql = """INSERT INTO customers
                 (customer_id, customer_name, gender, phone, city)
                 VALUES (%s,%s,%s,%s,%s)"""

        cur.execute(sql, (cid, name, gender, phone, city))
        con.commit()

        print("Customer Added Successfully!")

    # 7. DEPOSIT AMOUNT

    elif ch == 4:

        aid = int(input("Account Number: "))
        amount = float(input("Deposit Amount: "))

        if amount <= 0:
            print("Enter a valid amount!")
            continue

        cur.execute(
            "SELECT balance FROM accounts WHERE account_no=%s",
            (aid,)
        )

        result = cur.fetchone()

        if result:

            cur.execute(
                """UPDATE accounts
                   SET balance = balance + %s
                   WHERE account_no = %s""",
                (amount, aid)
            )

            cur.execute(
                """INSERT INTO transactions
                   (account_no, transaction_date,
                    transaction_type, amount, remarks)
                   VALUES (%s, CURDATE(), 'Deposit', %s, 'Cash Deposit')""",
                (aid, amount)
            )

            con.commit()

            print("Amount Deposited Successfully!")

        else:
            print("Account Not Found!")

    # 8. WITHDRAW AMOUNT

    elif ch == 5:

        aid = int(input("Account Number: "))
        amount = float(input("Withdrawal Amount: "))

        if amount <= 0:
            print("Enter a valid amount!")
            continue

        cur.execute(
            "SELECT balance FROM accounts WHERE account_no=%s",
            (aid,)
        )

        result = cur.fetchone()

        if result:

            if result[0] >= amount:

                cur.execute(
                    """UPDATE accounts
                       SET balance = balance - %s
                       WHERE account_no = %s""",
                    (amount, aid)
                )

                cur.execute(
                    """INSERT INTO transactions
                       (account_no, transaction_date,
                        transaction_type, amount, remarks)
                       VALUES (%s, CURDATE(), 'Withdrawal', %s, 'Cash Withdrawal')""",
                    (aid, amount)
                )

                con.commit()

                print("Withdrawal Successful!")

            else:
                print("Insufficient Balance!")

        else:
            print("Account Not Found!")

    # 9. CHECK ACCOUNT BALANCE

    elif ch == 6:

        aid = int(input("Account Number: "))

        cur.execute(
            """SELECT account_no, customer_id, account_type,
                      balance, account_status
               FROM accounts
               WHERE account_no=%s""",
            (aid,)
        )

        result = cur.fetchone()

        if result:

            print("\nAccount Number:", result[0])
            print("Customer ID:", result[1])
            print("Account Type:", result[2])
            print("Available Balance:", result[3])
            print("Account Status:", result[4])

        else:
            print("Account Not Found!")

    # 10. DISPLAY TRANSACTIONS

    elif ch == 7:

        display_data("SELECT * FROM transactions")

    # 11. TRANSACTION HISTORY

    elif ch == 8:

        aid = int(input("Account Number: "))

        display_data(
            """SELECT * FROM transactions
               WHERE account_no=%s""",
            (aid,)
        )

    # 12. DISPLAY CHARTS

    elif ch == 9:

        cur.execute(
            """SELECT account_type, SUM(balance)
               FROM accounts
               GROUP BY account_type"""
        )

        rows = cur.fetchall()

        if rows:

            df = pd.DataFrame(
                rows,
                columns=["Account Type", "Total Balance"]
            )

            while True:

                print("\n========== CHART MENU ==========")
                print("1. Bar Chart")
                print("2. Line Chart")
                print("3. Histogram")
                print("4. Back to Main Menu")

                cc = int(input("Enter Chart Choice: "))

                if cc == 1:

                    plt.bar(
                        df["Account Type"],
                        df["Total Balance"]
                    )

                    plt.title("Bank Account Balance")
                    plt.xlabel("Account Type")
                    plt.ylabel("Total Balance")
                    plt.show()

                elif cc == 2:

                    plt.plot(
                        df["Account Type"],
                        df["Total Balance"],
                        marker="o"
                    )

                    plt.title("Account Balance Analysis")
                    plt.xlabel("Account Type")
                    plt.ylabel("Total Balance")
                    plt.show()

                elif cc == 3:

                    cur.execute("SELECT balance FROM accounts")
                    balances = [row[0] for row in cur.fetchall()]

                    plt.hist(
                        balances,
                        bins=5,
                        edgecolor="black"
                    )

                    plt.title("Account Balance Distribution")
                    plt.xlabel("Balance")
                    plt.ylabel("Number of Accounts")
                    plt.show()

                elif cc == 4:
                    break

                else:
                    print("Invalid Chart Choice!")

        else:
            print("No Account Data Available!")

    # 13. EXIT

    elif ch == 10:

        print("Thank You for Using Bank Management System!")
        break

    else:
        print("Invalid Choice!")


# 14. CLOSE CONNECTION

cur.close()
con.close()

print("MySQL Connection Closed!")
