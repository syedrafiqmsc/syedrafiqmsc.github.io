
# RAILWAY RESERVATION MANAGEMENT SYSTEM
# CLASS XII INFORMATICS PRACTICES PROJECT

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# DATABASE CONNECTION
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="railway"
)
cur = con.cursor()

# DATE VALIDATION
def get_date():
    d = input("Journey Date (YYYY-MM-DD): ")
    try:
        jd = date.fromisoformat(d)
        if jd < date.today():
            print("Past dates are not allowed!")
            return None
        return jd
    except ValueError:
        print("Invalid Date!")
        return None

# 1. DISPLAY TRAINS
def trains():
    cur.execute("SELECT * FROM trains")
    df = pd.DataFrame(cur.fetchall(), columns=[
        "Train No", "Train Name", "Source",
        "Destination", "Seats", "Fare"
    ])
    print(df.to_string(index=False))

# 2. DISPLAY PASSENGERS
def passengers():
    cur.execute("SELECT * FROM passengers")
    df = pd.DataFrame(cur.fetchall(), columns=[
        "ID", "Name", "Age", "Gender", "Phone"
    ])
    print(df.to_string(index=False))

# 3. ADD NEW PASSENGER
def add_passenger():
    pid = int(input("Passenger ID: "))
    name = input("Passenger Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    phone = input("Phone Number: ")

    try:
        cur.execute(
            "INSERT INTO passengers VALUES (%s,%s,%s,%s,%s)",
            (pid, name, age, gender, phone)
        )
        con.commit()
        print("Passenger Added Successfully!")
    except mysql.connector.Error as e:
        con.rollback()
        print("Error:", e)

# 4. CHECK SEAT AVAILABILITY
def availability():
    t = int(input("Train Number: "))
    d = get_date()
    if d is None:
        return

    cur.execute("SELECT total_seats FROM trains WHERE train_no=%s", (t,))
    r = cur.fetchone()
    if r is None:
        print("Train Not Found!")
        return

    cur.execute("""SELECT COUNT(*) FROM bookings
        WHERE train_no=%s AND journey_date=%s
        AND booking_status='Confirmed'""", (t, d))
    booked = cur.fetchone()[0]

    print("Total Seats:", r[0])
    print("Booked Seats:", booked)
    print("Available Seats:", r[0]-booked)

# 5. BOOK TICKET
def booking():
    p = int(input("Passenger ID: "))
    t = int(input("Train Number: "))
    d = get_date()
    if d is None:
        return

    cur.execute("SELECT passenger_name FROM passengers WHERE passenger_id=%s", (p,))
    passenger = cur.fetchone()
    if passenger is None:
        print("Passenger Not Found!")
        return

    cur.execute("SELECT total_seats,fare FROM trains WHERE train_no=%s", (t,))
    train = cur.fetchone()
    if train is None:
        print("Train Not Found!")
        return

    total, fare = train
    cur.execute("""SELECT seat_no FROM bookings
        WHERE train_no=%s AND journey_date=%s
        AND booking_status='Confirmed'""", (t, d))
    seats = [x[0] for x in cur.fetchall()]

    seat = next((i for i in range(1, total+1) if i not in seats), None)
    if seat is None:
        print("No Seats Available!")
        return

    cur.execute("SELECT MAX(booking_id) FROM bookings")
    bid = (cur.fetchone()[0] or 100)+1
    cur.execute("SELECT MAX(payment_id) FROM payments")
    payid = (cur.fetchone()[0] or 0)+1

    try:
        cur.execute("INSERT INTO bookings VALUES (%s,%s,%s,%s,%s,%s)",
                    (bid, p, t, d, seat, "Confirmed"))
        cur.execute("INSERT INTO payments VALUES (%s,%s,%s,%s,%s)",
                    (payid, bid, fare, "UPI", "Paid"))
        con.commit()
        print("Ticket Booked Successfully!")
        print("Passenger:", passenger[0])
        print("Booking ID:", bid)
        print("Seat Number:", seat)
        print("Fare: Rs.", fare)
    except mysql.connector.Error as e:
        con.rollback()
        print("Booking Error:", e)

# 6. CANCEL TICKET
def cancellation():
    bid = int(input("Booking ID: "))
    cur.execute("SELECT booking_status FROM bookings WHERE booking_id=%s", (bid,))
    r = cur.fetchone()

    if r is None:
        print("Booking Not Found!")
    elif r[0] == "Cancelled":
        print("Already Cancelled!")
    else:
        cur.execute("UPDATE bookings SET booking_status='Cancelled' WHERE booking_id=%s", (bid,))
        cur.execute("""UPDATE payments SET payment_status='Refunded'
            WHERE booking_id=%s AND payment_status='Paid'""", (bid,))
        con.commit()
        print("Ticket Cancelled Successfully!")

# 7. SEARCH PASSENGER
def search():
    p = int(input("Passenger ID: "))
    cur.execute("""SELECT p.passenger_name,t.train_name,
        b.journey_date,b.seat_no,b.booking_status
        FROM passengers p JOIN bookings b
        ON p.passenger_id=b.passenger_id
        JOIN trains t ON b.train_no=t.train_no
        WHERE p.passenger_id=%s""", (p,))
    data = cur.fetchall()

    if data:
        df = pd.DataFrame(data, columns=[
            "Passenger", "Train", "Date", "Seat", "Status"
        ])
        print(df.to_string(index=False))
    else:
        print("No Records Found!")

# 8. DISPLAY BOOKINGS
def bookings():
    cur.execute("""SELECT b.booking_id,p.passenger_name,
        t.train_name,b.journey_date,b.seat_no,b.booking_status
        FROM bookings b JOIN passengers p
        ON b.passenger_id=p.passenger_id
        JOIN trains t ON b.train_no=t.train_no""")
    df = pd.DataFrame(cur.fetchall(), columns=[
        "Booking ID", "Passenger", "Train",
        "Date", "Seat", "Status"
    ])
    print(df.to_string(index=False))

# 9. DISPLAY PAYMENTS
def payments():
    cur.execute("SELECT * FROM payments")
    df = pd.DataFrame(cur.fetchall(), columns=[
        "Payment ID", "Booking ID", "Amount",
        "Mode", "Status"
    ])
    print(df.to_string(index=False))

# 10. DISPLAY ALL THREE CHARTS
def charts():

    # BAR CHART
    cur.execute("""SELECT t.train_name,COUNT(b.booking_id)
        FROM trains t LEFT JOIN bookings b
        ON t.train_no=b.train_no
        AND b.booking_status='Confirmed'
        GROUP BY t.train_no,t.train_name""")
    df = pd.DataFrame(cur.fetchall(), columns=["Train", "Bookings"])
    df.plot(x="Train", y="Bookings", kind="bar", legend=False)
    plt.title("Train Wise Bookings")
    plt.tight_layout()
    plt.show()

    # LINE CHART
    cur.execute("""SELECT journey_date,COUNT(*) FROM bookings
        WHERE booking_status='Confirmed'
        GROUP BY journey_date ORDER BY journey_date""")
    data = cur.fetchall()
    if data:
        df = pd.DataFrame(data, columns=["Date", "Bookings"])
        df.plot(x="Date", y="Bookings", kind="line", marker="o", legend=False)
        plt.title("Date Wise Bookings")
        plt.tight_layout()
        plt.show()
    else:
        print("No Booking Data!")

    # HISTOGRAM
    cur.execute("SELECT fare FROM trains")
    df = pd.DataFrame(cur.fetchall(), columns=["Fare"])
    df["Fare"].plot(kind="hist", bins=5)
    plt.title("Train Fare Distribution")
    plt.tight_layout()
    plt.show()

# 11. MAIN MENU
while True:
    print("\n===== RAILWAY RESERVATION SYSTEM =====")
    print("1. Display Trains")
    print("2. Display Passengers")
    print("3. Add New Passenger")
    print("4. Check Seat Availability")
    print("5. Book Ticket")
    print("6. Cancel Ticket")
    print("7. Search Passenger")
    print("8. Display Bookings")
    print("9. Display Payments")
    print("10. Display All Charts")
    print("11. Exit")

    ch = input("Enter Your Choice: ")

    try:
        if ch == '1':
            trains()
        elif ch == '2':
            passengers()
        elif ch == '3':
            add_passenger()
        elif ch == '4':
            availability()
        elif ch == '5':
            booking()
        elif ch == '6':
            cancellation()
        elif ch == '7':
            search()
        elif ch == '8':
            bookings()
        elif ch == '9':
            payments()
        elif ch == '10':
            charts()
        elif ch == '11':
            break
        else:
            print("Invalid Choice!")

    except ValueError:
        print("Enter Valid Input!")
    except mysql.connector.Error as e:
        con.rollback()
        print("Database Error:", e)

cur.close()
con.close()
print("Thank You!")
