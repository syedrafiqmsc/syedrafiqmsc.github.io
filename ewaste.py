
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# CONNECT TO MYSQL DATABASE
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="ewaste"
)

cur = con.cursor()

# 1. ADD NEW E-WASTE COLLECTION
def add_collection():
    print("\n--- ADD E-WASTE COLLECTION ---")

    item = input("Enter Item Name: ")
    category = int(input("Enter Category ID: "))
    quantity = float(input("Enter Quantity in KG: "))
    date = input("Enter Collection Date (YYYY-MM-DD): ")
    location = input("Enter Collection Location: ")

    sql = """INSERT INTO collections
    (item_name, category_id, quantity_kg, collection_date, collection_location)
    VALUES (%s, %s, %s, %s, %s)"""

    values = (item, category, quantity, date, location)

    cur.execute(sql, values)
    con.commit()

    print("Collection Record Added Successfully!")


# 2. DISPLAY ALL COLLECTIONS
def display_collections():
    print("\n--- E-WASTE COLLECTION RECORDS ---")

    sql = """SELECT c.collection_id, c.item_name,
    w.category_name, c.quantity_kg, c.collection_date,
    c.collection_location
    FROM collections c
    JOIN waste_categories w
    ON c.category_id = w.category_id"""

    df = pd.read_sql(sql, con)
    print(df.to_string(index=False))


# 3. DISPLAY WASTE CATEGORIES
def display_categories():
    print("\n--- WASTE CATEGORIES ---")

    cur.execute("SELECT * FROM waste_categories")

    for row in cur.fetchall():
        print(row)


# 4. DISPLAY DISPOSAL METHODS
def display_methods():
    print("\n--- DISPOSAL METHODS ---")

    cur.execute("SELECT * FROM disposal_methods")

    for row in cur.fetchall():
        print(row)


# 5. ADD DISPOSAL RECORD
def add_disposal():
    print("\n--- ADD DISPOSAL RECORD ---")

    collection = int(input("Enter Collection ID: "))
    method = int(input("Enter Disposal Method ID: "))
    quantity = float(input("Enter Disposed Quantity in KG: "))
    date = input("Enter Disposal Date (YYYY-MM-DD): ")
    remarks = input("Enter Remarks: ")

    sql = """INSERT INTO disposal_records
    (collection_id, method_id, quantity_kg, disposal_date, remarks)
    VALUES (%s, %s, %s, %s, %s)"""

    values = (collection, method, quantity, date, remarks)

    cur.execute(sql, values)
    con.commit()

    print("Disposal Record Added Successfully!")


# 6. DISPLAY DISPOSAL RECORDS
def display_disposals():
    print("\n--- DISPOSAL RECORDS ---")

    sql = """SELECT d.disposal_id, c.item_name,
    m.method_name, d.quantity_kg, d.disposal_date, d.remarks
    FROM disposal_records d
    JOIN collections c ON d.collection_id = c.collection_id
    JOIN disposal_methods m ON d.method_id = m.method_id"""

    df = pd.read_sql(sql, con)
    print(df.to_string(index=False))


# 7. DISPLAY RECYCLING STATISTICS
def recycling_statistics():
    print("\n--- E-WASTE STATISTICS ---")

    sql = """SELECT w.category_name,
    SUM(c.quantity_kg) AS collected_kg,
    COALESCE(SUM(d.quantity_kg), 0) AS disposed_kg
    FROM waste_categories w
    JOIN collections c ON w.category_id = c.category_id
    LEFT JOIN disposal_records d ON c.collection_id = d.collection_id
    GROUP BY w.category_id, w.category_name"""

    df = pd.read_sql(sql, con)

    df["remaining_kg"] = df["collected_kg"] - df["disposed_kg"]

    print(df.to_string(index=False))

    print("\nTotal Collected:", df["collected_kg"].sum(), "KG")
    print("Total Disposed:", df["disposed_kg"].sum(), "KG")
    print("Remaining Waste:", df["remaining_kg"].sum(), "KG")


# 8. DISPLAY CHARTS
def display_charts():
    sql = """SELECT w.category_name,
    SUM(c.quantity_kg) AS total_kg
    FROM collections c
    JOIN waste_categories w ON c.category_id = w.category_id
    GROUP BY w.category_id, w.category_name"""

    df = pd.read_sql(sql, con)

    print("\n1. Bar Chart")
    print("2. Line Chart")
    print("3. Histogram")

    choice = input("Enter your choice: ")

    if choice == "1":
        plt.bar(df["category_name"], df["total_kg"])
        plt.title("E-Waste Collection by Category")
        plt.xlabel("Waste Category")
        plt.ylabel("Quantity (KG)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    elif choice == "2":
        plt.plot(df["category_name"], df["total_kg"], marker="o")
        plt.title("E-Waste Collection Analysis")
        plt.xlabel("Waste Category")
        plt.ylabel("Quantity (KG)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.show()

    elif choice == "3":
        plt.hist(df["total_kg"], bins=5, edgecolor="black")
        plt.title("Distribution of E-Waste")
        plt.xlabel("Quantity (KG)")
        plt.ylabel("Frequency")
        plt.show()

    else:
        print("Invalid Chart Choice!")


# MAIN MENU
while True:
    print("\n================================")
    print(" E-WASTE MANAGEMENT SYSTEM")
    print("================================")
    print("1. Add E-Waste Collection")
    print("2. Display Collections")
    print("3. Display Waste Categories")
    print("4. Display Disposal Methods")
    print("5. Add Disposal Record")
    print("6. Display Disposal Records")
    print("7. Recycling Statistics")
    print("8. Display Charts")
    print("9. Exit")

    choice = input("Enter Your Choice: ")

    try:
        if choice == "1":
            add_collection()

        elif choice == "2":
            display_collections()

        elif choice == "3":
            display_categories()

        elif choice == "4":
            display_methods()

        elif choice == "5":
            add_disposal()

        elif choice == "6":
            display_disposals()

        elif choice == "7":
            recycling_statistics()

        elif choice == "8":
            display_charts()

        elif choice == "9":
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")

    except mysql.connector.Error as e:
        con.rollback()
        print("Database Error:", e)

    except ValueError:
        print("Please enter valid numeric values.")

cur.close()
con.close()
