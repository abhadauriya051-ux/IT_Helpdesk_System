# IT Helpdesk System V15 (Upgraded with User Management)
# CLI Ticketing System with User Creation Feature

import datetime

# -------------------- Data Storage --------------------
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"}
}

tickets = []
current_user = None

# -------------------- AUTH --------------------
def login():
    global current_user
    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    if username in users and users[username]["password"] == password:
        current_user = username
        print(f"Login successful. Welcome {username}!")
        return True
    else:
        print("Invalid credentials")
        return False

# -------------------- USER MANAGEMENT --------------------
def create_user():
    if users[current_user]["role"] != "admin":
        print("Only admin can create users")
        return

    print("\n=== CREATE NEW USER ===")
    username = input("Enter new username: ")

    if username in users:
        print("User already exists")
        return

    password = input("Enter password: ")
    role = input("Enter role (admin/user): ")

    users[username] = {
        "password": password,
        "role": role
    }

    print(f"User {username} created successfully!")

# -------------------- TICKETS --------------------
def create_ticket():
    title = input("Enter issue title: ")
    desc = input("Enter issue description: ")

    ticket = {
        "id": len(tickets) + 1,
        "title": title,
        "description": desc,
        "status": "Open",
        "created_by": current_user,
        "assigned_to": None,
        "created_at": str(datetime.datetime.now())
    }

    tickets.append(ticket)
    print(f"Ticket #{ticket['id']} created successfully!")


def view_tickets():
    print("\n=== ALL TICKETS ===")
    for t in tickets:
        print(f"ID: {t['id']} | {t['title']} | {t['status']} | By: {t['created_by']}")


def my_tickets():
    print("\n=== MY TICKETS ===")
    for t in tickets:
        if t["created_by"] == current_user:
            print(f"ID: {t['id']} | {t['title']} | {t['status']}")


def update_ticket_status():
    if users[current_user]["role"] != "admin":
        print("Only admin can update ticket status")
        return

    tid = int(input("Enter Ticket ID: "))

    for t in tickets:
        if t["id"] == tid:
            t["status"] = input("Enter new status (Open/In Progress/Closed): ")
            print("Ticket updated")
            return

    print("Ticket not found")

# -------------------- MENU --------------------
def menu():
    while True:
        print("\n\n===== IT HELP DESK V15 =====")
        print("1. Create Ticket")
        print("2. My Tickets")
        print("3. View All Tickets (Admin)")
        print("4. Update Ticket (Admin)")
        print("5. Create User (Admin)")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            my_tickets()
        elif choice == "3":
            view_tickets()
        elif choice == "4":
            update_ticket_status()
        elif choice == "5":
            create_user()
        elif choice == "6":
            break
        else:
            print("Invalid choice")

# -------------------- MAIN --------------------
if __name__ == "__main__":
    print("Welcome to IT Helpdesk System V15")
    if login():
        menu()
