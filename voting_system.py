import mysql.connector

# 🔗 DATABASE CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="voting_system"
)

cursor = conn.cursor()

# 🌍 STATE OPTIONS
states = ["Gujarat", "Maharashtra", "Rajasthan", "Delhi"]

# 🔐 REGISTER (WITH STATE)
def register():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    print("\n🌍 Select Your State:")
    for i, state in enumerate(states, start=1):
        print(f"{i}. {state}")

    try:
        state_choice = int(input("Enter state number: "))
        if state_choice not in range(1, len(states)+1):
            print("❌ Invalid state selection!")
            return
    except ValueError:
        print("❌ Invalid input!")
        return

    selected_state = states[state_choice - 1]

    try:
        query = "INSERT INTO users (username, password, state) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, selected_state))
        conn.commit()
        print("✅ Registration Successful!")
    except mysql.connector.IntegrityError:
        print("❌ Username already exists!")

# 🔑 LOGIN
def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user:
        print(f"✅ Login Successful! (State: {user[4]})")
        return user
    else:
        print("❌ Invalid Credentials")
        return None

# 🗳️ VOTE FUNCTION
def vote(user):
    if user[3]:  # has_voted
        print("❌ You have already voted!")
        return

    print("\n🗳️ Choose Party:")
    print("1. BJP")
    print("2. Congress")
    print("3. AAP")
    print("4. Other")

    try:
        choice = int(input("Enter your choice (1-4): "))
    except ValueError:
        print("❌ Invalid input!")
        return

    if choice not in [1, 2, 3, 4]:
        print("❌ Invalid choice!")
        return

    try:
        cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE id=%s", (choice,))
        cursor.execute("UPDATE users SET has_voted=TRUE WHERE id=%s", (user[0],))
        conn.commit()
        print("✅ Vote Submitted Successfully!")
    except Exception as e:
        print("❌ Error while voting:", e)

# 📊 RESULTS
def show_results():
    cursor.execute("SELECT name, votes FROM candidates")
    results = cursor.fetchall()

    if not results:
        print("❌ No candidates found.")
        return

    print("\n📊 Voting Results:")
    for name, votes in results:
        print(f"{name} : {votes} votes")

# 🏆 WINNER
def show_winner():
    cursor.execute("SELECT name, votes FROM candidates ORDER BY votes DESC LIMIT 1")
    winner = cursor.fetchone()

    if winner is None:
        print("❌ No candidates available.")
    elif winner[1] == 0:
        print("⚠️ No votes cast yet.")
    else:
        print(f"\n🏆 Winner: {winner[0]} with {winner[1]} votes")

# 🌍 SHOW USERS BY STATE (NEW FEATURE 🔥)
def show_users_by_state():
    print("\n🌍 Select State:")
    for i, state in enumerate(states, start=1):
        print(f"{i}. {state}")

    try:
        choice = int(input("Enter state number: "))
        if choice not in range(1, len(states)+1):
            print("❌ Invalid choice!")
            return
    except ValueError:
        print("❌ Invalid input!")
        return

    selected_state = states[choice - 1]

    cursor.execute("SELECT username FROM users WHERE state=%s", (selected_state,))
    users = cursor.fetchall()

    print(f"\n👥 Users from {selected_state}:")
    if users:
        for u in users:
            print(u[0])
    else:
        print("No users found.")

# 🔁 MAIN MENU
while True:
    print("\n===== VOTING SYSTEM =====")
    print("1. Register")
    print("2. Login & Vote")
    print("3. Show Results")
    print("4. Show Winner")
    print("5. Show Users by State 🌍")
    print("6. Exit")

    choice = input("Enter choice: ").strip()

    if choice == "1":
        register()

    elif choice == "2":
        user = login()
        if user:
            vote(user)

    elif choice == "3":
        show_results()

    elif choice == "4":
        show_winner()

    elif choice == "5":
        show_users_by_state()

    elif choice == "6":
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid option")

# 🔚 CLOSE CONNECTION
cursor.close()
conn.close()