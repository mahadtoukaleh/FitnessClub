import subprocess
import psycopg2
from colorama import Fore, Style
from Admin import Admin
from Member import Member
from Trainer import Trainer

Fore.BLUE, Fore.RED, Fore.GREEN

DB_PARAMS = {
    'dbname': 'healthclub',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        print(f"{Fore.RED}An error occurred while connecting to the database: {e}{Style.RESET_ALL}")
        return None

def fitness_gram_terminal():
    subprocess.run(["start", "cmd", "/k", "python", "fitness_gram_feed.py"], shell=True)

def display_main_menu():
    print(f"\n{Fore.YELLOW}Main Menu{Style.RESET_ALL}")
    print("---------")
    print("1. Register User")
    printe("2. Update Profile")
    print("3. View Dashboard")
    print("4. Schedule Session")
    print("5. Set Trainer Availability")
    print("6. View Membr Profile")
    print("0. Exit")

    choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
    return choice

def member_main_menu():
    print(f"\n{Fore.LIGHTGREEN_EX}Member Main Menu{Style.RESET_ALL}")
    print("----------------")
    print("1. Register as a New Member!")
    print("2. Update Profile")
    print("3. View Dashboard")
    print("4. Schedule Session")
    print("5. FitnessGram")
    print("0. Back")

    choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
    return choice

def trainer_main_menu():
    print(f"\n{Fore.YELLOW}Trainer Main Menu{Style.RESET_ALL}")
    print("-----------------")
    print("1. Set Availability")
    print("2. View Scheduled Sessions")
    print("0. Back")

    choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
    return choice

def role_selection():
    print(f"\n{Fore.GREEN}Welcome to the Health Club Management System{Style.RESET_ALL}")
    print("-------------------------------------------")
    print(f"1. Member\n2. Trainer\n3. Manager (Admin)")

    role = input(f"{Fore.YELLOW}Select your role (1 for Member, 2 for Trainer, 3 for Manager):{Style.RESET_ALL}")
    return role

def authenticate_manager(username, password):
    attempts = 0
    while attempts < 3:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM Admins WHERE username = %s AND password = %s;", (username, password))
                admin = cur.fetchone()
                if admin:
                    print(f"{Fore.GREEN}Authentication successful. {Style.RESET_ALL}")
                    return True
                else:
                    print(f"{Fore.RED}Authentication failed. Please try again.{Style.RESET_ALL}")
                    attempts += 1
                    password = input(f"{Fore.YELLOW}Enter manager password: {Style.RESET_ALL}")
    print(f"{Fore.RED}Maximum number of attempts reached. Access denied.{Style.RESET_ALL}")
    return False

def admin_main_menu():
    print(f"\n{Fore.YELLOW}Admin Main Menu{Style.RESET_ALL}")
    print("----------------")
    print("1. Manage Room Bookings")
    print("2. Manage Equipment Maintenance")
    print("3. Update Class Schedule")
    print("4. Process Billing and Payment")
    print("0. Back")

    choice = input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
    return choice

def main():
    while True:
        role = role_selection()
        if role == "1":
            member = Member()
            while True:
                choice = member_main_menu()
                if choice == "1":
                    member.register_user()
                elif choice == "2":
                    member.update_profile()
                elif choice == "3":
                    member.display_dashboard()
                elif choice == "4":
                    member.schedule_session()
                elif choice == "5":
                    fitness_gram_terminal()
                elif choice == "0":
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        elif role == "2":
            trainer = Trainer()
            while True:
                choice = trainer_main_menu()
                if choice == "1":
                    trainer.set_availability()
                elif choice == "2":
                    trainer.view_members()
                elif choice == "0":
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        elif role == "3":
            manager_username = input(f"{Fore.YELLOW}Enter manager username: {Style.RESET_ALL}")
            manager_password = input(f"{Fore.YELLOW}Enter manager password: {Style.RESET_ALL}")
            if authenticate_manager(manager_username, manager_password):
                admin = Admin()
                while True:
                    choice = admin_main_menu()
                    if choice == "1":
                        admin.manage_room_bookings()
                    elif choice == "2":
                        admin.manage_equipment_maintenance()
                    elif choice == "3":
                        admin.update_class_schedule()
                    elif choice == "4":
                        admin.process_billing_and_payment()
                    elif choice == "0":
                        break
                    else:
                        print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Authentication failed. Access denied.{Style.RESET_ALL}")
        elif role == "0":
            print(f"{Fore.GREEN}Thank you for using the Health Club Management System. Have a great day!{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Invalid role selected. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
