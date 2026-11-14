import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect to MySQL Database
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="ecom"
)

cur = con.cursor()

# 2. Display Customers
def display_customers():
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()

    print("\nCUSTOMER DETAILS")
    for row in rows:
        print(row)

# 3. Display Products
def display_products():
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()

    print("\nPRODUCT DETAILS")
    for row in rows:
        print(row)

# 4. Add New Customer
def add_customer():
    cid = int(input("Enter Customer ID: "))
    name = input("Enter Customer Name: ")
    city = input("Enter City: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")

    sql = """INSERT INTO customers
    VALUES (%s,%s,%s,%s,%s)"""

    cur.execute(sql, (cid, name, city, phone, email))
    con.commit()

    print("Customer added successfully.")

# 5. Add New Product
def add_product():
    pid = int(input("Enter Product ID: "))
    name = input("Enter Product Name: ")
    category = input("Enter Category: ")
    price = float(input("Enter Price: "))
    stock = int(input("Enter Stock: "))

    sql = """INSERT INTO products
    VALUES (%s,%s,%s,%s,%s)"""

    cur.execute(sql, (pid, name, category, price, stock))
    con.commit()

    print("Product added successfully.")

# 6. Display Orders
def display_orders():
    sql = """SELECT orders.order_id,
    customers.customer_name,
    orders.order_date,
    orders.order_status
    FROM orders
    INNER JOIN customers
    ON orders.customer_id = customers.customer_id"""

    cur.execute(sql)

    print("\nORDER DETAILS")
    for row in cur.fetchall():
        print(row)

# 7. Place New Order
def place_order():
    try:
        oid = int(input("Enter Order ID: "))
        cid = int(input("Enter Customer ID: "))
        pid = int(input("Enter Product ID: "))
        qty = int(input("Enter Quantity: "))

        if qty <= 0:
            print("Quantity must be greater than zero.")
            return

        cur.execute(
            "SELECT price, stock FROM products WHERE product_id=%s",
            (pid,)
        )
        product = cur.fetchone()

        if product is None:
            print("Product not found.")
            return

        price, stock = product

        if qty > stock:
            print("Insufficient stock.")
            return

        cur.execute(
            "SELECT customer_id FROM customers WHERE customer_id=%s",
            (cid,)
        )

        if cur.fetchone() is None:
            print("Customer not found.")
            return

        total = float(price) * qty

        method = input(
            "Payment Method (UPI/Card/Cash): "
        )

        status = input(
            "Payment Status (Paid/Pending): "
        ).strip().capitalize()

        if status not in ("Paid", "Pending"):
            print("Invalid payment status.")
            return

        # Insert Order
        cur.execute(
            """INSERT INTO orders
            VALUES (%s,%s,CURDATE(),'Pending')""",
            (oid, cid)
        )

        # Insert Order Item
        cur.execute(
            """INSERT INTO order_items
            VALUES (%s,%s,%s,%s)""",
            (oid, oid, pid, qty)
        )

        # Insert Payment
        cur.execute(
            """INSERT INTO payments
            VALUES (%s,%s,%s,%s,%s)""",
            (oid, oid, method, total, status)
        )

        # Update Product Stock
        cur.execute(
            """UPDATE products
            SET stock = stock - %s
            WHERE product_id = %s""",
            (qty, pid)
        )

        con.commit()

        print("\nOrder placed successfully!")
        print("Product:", pid)
        print("Quantity:", qty)
        print("Total Amount: Rs.", total)

    except mysql.connector.Error as e:
        con.rollback()
        print("Database Error:", e)

    except ValueError:
        con.rollback()
        print("Please enter valid numeric values.")

# 8. Display Payment Details
def display_payments():
    sql = """SELECT * FROM payments"""

    cur.execute(sql)

    print("\nPAYMENT DETAILS")
    for row in cur.fetchall():
        print(row)

# 9. Display Sales DataFrame
def sales_dataframe():
    sql = """SELECT p.product_name,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.quantity * p.price) AS total_sales
    FROM products p
    INNER JOIN order_items oi
    ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name"""

    df = pd.read_sql(sql, con)

    print("\nPRODUCT SALES ANALYSIS")
    print(df.to_string(index=False))

# 10. Sales Charts Menu
def sales_charts():

    sql = """SELECT p.product_name,
    SUM(oi.quantity) AS quantity,
    SUM(oi.quantity * p.price) AS sales
    FROM products p
    INNER JOIN order_items oi
    ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name"""

    df = pd.read_sql(sql, con)

    if df.empty:
        print("No sales data available.")
        return

    while True:
        print("\n===== SALES CHARTS =====")
        print("1. Bar Chart - Product Sales")
        print("2. Line Chart - Product Sales")
        print("3. Histogram - Order Amounts")
        print("4. Back to Main Menu")

        ch = input("Enter your choice: ")

        if ch == '1':
            plt.bar(df['product_name'], df['sales'])
            plt.title("Product-wise Sales")
            plt.xlabel("Products")
            plt.ylabel("Sales Amount")
            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.show()

        elif ch == '2':
            plt.plot(
                df['product_name'],
                df['sales'],
                marker='o'
            )
            plt.title("Product Sales Comparison")
            plt.xlabel("Products")
            plt.ylabel("Sales Amount")
            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.show()

        elif ch == '3':
            order_df = pd.read_sql(
                "SELECT amount FROM payments WHERE payment_status='Paid'",
                con
            )

            if order_df.empty:
                print("No paid orders available.")
            else:
                plt.hist(
                    order_df['amount'],
                    bins=5,
                    edgecolor='black'
                )
                plt.title("Order Amount Distribution")
                plt.xlabel("Order Amount")
                plt.ylabel("Number of Orders")
                plt.tight_layout()
                plt.show()

        elif ch == '4':
            break

        else:
            print("Invalid choice.")

# 11. Main Menu
while True:

    print("\n======================================")
    print(" E-COMMERCE MANAGEMENT SYSTEM")
    print("======================================")
    print("1. Add Customer")
    print("2. Add Product")
    print("3. Display Customers")
    print("4. Display Products")
    print("5. Place New Order")
    print("6. Display Orders")
    print("7. Display Payments")
    print("8. Sales DataFrame")
    print("9. Sales Charts")
    print("10. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_customer()

    elif choice == '2':
        add_product()

    elif choice == '3':
        display_customers()

    elif choice == '4':
        display_products()

    elif choice == '5':
        place_order()

    elif choice == '6':
        display_orders()

    elif choice == '7':
        display_payments()

    elif choice == '8':
        sales_dataframe()

    elif choice == '9':
        sales_charts()

    elif choice == '10':
        print("Thank you for using E-Commerce System!")
        break

    else:
        print("Invalid choice. Try again.")

cur.close()
con.close()
