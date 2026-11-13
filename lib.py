
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. MySQL Connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="lib"
)

cur = con.cursor()


# 2. Add New Book
def add_book():
    print("\n--- ADD NEW BOOK ---")
    bid = int(input("Book ID: "))
    name = input("Book Name: ")
    author = input("Author: ")
    publisher = input("Publisher: ")
    copies = int(input("Total Copies: "))

    sql = """INSERT INTO books
    (book_id, book_name, author, publisher,
     total_copies, available_copies)
    VALUES (%s,%s,%s,%s,%s,%s)"""

    cur.execute(sql, (bid, name, author, publisher,
                      copies, copies))
    con.commit()
    print("Book Added Successfully!")


# 3. Display All Books
def display_books():
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()

    print("\nBOOK DETAILS")
    print("-" * 65)
    for r in rows:
        print(r)

# 4. Search Book
def search_book():
    name = input("Enter Book Name: ")
    cur.execute("SELECT * FROM books WHERE book_name LIKE %s",
                ("%" + name + "%",))
    rows = cur.fetchall()

    if rows:
        for r in rows:
            print(r)
    else:
        print("Book Not Found!")

# 5. Issue Book
def issue_book():
    bid = int(input("Enter Book ID: "))
    student = input("Student Name: ")
    adm = int(input("Admission Number: "))

    cur.execute("SELECT available_copies FROM books WHERE book_id=%s",
                (bid,))
    row = cur.fetchone()

    if row and row[0] > 0:
        cur.execute("""
        INSERT INTO issue_records
        (book_id, student_name, admission_no, issue_date, status)
        VALUES (%s,%s,%s,CURDATE(),'Issued')
        """, (bid, student, adm))

        cur.execute(
            "UPDATE books SET available_copies=available_copies-1 WHERE book_id=%s",
            (bid,))
        con.commit()
        print("Book Issued Successfully!")
    else:
        print("Book Not Available!")

# 6. Return Book
def return_book():
    iid = int(input("Enter Issue ID: "))

    cur.execute(
        "SELECT book_id FROM issue_records WHERE issue_id=%s AND status='Issued'",
        (iid,))
    row = cur.fetchone()

    if row:
        bid = row[0]

        cur.execute("""
        UPDATE issue_records
        SET status='Returned', return_date=CURDATE()
        WHERE issue_id=%s
        """, (iid,))

        cur.execute(
            "UPDATE books SET available_copies=available_copies+1 WHERE book_id=%s",
            (bid,))
        con.commit()
        print("Book Returned Successfully!")
    else:
        print("Invalid Issue ID or Book Already Returned!")

# 7. Display Issue Records
def display_issues():
    cur.execute("SELECT * FROM issue_records")
    for r in cur.fetchall():
        print(r)




# 9. Matplotlib Charts
def book_chart():
    cur.execute("SELECT book_name, available_copies FROM books")
    rows = cur.fetchall()

    df = pd.DataFrame(rows, columns=["book_name", "available_copies"])

    if df.empty:
        print("No Book Records Available!")
        return

    print("\n--- MATPLOTLIB CHARTS ---")
    print("1. Bar Chart")
    print("2. Line Chart")
    print("3. Histogram")

    ch = int(input("Enter Chart Choice: "))

    if ch == 1:
        plt.bar(df["book_name"], df["available_copies"])
        plt.xlabel("Book Name")
        plt.ylabel("Available Copies")
        plt.title("Book Availability - Bar Chart")
        plt.xticks(rotation=45)

    elif ch == 2:
        plt.plot(df["book_name"], df["available_copies"],
                 marker="o")
        plt.xlabel("Book Name")
        plt.ylabel("Available Copies")
        plt.title("Book Availability - Line Chart")
        plt.xticks(rotation=45)

    elif ch == 3:
        plt.hist(df["available_copies"], bins=5,
                 edgecolor="black")
        plt.xlabel("Available Copies")
        plt.ylabel("Number of Books")
        plt.title("Book Availability - Histogram")

    else:
        print("Invalid Chart Choice!")
        return

    plt.tight_layout()
    plt.show()


# 10. Main Menu
while True:
    print("\n====== LIBRARY MANAGEMENT SYSTEM ======")
    print("1. Add New Book")
    print("2. Display All Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Display Issue Records")
    print("7. Book Availability Chart Wise")
    print("8. Exit")

    ch = int(input("Enter Choice: "))

    if ch == 1:
        add_book()
    elif ch == 2:
        display_books()
    elif ch == 3:
        search_book()
    elif ch == 4:
        issue_book()
    elif ch == 5:
        return_book()
    elif ch == 6:
        display_issues()
    elif ch == 7:
        book_chart()
    elif ch == 8:
        print("Thank You!")
        break
    else:
        print("Invalid Choice!")

cur.close()
con.close()
