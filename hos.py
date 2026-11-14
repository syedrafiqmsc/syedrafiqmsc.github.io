
import mysql.connector
import pandas as pd

# DATABASE CONNECTION
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="hos"
)

cur = con.cursor()

# 1. ADD PATIENT
def add_patient():
    print("\nADD NEW PATIENT")

    name = input("Patient Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    phone = input("Phone: ")
    address = input("Address: ")

    sql = """INSERT INTO patients
    (patient_name, age, gender, phone, address)
    VALUES (%s, %s, %s, %s, %s)"""

    cur.execute(sql, (name, age, gender, phone, address))
    con.commit()

    print("Patient Added Successfully!")


# 2. DISPLAY PATIENTS
def display_patients():
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()

    columns = ["Patient ID", "Name", "Age",
               "Gender", "Phone", "Address"]

    df = pd.DataFrame(rows, columns=columns)

    print("\nPATIENT DETAILS")
    print(df.to_string(index=False))


# 3. ADD DOCTOR
def add_doctor():
    print("\nADD NEW DOCTOR")

    name = input("Doctor Name: ")
    specialization = input("Specialization: ")
    phone = input("Phone: ")
    fee = float(input("Consultation Fee: "))

    sql = """INSERT INTO doctors
    (doctor_name, specialization, phone, consultation_fee)
    VALUES (%s, %s, %s, %s)"""

    cur.execute(sql, (name, specialization, phone, fee))
    con.commit()

    print("Doctor Added Successfully!")


# 4. DISPLAY DOCTORS
def display_doctors():
    cur.execute("SELECT * FROM doctors")
    rows = cur.fetchall()

    columns = ["Doctor ID", "Doctor Name",
               "Specialization", "Phone", "Fee"]

    df = pd.DataFrame(rows, columns=columns)

    print("\nDOCTOR DETAILS")
    print(df.to_string(index=False))


# 5. BOOK APPOINTMENT
def book_appointment():
    print("\nBOOK APPOINTMENT")

    patient_id = int(input("Patient ID: "))
    doctor_id = int(input("Doctor ID: "))
    date = input("Appointment Date (YYYY-MM-DD): ")
    time = input("Appointment Time (HH:MM:SS): ")

    sql = """INSERT INTO appointments
    (patient_id, doctor_id, appointment_date,
     appointment_time, status)
    VALUES (%s, %s, %s, %s, %s)"""

    cur.execute(sql, (
        patient_id, doctor_id, date, time, "Booked"
    ))

    con.commit()

    print("Appointment Booked Successfully!")


# 6. DISPLAY APPOINTMENTS
def display_appointments():
    sql = """
    SELECT
        a.appointment_id,
        p.patient_name,
        d.doctor_name,
        d.specialization,
        a.appointment_date,
        a.appointment_time,
        a.status
    FROM appointments a
    JOIN patients p
    ON a.patient_id = p.patient_id
    JOIN doctors d
    ON a.doctor_id = d.doctor_id
    ORDER BY a.appointment_id
    """

    cur.execute(sql)
    rows = cur.fetchall()

    columns = [
        "Appointment ID",
        "Patient Name",
        "Doctor Name",
        "Specialization",
        "Date",
        "Time",
        "Status"
    ]

    df = pd.DataFrame(rows, columns=columns)

    print("\nAPPOINTMENT DETAILS")
    print(df.to_string(index=False))


# 7. UPDATE APPOINTMENT STATUS
def update_status():
    aid = int(input("Enter Appointment ID: "))
    status = input("Enter New Status (Booked/Completed/Cancelled): ")

    sql = """UPDATE appointments
             SET status = %s
             WHERE appointment_id = %s"""

    cur.execute(sql, (status, aid))
    con.commit()

    if cur.rowcount > 0:
        print("Appointment Status Updated!")
    else:
        print("Appointment ID Not Found!")


# MAIN MENU
while True:

    print("\n================================")
    print("   HOSPITAL MANAGEMENT SYSTEM")
    print("================================")
    print("1. Add Patient")
    print("2. Display Patients")
    print("3. Add Doctor")
    print("4. Display Doctors")
    print("5. Book Appointment")
    print("6. Display Appointments")
    print("7. Update Appointment Status")
    print("8. Exit")

    choice = input("Enter Your Choice: ")

    try:
        if choice == '1':
            add_patient()

        elif choice == '2':
            display_patients()

        elif choice == '3':
            add_doctor()

        elif choice == '4':
            display_doctors()

        elif choice == '5':
            book_appointment()

        elif choice == '6':
            display_appointments()

        elif choice == '7':
            update_status()

        elif choice == '8':
            print("Thank You!")
            break

        else:
            print("Invalid Choice! Try Again.")

    except mysql.connector.Error as e:
        con.rollback()
        print("Database Error:", e)

    except (ValueError, TypeError):
        print("Invalid Input! Please Enter Correct Values.")

cur.close()
con.close()
