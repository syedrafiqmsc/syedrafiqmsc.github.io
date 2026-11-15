
# IPL AND T20 CRICKET DATA ANALYSIS SYSTEM

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# 1. MYSQL CONNECTION

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="ipl"
)

cur = con.cursor()

print("IPL DATABASE CONNECTED SUCCESSFULLY")


# 2. FUNCTION TO READ MYSQL DATA

def get_data(q):
    cur.execute(q)
    records = cur.fetchall()
    columns = [i[0] for i in cur.description]
    return pd.DataFrame(records, columns=columns)


# 3. DISPLAY TEAMS

def show_teams():
    df = get_data("SELECT * FROM teams")
    print(df.to_string(index=False))


# 4. DISPLAY PLAYERS

def show_players():
    q = """SELECT p.player_name,t.team_code,
           p.player_role FROM players p
           JOIN teams t ON p.team_id=t.team_id"""
    df = get_data(q)
    print(df.to_string(index=False))


# 5. DISPLAY MATCH DETAILS

def show_matches():
    q = """SELECT m.match_id,m.match_date,
           t1.team_code AS Team1,m.team1_runs,
           t2.team_code AS Team2,m.team2_runs,
           w.team_code AS Winner
           FROM matches m
           JOIN teams t1 ON m.team1_id=t1.team_id
           JOIN teams t2 ON m.team2_id=t2.team_id
           JOIN teams w ON m.winner_team_id=w.team_id"""
    df = get_data(q)
    print(df.to_string(index=False))


# 6. TEAM WISE TOTAL RUNS

def team_runs():
    q = """SELECT t.team_code,
           SUM(b.runs) AS Total_Runs
           FROM teams t JOIN players p
           ON t.team_id=p.team_id
           JOIN batting b ON p.player_id=b.player_id
           GROUP BY t.team_code"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="team_code",y="Total_Runs",
            kind="bar",legend=False)
    plt.title("Team Wise Total Runs")
    plt.xlabel("IPL Teams")
    plt.ylabel("Runs")
    plt.tight_layout()
    plt.show()


# 7. TOP RUN SCORERS

def top_batsmen():
    q = """SELECT p.player_name,
           SUM(b.runs) AS Total_Runs
           FROM batting b JOIN players p
           ON b.player_id=p.player_id
           GROUP BY p.player_id,p.player_name
           ORDER BY Total_Runs DESC"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="player_name",y="Total_Runs",
            kind="bar",legend=False)
    plt.title("Top Run Scorers")
    plt.xlabel("Players")
    plt.ylabel("Runs")
    plt.tight_layout()
    plt.show()


# 8. TOP WICKET TAKERS

def top_bowlers():
    q = """SELECT p.player_name,
           SUM(b.wickets) AS Total_Wickets
           FROM bowling b JOIN players p
           ON b.player_id=p.player_id
           GROUP BY p.player_id,p.player_name
           ORDER BY Total_Wickets DESC"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="player_name",y="Total_Wickets",
            kind="bar",legend=False)
    plt.title("Top Wicket Takers")
    plt.xlabel("Players")
    plt.ylabel("Wickets")
    plt.tight_layout()
    plt.show()


# 9. MATCH SCORE COMPARISON

def match_scores():
    q = """SELECT match_id,team1_runs,team2_runs
           FROM matches ORDER BY match_id"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="match_id",
            y=["team1_runs","team2_runs"],
            kind="line",marker="o")
    plt.title("Match Score Comparison")
    plt.xlabel("Match Number")
    plt.ylabel("Runs")
    plt.legend(["Team 1","Team 2"])
    plt.tight_layout()
    plt.show()


# 10. TEAM WISE MATCH WINS

def team_wins():
    q = """SELECT t.team_code,
           COUNT(m.match_id) AS Total_Wins
           FROM teams t LEFT JOIN matches m
           ON t.team_id=m.winner_team_id
           GROUP BY t.team_id,t.team_code"""
    df = get_data(q)
    print(df.to_string(index=False))

    df.plot(x="team_code",y="Total_Wins",
            kind="bar",legend=False)
    plt.title("Team Wise Match Wins")
    plt.xlabel("IPL Teams")
    plt.ylabel("Wins")
    plt.tight_layout()
    plt.show()


# 11. BATTING STATISTICS

def batting_details():
    q = """SELECT p.player_name,
           SUM(b.runs) AS Runs,
           SUM(b.balls) AS Balls,
           SUM(b.fours) AS Fours,
           SUM(b.sixes) AS Sixes
           FROM batting b JOIN players p
           ON b.player_id=p.player_id
           GROUP BY p.player_id,p.player_name"""
    df = get_data(q)
    print(df.to_string(index=False))


# 12. BOWLING STATISTICS

def bowling_details():
    q = """SELECT p.player_name,
           SUM(b.overs) AS Overs,
           SUM(b.runs_conceded) AS Runs,
           SUM(b.wickets) AS Wickets
           FROM bowling b JOIN players p
           ON b.player_id=p.player_id
           GROUP BY p.player_id,p.player_name"""
    df = get_data(q)
    print(df.to_string(index=False))


# 13. DISPLAY ALL REPORTS

def all_reports():
    print("\nTEAM DETAILS")
    show_teams()

    print("\nPLAYER DETAILS")
    show_players()

    print("\nMATCH DETAILS")
    show_matches()

    print("\nBATTING DETAILS")
    batting_details()

    print("\nBOWLING DETAILS")
    bowling_details()

    print("\nTEAM PERFORMANCE")
    team_runs()

    print("\nPLAYER PERFORMANCE")
    top_batsmen()
    top_bowlers()

    print("\nMATCH ANALYSIS")
    match_scores()
    team_wins()


# 14. MAIN MENU

def main_menu():

    while True:

        print("\n" + "=" * 40)
        print(" IPL CRICKET DATA ANALYSIS SYSTEM")
        print("=" * 40)

        print("1. Display Teams")
        print("2. Display Players")
        print("3. Display Match Details")
        print("4. Team Wise Total Runs")
        print("5. Top Run Scorers")
        print("6. Top Wicket Takers")
        print("7. Match Score Comparison")
        print("8. Team Wise Match Wins")
        print("9. Batting Statistics")
        print("10. Bowling Statistics")
        print("11. Display All Reports")
        print("0. Exit")

        ch = input("\nEnter Your Choice: ")

        if ch == "1":
            show_teams()

        elif ch == "2":
            show_players()

        elif ch == "3":
            show_matches()

        elif ch == "4":
            team_runs()

        elif ch == "5":
            top_batsmen()

        elif ch == "6":
            top_bowlers()

        elif ch == "7":
            match_scores()

        elif ch == "8":
            team_wins()

        elif ch == "9":
            batting_details()

        elif ch == "10":
            bowling_details()

        elif ch == "11":
            all_reports()

        elif ch == "0":
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")


# 15. START PROGRAM

try:
    main_menu()

except Exception as e:
    print("Error:", e)

finally:
    if con.is_connected():
        cur.close()
        con.close()
        print("MySQL Connection Closed")
