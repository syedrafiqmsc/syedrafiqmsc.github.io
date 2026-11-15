
# SPORTS MANAGEMENT SYSTEM
# Python + MySQL + Matplotlib

import mysql.connector
import matplotlib.pyplot as plt

# DATABASE CONNECTION

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="sports"
)

cur = con.cursor()

# 1. DISPLAY PLAYERS

def display_players():
    cur.execute("SELECT * FROM players")
    print("\nPLAYER DETAILS")
    print("-" * 65)
    for row in cur.fetchall():
        print(row)

# 2. DISPLAY TEAMS

def display_teams():
    cur.execute("SELECT * FROM teams")
    print("\nTEAM DETAILS")
    for row in cur.fetchall():
        print(row)

# 3. DISPLAY EVENTS

def display_events():
    cur.execute("SELECT * FROM events")
    print("\nSPORTS EVENTS")
    for row in cur.fetchall():
        print(row)

# 4. DISPLAY MATCHES

def display_matches():
    cur.execute("SELECT * FROM matches")
    print("\nMATCH SCHEDULE")
    for row in cur.fetchall():
        print(row)

# 5. DISPLAY RESULTS

def display_results():
    cur.execute("SELECT * FROM results")
    print("\nMATCH RESULTS")
    for row in cur.fetchall():
        print(row)

# 6. ADD PLAYER

def add_player():
    pid = int(input("Player ID: "))
    name = input("Player Name: ")
    age = int(input("Age: "))
    gender = input("Gender: ")
    tid = int(input("Team ID: "))

    q = "INSERT INTO players VALUES(%s,%s,%s,%s,%s)"
    cur.execute(q, (pid, name, age, gender, tid))
    con.commit()
    print("Player Added Successfully")

# 7. ADD TEAM

def add_team():
    tid = int(input("Team ID: "))
    name = input("Team Name: ")
    coach = input("Coach Name: ")
    sport = input("Sport: ")

    q = "INSERT INTO teams VALUES(%s,%s,%s,%s)"
    cur.execute(q, (tid, name, coach, sport))
    con.commit()
    print("Team Added Successfully")

# 8. ADD EVENT

def add_event():
    eid = int(input("Event ID: "))
    name = input("Event Name: ")
    sport = input("Sport: ")
    date = input("Event Date (YYYY-MM-DD): ")
    venue = input("Venue: ")

    q = "INSERT INTO events VALUES(%s,%s,%s,%s,%s)"
    cur.execute(q, (eid, name, sport, date, venue))
    con.commit()
    print("Event Added Successfully")

# 9. ADD MATCH AND RESULT

def add_match():
    mid = int(input("Match ID: "))
    t1 = int(input("Team 1 ID: "))
    t2 = int(input("Team 2 ID: "))
    eid = int(input("Event ID: "))
    date = input("Match Date (YYYY-MM-DD): ")
    venue = input("Venue: ")

    q = "INSERT INTO matches VALUES(%s,%s,%s,%s,%s,%s)"
    cur.execute(q, (mid, t1, t2, eid, date, venue))
    con.commit()
    print("Match Scheduled Successfully")

    choice = input("Enter Result Now? (y/n): ")

    if choice.lower() == 'y':
        add_result(mid)

def add_result(mid=None):
    if mid is None:
        mid = int(input("Match ID: "))

    cur.execute(
        "SELECT t1.team_name,t2.team_name "
        "FROM matches m JOIN teams t1 ON m.team1_id=t1.team_id "
        "JOIN teams t2 ON m.team2_id=t2.team_id "
        "WHERE m.match_id=%s", (mid,))

    teams = cur.fetchone()

    if teams is None:
        print("Match Not Found")
        return

    rid = int(input("Result ID: "))
    s1 = int(input("Team 1 Score: "))
    s2 = int(input("Team 2 Score: "))

    if s1 > s2:
        winner = teams[0]
    elif s2 > s1:
        winner = teams[1]
    else:
        winner = "Draw"

    q = "INSERT INTO results VALUES(%s,%s,%s,%s,%s)"
    cur.execute(q, (rid, mid, s1, s2, winner))
    con.commit()
    print("Winner:", winner)

# 10. SPORTS ANALYSIS CHARTS

def sports_chart():
    print("\n1. Team Wise Players")
    print("2. Match Score Analysis")
    print("3. Sport Wise Teams")

    ch = input("Enter Chart Choice: ")

    if ch == '1':
        cur.execute(
            "SELECT t.team_name,COUNT(p.player_id) "
            "FROM teams t LEFT JOIN players p "
            "ON t.team_id=p.team_id "
            "GROUP BY t.team_id,t.team_name")

        rows = cur.fetchall()

        names = [r[0] for r in rows]
        totals = [r[1] for r in rows]

        plt.bar(names, totals)
        plt.title("Team Wise Players")
        plt.xlabel("Teams")
        plt.ylabel("Players")

    elif ch == '2':
        cur.execute(
            "SELECT match_id,team1_score,team2_score "
            "FROM results")

        rows = cur.fetchall()

        ids = [str(r[0]) for r in rows]
        s1 = [r[1] for r in rows]
        s2 = [r[2] for r in rows]

        x = range(len(ids))

        plt.bar(x, s1, width=0.4, label="Team 1")
        plt.bar([i+0.4 for i in x], s2,
                width=0.4, label="Team 2")

        plt.xticks([i+0.2 for i in x], ids)
        plt.legend()
        plt.title("Match Score Analysis")
        plt.xlabel("Match ID")
        plt.ylabel("Scores")

    elif ch == '3':
        cur.execute(
            "SELECT sport,COUNT(*) FROM teams GROUP BY sport")

        rows = cur.fetchall()

        sports = [r[0] for r in rows]
        totals = [r[1] for r in rows]

        plt.bar(sports, totals)
        plt.title("Sport Wise Teams")
        plt.xlabel("Sports")
        plt.ylabel("Number of Teams")

    else:
        print("Invalid Chart Choice")
        return

    plt.tight_layout()
    plt.show()

# MAIN MENU - ONLY 10 CHOICES

def main_menu():

    while True:

        print("\n==============================")
        print("   SPORTS MANAGEMENT SYSTEM")
        print("==============================")
        print("1. Display Players")
        print("2. Display Teams")
        print("3. Display Events")
        print("4. Display Matches")
        print("5. Display Results")
        print("6. Add Player")
        print("7. Add Team")
        print("8. Add Event")
        print("9. Add Match and Result")
        print("10. Sports Analysis Charts")
        print("0. Exit")

        ch = input("Enter Your Choice: ")

        try:
            if ch == '1':
                display_players()
            elif ch == '2':
                display_teams()
            elif ch == '3':
                display_events()
            elif ch == '4':
                display_matches()
            elif ch == '5':
                display_results()
            elif ch == '6':
                add_player()
            elif ch == '7':
                add_team()
            elif ch == '8':
                add_event()
            elif ch == '9':
                add_match()
            elif ch == '10':
                sports_chart()
            elif ch == '0':
                print("Thank You")
                break
            else:
                print("Invalid Choice")

        except mysql.connector.Error as e:
            con.rollback()
            print("Database Error:", e)

        except ValueError:
            print("Enter Valid Numeric Values")

# RUN PROGRAM

try:
    main_menu()

finally:
    cur.close()
    con.close()
    print("Database Connection Closed")
