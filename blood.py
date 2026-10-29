# BLOOD BANK MANAGEMENT SYSTEM
# Class XII Informatics Practices (065)
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="blood"
)
cur = con.cursor()

def add_donor():
    name = input("Donor name: ").strip()
    age = int(input("Age: "))
    group = input("Blood group (A+, A-, B+, B-, AB+, AB-, O+, O-): ").upper()
    phone = input("Phone: ").strip()
    city = input("City: ").strip()
    cur.execute("""INSERT INTO Donor
        (DonorName, Age, Phone, BloodGroup, City, RegistrationDate)
        VALUES (%s,%s,%s,%s,%s,CURDATE())""",
        (name, age, phone, group, city))
    con.commit()
    print("Donor added successfully.")

def show_donors():
    cur.execute("SELECT * FROM Donor")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=[x[0] for x in cur.description])
    print(df.to_string(index=False) if not df.empty else "No donor records.")

def donate_blood():
    donor_id = int(input("Donor ID: "))
    group = input("Blood group: ").upper()
    units = int(input("Units donated: "))
    cur.execute("SELECT BloodGroup FROM Donor WHERE DonorID=%s", (donor_id,))
    donor = cur.fetchone()
    if donor is None or donor[0] != group:
        print("Donor not found or blood group mismatch.")
        return
    cur.execute("INSERT IGNORE INTO BloodStock VALUES (%s,0)", (group,))
    cur.execute("""INSERT INTO Donation
        (DonorID, DonationDate, BloodGroup, UnitsDonated)
        VALUES (%s,CURDATE(),%s,%s)""", (donor_id, group, units))
    cur.execute("UPDATE BloodStock SET UnitsAvailable=UnitsAvailable+%s WHERE BloodGroup=%s",
                (units, group))
    con.commit()
    print("Donation recorded and stock updated.")

def show_stock():
    cur.execute("SELECT BloodGroup, UnitsAvailable FROM BloodStock ORDER BY BloodGroup")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["Blood Group", "Units Available"])
    print(df.to_string(index=False) if not df.empty else "No stock records.")
    if not df.empty:
        plt.bar(df["Blood Group"], df["Units Available"])
        plt.title("Available Blood Stock")
        plt.xlabel("Blood Group")
        plt.ylabel("Units Available")
        plt.tight_layout()
        plt.show()

def show_donations():
    cur.execute("""SELECT Donor.DonorName, Donation.DonationDate,
        Donation.BloodGroup, Donation.UnitsDonated
        FROM Donor JOIN Donation ON Donor.DonorID=Donation.DonorID""")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["Donor", "Date", "Blood Group", "Units"])
    print(df.to_string(index=False) if not df.empty else "No donation records.")
    if not df.empty:
        daily = df.groupby("Date")["Units"].sum()
        daily.plot(kind="line", marker="o")
        plt.title("Donation Trend")
        plt.xlabel("Date")
        plt.ylabel("Units Donated")
        plt.tight_layout()
        plt.show()

def register_request():
    name = input("Hospital/requester name: ").strip()
    group = input("Blood group needed: ").upper()
    units = int(input("Units required: "))
    cur.execute("INSERT IGNORE INTO BloodStock VALUES (%s,0)", (group,))
    cur.execute("""INSERT INTO BloodRequest
        (RequesterName, BloodGroup, UnitsRequested, RequestDate, Status)
        VALUES (%s,%s,%s,CURDATE(),'Pending')""", (name, group, units))
    con.commit()
    print("Request registered.")

def issue_request():
    request_id = int(input("Request ID: "))
    cur.execute("""SELECT BloodGroup, UnitsRequested, Status
        FROM BloodRequest WHERE RequestID=%s""", (request_id,))
    req = cur.fetchone()
    if req is None or req[2] != "Pending":
        print("Request not found or already issued.")
        return
    group, units, status = req
    cur.execute("SELECT UnitsAvailable FROM BloodStock WHERE BloodGroup=%s", (group,))
    stock = cur.fetchone()
    if stock is None or stock[0] < units:
        print("Insufficient blood stock.")
        return
    cur.execute("UPDATE BloodStock SET UnitsAvailable=UnitsAvailable-%s WHERE BloodGroup=%s",
                (units, group))
    cur.execute("UPDATE BloodRequest SET Status='Issued' WHERE RequestID=%s", (request_id,))
    con.commit()
    print("Request issued; stock updated.")

def show_requests():
    cur.execute("SELECT * FROM BloodRequest")
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=[x[0] for x in cur.description])
    print(df.to_string(index=False) if not df.empty else "No requests.")

def donation_histogram():
    cur.execute("SELECT UnitsDonated FROM Donation")
    rows = cur.fetchall()
    if not rows:
        print("No donation data.")
        return
    df = pd.DataFrame(rows, columns=["Units"])
    plt.hist(df["Units"], bins=5, edgecolor="black")
    plt.title("Donation Units Histogram")
    plt.xlabel("Units Donated")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()

def graph_menu():
    while True:
        print("\nGRAPH MENU")
        print("1. Line Chart - Donation Trend")
        print("2. Bar Chart - Available Blood Stock")
        print("3. Histogram - Donation Units")
        print("4. Back to Main Menu")
        choice = input("Choose graph (1-4): ")
        if choice == "1":
            show_donations()
        elif choice == "2":
            show_stock()
        elif choice == "3":
            donation_histogram()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def main():
    while True:
        print("\nBLOOD BANK MANAGEMENT SYSTEM")
        print("1. Add Donor")
        print("2. Show Donors")
        print("3. Record Donation")
        print("4. Show Stock")
        print("5. Show Donations")
        print("6. Register Request")
        print("7. Issue Request")
        print("8. Show Requests")
        print("9. Graphs (Line, Bar, Histogram)")
        print("10. Exit")
        choice = input("Enter choice: ")
        try:
            if choice == "1":
                add_donor()
            elif choice == "2":
                show_donors()
            elif choice == "3":
                donate_blood()
            elif choice == "4":
                show_stock()
            elif choice == "5":
                show_donations()
            elif choice == "6":
                register_request()
            elif choice == "7":
                issue_request()
            elif choice == "8":
                show_requests()
            elif choice == "9":
                graph_menu()
            elif choice == "10":
                break
            else:
                print("Invalid choice.")
        except (ValueError, mysql.connector.Error) as e:
            con.rollback()
            print("Error:", e)
    cur.close()
    con.close()
    print("Program closed.")

if __name__ == "__main__":
    main()
