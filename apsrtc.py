import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# CONNECT TO MYSQL DATABASE
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="apsrtc"
)
cur = con.cursor()

def line():
    print("-" * 55)

# 1. DISPLAY BUSES AND ROUTES
def show_buses():
    line()
    print("AVAILABLE APSRTC BUSES")
    line()
    cur.execute("""
    SELECT b.bus_id,b.bus_number,b.bus_type,
    r.source,r.destination,b.departure_time,
    b.total_seats,b.fare
    FROM buses b JOIN routes r
    ON b.route_id=r.route_id
    """)
    for row in cur.fetchall():
        print(row)

# 2. ADD PASSENGER
def add_passenger():
    line()
    print("ADD PASSENGER DETAILS")
    name = input("Passenger Name: ").strip()
    try:
        age = int(input("Age: "))
        if age <= 0:
            print("Invalid age")
            return
    except ValueError:
        print("Enter a valid age")
        return
    gender = input("Gender: ").strip()
    phone = input("Phone Number: ").strip()
    if not name or not phone:
        print("Name and phone are required")
        return
    cur.execute("""
    INSERT INTO passengers
    (passenger_name,age,gender,phone)
    VALUES(%s,%s,%s,%s)
    """, (name,age,gender,phone))
    con.commit()
    print("Passenger Added Successfully")
    print("Passenger ID:",cur.lastrowid)

# 3. DISPLAY PASSENGERS
def show_passengers():
    line()
    print("PASSENGER DETAILS")
    cur.execute("SELECT * FROM passengers")
    for row in cur.fetchall():
        print(row)

# 4. CHECK AVAILABLE SEATS
def available_seats(bus_id, journey):
    cur.execute(
    "SELECT total_seats FROM buses WHERE bus_id=%s",
    (bus_id,))
    result = cur.fetchone()
    if result is None:
        return None
    total = result[0]
    cur.execute("""
    SELECT COALESCE(SUM(seats),0)
    FROM bookings
    WHERE bus_id=%s AND journey_date=%s
    AND booking_status='Booked'
    """,(bus_id,journey))
    booked = cur.fetchone()[0]
    return total-booked

# 5. BOOK TICKET
def book_ticket():
    line()
    print("BUS TICKET BOOKING")
    show_buses()
    try:
        pid = int(input("Passenger ID: "))
        bid = int(input("Bus ID: "))
        seats = int(input("Number of Seats: "))
    except ValueError:
        print("Enter valid numbers")
        return

    journey = input("Journey Date (YYYY-MM-DD): ")
    try:
        travel_date = date.fromisoformat(journey)
        if travel_date < date.today():
            print("Past date not allowed")
            return
    except ValueError:
        print("Invalid journey date")
        return

    if seats <= 0:
        print("Enter valid seat quantity")
        return

    cur.execute(
    "SELECT passenger_id FROM passengers WHERE passenger_id=%s",
    (pid,))
    if cur.fetchone() is None:
        print("Passenger not found")
        return

    cur.execute("SELECT fare FROM buses WHERE bus_id=%s",(bid,))
    bus = cur.fetchone()
    if bus is None:
        print("Bus not found")
        return

    remaining = available_seats(bid,journey)
    if seats > remaining:
        print("Available seats:",remaining)
        return

    total = float(bus[0])*seats
    cur.execute("""
    INSERT INTO bookings
    (passenger_id,bus_id,journey_date,seats,
    total_fare,booking_status)
    VALUES(%s,%s,%s,%s,%s,'Booked')
    """,(pid,bid,journey,seats,total))
    con.commit()
    print("Ticket Booked Successfully")
    print("Booking ID:",cur.lastrowid)
    print("Total Fare: Rs.",total)

# 6. DISPLAY BOOKINGS
def show_bookings():
    line()
    print("ALL BOOKING DETAILS")
    cur.execute("""
    SELECT bk.booking_id,p.passenger_name,
    b.bus_number,r.source,r.destination,
    bk.journey_date,bk.seats,bk.total_fare,
    bk.booking_status
    FROM bookings bk
    JOIN passengers p ON bk.passenger_id=p.passenger_id
    JOIN buses b ON bk.bus_id=b.bus_id
    JOIN routes r ON b.route_id=r.route_id
    ORDER BY bk.booking_id
    """)
    rows = cur.fetchall()
    if not rows:
        print("No bookings found")
    for row in rows:
        print(row)

# 7. CANCEL TICKET
def cancel_ticket():
    line()
    try:
        bid = int(input("Enter Booking ID: "))
    except ValueError:
        print("Invalid booking ID")
        return
    cur.execute("""
    UPDATE bookings SET booking_status='Cancelled'
    WHERE booking_id=%s AND booking_status='Booked'
    """,(bid,))
    con.commit()
    if cur.rowcount == 1:
        print("Ticket Cancelled Successfully")
    else:
        print("Active booking not found")

# 8. CHECK SEAT AVAILABILITY
def check_seats():
    line()
    show_buses()
    try:
        bid = int(input("Enter Bus ID: "))
    except ValueError:
        print("Invalid Bus ID")
        return
    journey = input("Journey Date (YYYY-MM-DD): ")
    try:
        date.fromisoformat(journey)
    except ValueError:
        print("Invalid date")
        return
    seats = available_seats(bid,journey)
    if seats is None:
        print("Bus not found")
    else:
        print("Available Seats:",seats)

# 9. SEARCH PASSENGER
def search_passenger():
    line()
    try:
        pid = int(input("Enter Passenger ID: "))
    except ValueError:
        print("Invalid ID")
        return
    cur.execute(
    "SELECT * FROM passengers WHERE passenger_id=%s",
    (pid,))
    row = cur.fetchone()
    if row:
        print(row)
    else:
        print("Passenger Not Found")

# 10. BOOKING SUMMARY
def booking_summary():
    line()
    cur.execute("""
    SELECT COUNT(*),COALESCE(SUM(total_fare),0)
    FROM bookings WHERE booking_status='Booked'
    """)
    count,revenue = cur.fetchone()
    print("Active Bookings:",count)
    print("Total Revenue: Rs.",revenue)


# 11. DISPLAY GRAPH
def booking_chart():
    line()
    print("BUS-WISE BOOKING CHART")

    cur.execute("""
    SELECT b.bus_number, COALESCE(SUM(bk.seats),0)
    FROM buses b LEFT JOIN bookings bk
    ON b.bus_id=bk.bus_id
    AND bk.booking_status='Booked'
    GROUP BY b.bus_id,b.bus_number
    """)

    rows = cur.fetchall()

    if not rows:
        print("No data available")
        return

    df = pd.DataFrame(
        rows,
        columns=["Bus Number", "Seats Booked"]
    )

    df["Seats Booked"] = pd.to_numeric(
        df["Seats Booked"], errors="coerce"
    ).fillna(0)

    df["Seats Booked"] = df["Seats Booked"].astype(int)

    plt.figure(figsize=(9, 5))
    plt.bar(df["Bus Number"], df["Seats Booked"])

    plt.title("APSRTC Bus Booking Analysis")
    plt.xlabel("Bus Number")
    plt.ylabel("Seats Booked")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    plt.tight_layout()
    plt.show()

# 12. MAIN MENU
def main_menu():
    while True:
        line()
        print("APSRTC BUS RESERVATION SYSTEM")
        line()
        print("1. Display Buses and Routes")
        print("2. Add Passenger")
        print("3. View Passengers")
        print("4. Book Bus Ticket")
        print("5. View Bookings")
        print("6. Cancel Ticket")
        print("7. Check Seat Availability")
        print("8. Search Passenger")
        print("9. Booking Summary")
        print("10. Display Booking Chart")
        print("0. Exit")
        line()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_buses()
        elif choice == "2":
            add_passenger()
        elif choice == "3":
            show_passengers()
        elif choice == "4":
            book_ticket()
        elif choice == "5":
            show_bookings()
        elif choice == "6":
            cancel_ticket()
        elif choice == "7":
            check_seats()
        elif choice == "8":
            search_passenger()
        elif choice == "9":
            booking_summary()
        elif choice == "10":
            booking_chart()
        elif choice == "0":
            print("Thank You")
            break
        else:
            print("Invalid Choice")

        input("\nPress Enter to continue...")

# 13. PROGRAM EXECUTION
try:
    print("Connected to APSRTC Database")
    main_menu()
except mysql.connector.Error as err:
    print("MySQL Error:",err)
finally:
    cur.close()
    con.close()
# END OF APSRTC PROJECT
# Python and MySQL Database Connectivity
# Passenger and Bus Reservation Management
# Ticket Booking and Cancellation
# Seat Availability and Fare Calculation
# Booking Analysis Using Pandas and Matplotlib
# End
