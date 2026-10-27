# HOTEL MANAGEMENT SYSTEM
# Student project using Python, MySQL and Matplotlib
# Install required packages from Command Prompt:
# pip install mysql-connector-python matplotlib

import mysql.connector
from tkinter import Tk, simpledialog
from datetime import datetime
import matplotlib.pyplot as plt


def get_mysql_password():
    """Ask for the local MySQL password without displaying it."""
    root = Tk()
    root.withdraw()
    password = simpledialog.askstring(
        "MySQL Login",
        "Enter your MySQL password:",
        show="*"
    )
    root.destroy()
    if password is None:
        raise SystemExit("Login cancelled.")
    return password


def main():
    password = get_mysql_password()

    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="hotel"
    )
    cur = con.cursor()

    def add_customer():
        name = input("Customer name: ").strip()
        phone = input("Phone number: ").strip()
        address = input("Address: ").strip()

        if not name:
            print("Customer name cannot be empty.")
            return

        cur.execute(
            """INSERT INTO Customer (CustomerName, Phone, Address)
               VALUES (%s, %s, %s)""",
            (name, phone, address)
        )
        con.commit()
        print("Customer added successfully. Customer ID:", cur.lastrowid)

    def view_customers():
        cur.execute(
            "SELECT CustomerID, CustomerName, Phone, Address FROM Customer"
        )
        rows = cur.fetchall()
        print("\nCUSTOMER DETAILS")
        if not rows:
            print("No customer records found.")
        for row in rows:
            print(row)

    def view_rooms():
        cur.execute(
            "SELECT RoomNo, RoomType, Price, Status FROM Room ORDER BY RoomNo"
        )
        rows = cur.fetchall()
        print("\nROOM DETAILS")
        if not rows:
            print("No room records found.")
        for row in rows:
            print(row)

    def book_room():
        try:
            customer_id = int(input("Customer ID: "))
            room_no = int(input("Room number: "))
            check_in = input("Check-in date (YYYY-MM-DD): ").strip()
            check_out = input("Check-out date (YYYY-MM-DD): ").strip()

            start = datetime.strptime(check_in, "%Y-%m-%d").date()
            end = datetime.strptime(check_out, "%Y-%m-%d").date()

            if end <= start:
                print("Check-out date must be after check-in date.")
                return

            cur.execute(
                "SELECT CustomerID FROM Customer WHERE CustomerID = %s",
                (customer_id,)
            )
            if cur.fetchone() is None:
                print("Customer ID not found. Add the customer first.")
                return

            cur.execute(
                "SELECT Status FROM Room WHERE RoomNo = %s",
                (room_no,)
            )
            room = cur.fetchone()

            if room is None:
                print("Room number not found.")
                return
            if room[0] != "Available":
                print("This room is not marked Available.")
                return

            cur.execute(
                """INSERT INTO Booking (CustomerID, RoomNo, CheckIn, CheckOut)
                   VALUES (%s, %s, %s, %s)""",
                (customer_id, room_no, start, end)
            )
            cur.execute(
                "UPDATE Room SET Status = 'Booked' WHERE RoomNo = %s",
                (room_no,)
            )
            con.commit()
            print("Room booked successfully. Booking ID:", cur.lastrowid)

        except ValueError:
            con.rollback()
            print("Invalid ID or date. Use YYYY-MM-DD for dates.")
        except mysql.connector.Error as err:
            con.rollback()
            print("Booking error:", err)

    def view_bookings():
        cur.execute(
            """SELECT b.BookingID, c.CustomerName, b.RoomNo,
                      b.CheckIn, b.CheckOut
               FROM Booking AS b
               JOIN Customer AS c ON b.CustomerID = c.CustomerID
               ORDER BY b.BookingID"""
        )
        rows = cur.fetchall()
        print("\nBOOKING DETAILS")
        if not rows:
            print("No booking records found.")
        for row in rows:
            print(row)

    def display_charts():
        cur.execute(
            """SELECT CheckIn, COUNT(*)
               FROM Booking
               GROUP BY CheckIn
               ORDER BY CheckIn"""
        )
        booking_data = cur.fetchall()

        cur.execute(
            """SELECT RoomType, COUNT(*)
               FROM Room
               GROUP BY RoomType
               ORDER BY RoomType"""
        )
        room_data = cur.fetchall()

        cur.execute("SELECT Price FROM Room WHERE Price IS NOT NULL")
        price_data = cur.fetchall()

        dates = [str(row[0]) for row in booking_data]
        booking_counts = [row[1] for row in booking_data]
        room_types = [row[0] for row in room_data]
        room_counts = [row[1] for row in room_data]
        prices = [float(row[0]) for row in price_data]

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        if dates:
            axes[0].plot(dates, booking_counts, marker="o", label="Bookings")
            axes[0].legend()
            axes[0].tick_params(axis="x", rotation=45)
        else:
            axes[0].text(0.5, 0.5, "No booking records",
                         ha="center", va="center")
        axes[0].set_title("Bookings by Date")
        axes[0].set_xlabel("Check-in Date")
        axes[0].set_ylabel("Number of Bookings")

        if room_types:
            axes[1].bar(room_types, room_counts, label="Rooms")
            axes[1].legend()
        else:
            axes[1].text(0.5, 0.5, "No room records",
                         ha="center", va="center")
        axes[1].set_title("Rooms by Type")
        axes[1].set_xlabel("Room Type")
        axes[1].set_ylabel("Number of Rooms")

        if prices:
            axes[2].hist(prices, bins=min(5, len(set(prices))),
                         edgecolor="black", label="Room Prices")
            axes[2].legend()
        else:
            axes[2].text(0.5, 0.5, "No room prices",
                         ha="center", va="center")
        axes[2].set_title("Room Price Distribution")
        axes[2].set_xlabel("Room Price (Rs.)")
        axes[2].set_ylabel("Number of Rooms")

        fig.tight_layout()
        plt.show()

    try:
        while True:
            print("\n===== HOTEL MANAGEMENT SYSTEM =====")
            print("1. Add Customer")
            print("2. View Customers")
            print("3. View Rooms")
            print("4. Book Room")
            print("5. View Bookings")
            print("6. Display All Charts")
            print("7. Exit")

            choice = input("Enter your choice: ").strip()

            try:
                if choice == "1":
                    add_customer()
                elif choice == "2":
                    view_customers()
                elif choice == "3":
                    view_rooms()
                elif choice == "4":
                    book_room()
                elif choice == "5":
                    view_bookings()
                elif choice == "6":
                    display_charts()
                elif choice == "7":
                    break
                else:
                    print("Invalid choice. Enter a number from 1 to 7.")
            except mysql.connector.Error as err:
                con.rollback()
                print("Database error:", err)

    finally:
        cur.close()
        con.close()
        print("MySQL connection closed.")


if __name__ == "__main__":
    try:
        main()
    except mysql.connector.Error as err:
        print("Could not connect to MySQL:", err)
        print("Check that MySQL Server is running and the hotel database exists.")
