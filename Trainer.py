from datetime import datetime
import psycopg2
import re

class Trainer:
    def __init__(self):
        self.db_params = {
            'dbname': 'healthclub',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost'
        }

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(**self.db_params)
            return conn
        except psycopg2.Error as e:
            print(f"An error occurred while connecting to the database: {e}")
            return None

    def is_valid_trainer_id(self, trainer_id):
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM Trainer WHERE TrainerID = %s;", (trainer_id,))
                count = cur.fetchone()[0]
                return count > 0

    def set_availability(self):
        try:
            trainer_id = input("\nEnter your Trainer ID: ")
            if not self.is_valid_trainer_id(trainer_id):
                print("Invalid Trainer ID.")
                return

            available_date = input("Enter the date you're available (YYYY-MM-DD): ")
            if not re.match(r'\d{4}-\d{2}-\d{2}', available_date):
                print("Invalid date format. Please enter date in YYYY-MM-DD format.")
                return

            start_time = input("Enter your start time (HH:MM): ")
            if not re.match(r'\d{2}:\d{2}', start_time):
                print("Invalid time format. Please enter time in HH:MM format.")
                return

            end_time = input("Enter your end time (HH:MM): ")
            if not re.match(r'\d{2}:\d{2}', end_time):
                print("Invalid time format. Please enter time in HH:MM format.")
                return

            start_datetime = datetime.strptime(f"{available_date} {start_time}", "%Y-%m-%d %H:%M")
            end_datetime = datetime.strptime(f"{available_date} {end_time}", "%Y-%m-%d %H:%M")
            if start_datetime >= end_datetime:
                print("End time must be later than start time.")
                return

            with self.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO TrainerAvailability (TrainerID, AvailableDate, Start, End) VALUES (%s, %s, %s, %s);
                    """, (trainer_id, available_date, start_time, end_time))
                    conn.commit()
                    print("Availability set successfully.")
        except psycopg2.Error as e:
            print(f"An error occurred while setting availability: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def view_members(self):
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT Name, Email FROM Members;")
                    members = cur.fetchall()
                    print("List of Members:")
                    for member in members:
                        print(f"Name: {member[0]}, Email: {member[1]}")
        except psycopg2.Error as e:
            print(f"An error occurred while fetching members: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

