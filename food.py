
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# DATABASE CONNECTION
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="food"
)

cur = con.cursor()

# DISPLAY FOOD MENU
def display_menu():
    cur.execute("SELECT * FROM menu_items")
    data = cur.fetchall()

    print("\n--------- FOOD MENU ---------")
    for row in data:
        print(row)

# DISPLAY CUSTOMERS
def display_customers():
    cur.execute("SELECT * FROM customers")
    for row in cur.fetchall():
        print(row)

# PLACE NEW ORDER
def place_order():
    display_customers()

    cid = int(input("\nEnter Customer ID: "))

    display_menu()

    fid = int(input("\nEnter Food ID: "))
    qty = int(input("Enter Quantity: "))

    if qty <= 0:
        print("Quantity must be greater than zero.")
        return

    cur.execute(
        "SELECT price FROM menu_items WHERE food_id=%s",
        (fid,)
    )
    result = cur.fetchone()

    if result is None:
        print("Invalid Food ID!")
        return

    price = result[0]
    total = price * qty

    try:
        cur.execute(
            "INSERT INTO orders "
            "(customer_id, order_date, total_amount) "
            "VALUES (%s, CURDATE(), %s)",
            (cid, total)
        )

        oid = cur.lastrowid

        cur.execute(
            "INSERT INTO order_items "
            "(order_id, food_id, quantity, subtotal) "
            "VALUES (%s, %s, %s, %s)",
            (oid, fid, qty, total)
        )

        cur.execute(
            "INSERT INTO deliveries "
            "(order_id, delivery_status, delivery_date) "
            "VALUES (%s, %s, NULL)",
            (oid, "Pending")
        )

        con.commit()

        print("\nOrder Placed Successfully!")
        print("Order ID:", oid)
        print("Total Amount:", total)

    except mysql.connector.Error as e:
        con.rollback()
        print("Order Error:", e)


# DISPLAY ALL ORDERS
def display_orders():
    query = """
    SELECT o.order_id, c.customer_name,
    o.order_date, o.total_amount,
    d.delivery_status
    FROM orders o
    JOIN customers c
    ON o.customer_id = c.customer_id
    JOIN deliveries d
    ON o.order_id = d.order_id
    """

    cur.execute(query)

    for row in cur.fetchall():
        print(row)


# UPDATE DELIVERY STATUS
def update_delivery():
    oid = int(input("Enter Order ID: "))

    print("1. Pending")
    print("2. Out for Delivery")
    print("3. Delivered")

    choice = int(input("Enter Choice: "))

    status = {
        1: "Pending",
        2: "Out for Delivery",
        3: "Delivered"
    }

    if choice not in status:
        print("Invalid Choice!")
        return

    cur.execute(
        "UPDATE deliveries SET delivery_status=%s, "
        "delivery_date=IF(%s='Delivered', CURDATE(), NULL) "
        "WHERE order_id=%s",
        (status[choice], status[choice], oid)
    )

    if cur.rowcount == 0:
        print("Order ID not found!")
    else:
        con.commit()
        print("Delivery Status Updated!")


# SALES ANALYSIS USING PANDAS
def sales_analysis():
    query = """
    SELECT o.order_date, SUM(o.total_amount) AS sales
    FROM orders o
    GROUP BY o.order_date
    ORDER BY o.order_date
    """

    df = pd.read_sql(query, con)

    print("\n--------- SALES DATAFRAME ---------")
    print(df)

    print("\nTotal Sales:", df["sales"].sum())
    print("Average Sales:", df["sales"].mean())
    print("Highest Sales:", df["sales"].max())

    df["order_date"] = pd.to_datetime(df["order_date"])

    return df


# DISPLAY CHARTS
def display_charts():
    df = sales_analysis()

    print("\n1. Bar Chart")
    print("2. Line Chart")
    print("3. Histogram")

    choice = int(input("Enter Chart Choice: "))

    if choice == 1:
        plt.bar(df["order_date"].astype(str), df["sales"])
        plt.title("Daily Food Sales")
        plt.xlabel("Order Date")
        plt.ylabel("Sales Amount")
        plt.xticks(rotation=45)

    elif choice == 2:
        plt.plot(df["order_date"], df["sales"], marker="o")
        plt.title("Daily Sales Trend")
        plt.xlabel("Order Date")
        plt.ylabel("Sales Amount")
        plt.xticks(rotation=45)

    elif choice == 3:
        plt.hist(df["sales"], bins=5, edgecolor="black")
        plt.title("Food Sales Distribution")
        plt.xlabel("Sales Amount")
        plt.ylabel("Number of Days")

    else:
        print("Invalid Choice!")
        return

    plt.tight_layout()
    plt.show()


# MAIN MENU
while True:

    print("\n================================")
    print(" ONLINE FOOD ORDERING SYSTEM")
    print("================================")
    print("1. Display Food Menu")
    print("2. Display Customers")
    print("3. Place New Order")
    print("4. Display All Orders")
    print("5. Update Delivery Status")
    print("6. Sales Analysis")
    print("7. Display Sales Charts")
    print("8. Exit")

    ch = input("\nEnter Your Choice: ")

    try:
        if ch == '1':
            display_menu()

        elif ch == '2':
            display_customers()

        elif ch == '3':
            place_order()

        elif ch == '4':
            display_orders()

        elif ch == '5':
            update_delivery()

        elif ch == '6':
            sales_analysis()

        elif ch == '7':
            display_charts()

        elif ch == '8':
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")

    except (ValueError, mysql.connector.Error) as e:
        print("Error:", e)
        con.rollback()

cur.close()
con.close()
