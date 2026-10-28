# COVID-19 DATA ANALYSIS SYSTEM
# CBSE Class XII Informatics Practices (065) Project
# MySQL database: covid | MySQL table: covid
# Uses mysql.connector, Pandas and Matplotlib. No SQLAlchemy.

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger",  # Replace with your actual MySQL password
        database="covid"
    )


def fetch_data(query, params=None):
    """Fetch query results using MySQL Connector, without pandas.read_sql()."""
    con = get_connection()
    try:
        cursor = con.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description] if cursor.description else []
        return pd.DataFrame(rows, columns=columns)
    finally:
        con.close()


def display_all():
    df = fetch_data(
        "SELECT report_date, location, confirmed, recovered, deaths "
        "FROM covid ORDER BY location, report_date"
    )
    if df.empty:
        print("No records found.")
        return
    df["active_cases"] = df["confirmed"] - df["recovered"] - df["deaths"]
    print("\nCOVID-19 RECORDS")
    print(df.to_string(index=False))


def search_location():
    location = input("Enter location: ").strip()
    df = fetch_data(
        """SELECT report_date, location, confirmed, recovered, deaths
           FROM covid WHERE location = %s ORDER BY report_date""",
        (location,)
    )
    if df.empty:
        print("No records found.")
        return
    df["active_cases"] = df["confirmed"] - df["recovered"] - df["deaths"]
    print(df.to_string(index=False))


def active_cases():
    df = fetch_data(
        """SELECT report_date, location, confirmed, recovered, deaths
           FROM covid ORDER BY location, report_date"""
    )
    if df.empty:
        print("No records found.")
        return
    df["active_cases"] = df["confirmed"] - df["recovered"] - df["deaths"]
    print("\nACTIVE CASES")
    print(df.to_string(index=False))


def latest_stats():
    location = input("Enter location: ").strip()
    df = fetch_data(
        """SELECT report_date, location, confirmed, recovered, deaths
           FROM covid WHERE location = %s ORDER BY report_date DESC LIMIT 1""",
        (location,)
    )
    if df.empty:
        print("No records found.")
        return
    row = df.iloc[0]
    active = row["confirmed"] - row["recovered"] - row["deaths"]
    print("\nLatest statistics for", row["location"])
    print("Date      :", row["report_date"])
    print("Confirmed :", row["confirmed"])
    print("Recovered :", row["recovered"])
    print("Deaths    :", row["deaths"])
    print("Active    :", active)


def line_graph():
    location = input("Enter location: ").strip()
    df = fetch_data(
        """SELECT report_date, confirmed FROM covid
           WHERE location = %s ORDER BY report_date""",
        (location,)
    )
    if df.empty:
        print("No records found.")
        return

    plt.plot(df["report_date"], df["confirmed"], marker="o", label="Confirmed")
    plt.title("Confirmed Cases Trend - " + location)
    plt.xlabel("Date")
    plt.ylabel("Cumulative confirmed cases")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def bar_graph():
    df = fetch_data(
        """SELECT c.report_date, c.location, c.confirmed
           FROM covid AS c
           INNER JOIN (
               SELECT location, MAX(report_date) AS latest_date
               FROM covid GROUP BY location
           ) AS latest
           ON c.location = latest.location
           AND c.report_date = latest.latest_date
           ORDER BY c.location"""
    )
    if df.empty:
        print("No records found.")
        return

    plt.bar(df["location"], df["confirmed"])
    plt.title("Confirmed Cases by Location (Latest)")
    plt.xlabel("Location")
    plt.ylabel("Cumulative confirmed cases")
    plt.tight_layout()
    plt.show()


def histogram():
    df = fetch_data("SELECT confirmed FROM covid")
    if df.empty:
        print("No records found.")
        return

    plt.hist(df["confirmed"], bins=5, edgecolor="black")
    plt.title("Distribution of Recorded Confirmed Counts")
    plt.xlabel("Cumulative confirmed cases")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()


def main():
    while True:
        print("\n===== COVID-19 DATA ANALYSIS SYSTEM =====")
        print("1. Display all records")
        print("2. Search records by location")
        print("3. Calculate active cases")
        print("4. Display latest statistics for a location")
        print("5. Line graph - confirmed cases trend")
        print("6. Bar graph - compare locations")
        print("7. Histogram - confirmed counts")
        print("8. Exit")

        try:
            choice = int(input("Enter your choice (1-8): ").strip())
        except ValueError:
            print("Please enter a number from 1 to 8.")
            continue

        try:
            if choice == 1:
                display_all()
            elif choice == 2:
                search_location()
            elif choice == 3:
                active_cases()
            elif choice == 4:
                latest_stats()
            elif choice == 5:
                line_graph()
            elif choice == 6:
                bar_graph()
            elif choice == 7:
                histogram()
            elif choice == 8:
                print("Thank you for using the COVID-19 Data Analysis System.")
                break
            else:
                print("Invalid choice. Try again.")
        except mysql.connector.Error as error:
            print("MySQL error:", error)


if __name__ == "__main__":
    main()
