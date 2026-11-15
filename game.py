
# COMPUTER GAME DEVELOPMENT SYSTEM
# Python + MySQL
# WITHOUT PYGAME

import mysql.connector
import random
import time

# DATABASE CONNECTION

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="game"
)

cur = db.cursor()

# PLAYER REGISTRATION

name = input("Enter Player Name: ")

cur.execute(
    "INSERT INTO players(player_name) VALUES(%s)",
    (name,)
)

db.commit()
player_id = cur.lastrowid


# SAVE SCORE

def save_score(game_id, score):
    cur.execute(
        "INSERT INTO game_scores(player_id,game_id,score) VALUES(%s,%s,%s)",
        (player_id, game_id, score)
    )
    db.commit()
    print("\nScore saved successfully!")


# 1. SNAKE GAME

def snake_game():
    print("\n===== SNAKE GAME =====")
    print("Collect food and avoid obstacles.")
    print("Use W, A, S, D keys.")

    score = 0
    snake = 5
    food = 10

    while True:
        print("\nSnake Length:", snake)
        print("Score:", score)

        move = input("Move (W/A/S/D or Q): ").upper()

        if move == "Q":
            break

        if move in ["W", "A", "S", "D"]:
            chance = random.randint(1, 5)

            if chance <= 3:
                print("Food collected!")
                score += food
                snake += 1
            else:
                print("Snake hit an obstacle!")
                break
        else:
            print("Invalid move!")

    print("Final Score:", score)
    save_score(1, score)


# 2. CAR RACING GAME

def car_game():
    print("\n===== CAR RACING GAME =====")
    print("Avoid enemy cars.")
    print("Press L for Left, R for Right.")

    score = 0
    distance = 0

    while True:
        print("\nDistance:", distance)
        print("Score:", score)

        move = input("Choose L/R or Q: ").upper()

        if move == "Q":
            break

        if move not in ["L", "R"]:
            print("Invalid move!")
            continue

        enemy = random.choice(["L", "R"])

        if move == enemy:
            print("CRASH! You hit an enemy car.")
            break

        print("Safe driving!")
        score += 10
        distance += 100

    print("Final Score:", score)
    save_score(2, score)


# 3. SPACE SHOOTER GAME

def space_game():
    print("\n===== SPACE SHOOTER GAME =====")
    print("Shoot enemies using SPACE.")
    print("Avoid enemy attacks.")

    score = 0

    for i in range(1, 11):
        print("\nEnemy Number:", i)

        action = input("Press S to shoot or Q to quit: ").upper()

        if action == "Q":
            break

        if action == "S":
            hit = random.randint(1, 4)

            if hit <= 3:
                print("Enemy destroyed!")
                score += 10
            else:
                print("Enemy escaped!")
        else:
            print("Invalid action!")

    print("Final Score:", score)
    save_score(3, score)


# 4. QUIZ GAME

def quiz_game():
    print("\n===== QUIZ GAME =====")

    cur.execute("SELECT * FROM quiz_questions ORDER BY RAND()")
    questions = cur.fetchall()

    score = 0

    for q in questions:
        print("\n", q[1])
        print("A.", q[2])
        print("B.", q[3])
        print("C.", q[4])
        print("D.", q[5])

        answer = input("Enter answer: ").upper()

        if answer == q[6]:
            print("Correct Answer!")
            score += 10
        else:
            print("Wrong Answer!")
            print("Correct Answer:", q[6])

    print("\nTotal Score:", score)
    save_score(4, score)


# 5. BRICK BREAKER GAME

def brick_game():
    print("\n===== BRICK BREAKER GAME =====")
    print("Break bricks using the ball.")
    print("Choose L, R or S.")

    score = 0
    bricks = 10

    while bricks > 0:
        print("\nBricks Remaining:", bricks)
        print("Score:", score)

        move = input("Move paddle (L/R/S or Q): ").upper()

        if move == "Q":
            break

        if move not in ["L", "R", "S"]:
            print("Invalid move!")
            continue

        hit = random.randint(1, 3)

        if hit == 1:
            print("Ball missed the bricks!")
        else:
            print("Brick broken!")
            bricks -= 1
            score += 10

    print("Final Score:", score)
    save_score(5, score)


# VIEW PLAYER SCORES

def view_scores():
    cur.execute(
        """SELECT g.game_name, s.score, s.play_date
        FROM game_scores s
        JOIN game_master g ON s.game_id=g.game_id
        WHERE s.player_id=%s
        ORDER BY s.score DESC""",
        (player_id,)
    )

    records = cur.fetchall()

    print("\n===== MY GAME SCORES =====")

    for record in records:
        print(record[0], "| Score:", record[1],
              "| Date:", record[2])

    if not records:
        print("No scores available.")


# MAIN MENU

def main_menu():

    while True:

        print("\n================================")
        print(" COMPUTER GAME DEVELOPMENT SYSTEM")
        print("================================")
        print("Player:", name)
        print("1. Snake Game")
        print("2. Car Racing Game")
        print("3. Space Shooter Game")
        print("4. Quiz Game")
        print("5. Brick Breaker Game")
        print("6. View My Scores")
        print("0. Exit")
        print("================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            snake_game()

        elif choice == "2":
            car_game()

        elif choice == "3":
            space_game()

        elif choice == "4":
            quiz_game()

        elif choice == "5":
            brick_game()

        elif choice == "6":
            view_scores()

        elif choice == "0":
            print("Thank you for playing!")
            break

        else:
            print("Invalid choice! Try again.")


# START PROGRAM

try:
    main_menu()

finally:
    cur.close()
    db.close()
