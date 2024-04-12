import psycopg2

from colorama import Fore


counter = 0
gram_list = []


class Member:

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
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}An error occurred while connecting to the database: {e}")
            return None

    def get_sessions(self, member_email):
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT s.SessionTime, t.Name
                    FROM Sessions s
                    JOIN Trainers t ON s.TrainerID = t.TrainerID
                    JOIN Members m ON s.MemberID = m.MemberID
                    WHERE m.Email = %s
                    ORDER BY s.SessionTime;
                """, (member_email,))
                sessions = cur.fetchall()
                return sessions

    def register_user(self):
        print("\nUser Registration")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        print("Select your fitness goal:")
        print("1. Gain weight")
        print("2. Maintain current weight")
        print("3. Lose weight")
        fitness_goal_choice = input("Enter your choice (1, 2, or 3): ")
        fitness_goals = None
        if fitness_goal_choice == "1":
            fitness_goals = "Gain Weight"
        elif fitness_goal_choice == "2":
            fitness_goals = "Maintain"
        elif fitness_goal_choice == "3":
            fitness_goals = "Lose Weight"
        else:
            print("Invalid choice.")
            return

        weight = input("Enter your weight (kg): ")
        height = input("Enter your height (cm): ")
        while True:
            gender = input("Enter your gender (Male/Female): ").lower()
            if gender not in ["male", "female"]:
                print("Invalid gender. Please enter 'Male' or 'Female'.")
            else:
                break
        age = input("Enter your age: ")

        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Members (Name, Email, FitnessGoals, WeightKG, HeightCM, Gender, Age)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (name, email, fitness_goals, weight, height, gender, age))
                conn.commit()
                print("User registered successfully.")
                global counter
                counter += 1

        if counter <= 10:
            print("You received a 10% discount for being one of the first 10 members for your next session.")

            while True:
                choice = input(
                    "Do you want to join our FitnessGram network? Members share their experience and progress. (yes/no): ").lower()
                if choice == "yes":
                    gram_list.append(self)
                    print("You have been added to the FitnessGram network!")
                    break
                elif choice == "no":
                    print("You chose not to join the FitnessGram network.")
                    break
                else:
                    print("Invalid choice. Please enter 'yes' or 'no'.")


    def update_profile(self):
        print("\nProfile Update")
        email = input("Enter your email: ")
        print("""
        1. Name
        2. Fitness Goals
        3. Weight (kg)
        4. Height (cm)
        5. Gender
        6. Age""")
        choice = input("Which field would you like to update? (Enter number): ")
        field_mapping = {
            "1": "Name",
            "2": "FitnessGoals",
            "3": "WeightKG",
            "4": "HeightCM",
            "5": "Gender",
            "6": "Age"
        }
        field = field_mapping.get(choice)
        if not field:
            print("Invalid choice.")
            return
        new_value = input(f"Enter new value for {field}: ")

        if field == "FitnessGoals":
            print("Select your fitness goal:")
            print("1. Gain weight")
            print("2. Maintain")
            print("3. Lose weight")
            fitness_goal_choice = input("Enter your choice (1, 2, or 3): ")
            new_value = None
            if fitness_goal_choice == "1":
                new_value = "Gain Weight"
            elif fitness_goal_choice == "2":
                new_value = "Maintain"
            elif fitness_goal_choice == "3":
                new_value = "Lose Weight"
            else:
                print("Invalid choice.")
                return

        if field == "Gender":
            new_value = new_value.lower()
            if new_value not in ["Male", "Female"]:
                print("Invalid Input.")
                return

        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"UPDATE Members SET {field} = %s WHERE Email = %s;", (new_value, email))
                conn.commit()
                print(f"{field} updated successfully.")

    def display_dashboard(self):
        email = input("\nEnter your email to view your dashboard: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT Name, FitnessGoals, WeightKG, HeightCM, Age FROM Members WHERE Email = %s;
                """, (email,))
                user_data = cur.fetchone()
                if user_data:
                    print(f"\n--- Dashboard for {user_data[0]} ---")
                    print(
                        f"Fitness Goals: {user_data[1]}\nWeight: {user_data[2]} kg\nHeight: {user_data[3]} cm\nAge: {user_data[4]}")

                    weight_kg = float(user_data[2])
                    height_cm = float(user_data[3])
                    bmi = weight_kg / ((height_cm / 100) ** 2)
                    print(f"BMI: {bmi:.2f}")

                    if bmi < 18.5:
                        category = "Underweight"
                    elif bmi < 24.9:
                        category = "Normal weight"
                    elif bmi < 29.9:
                        category = "Overweight"
                    else:
                        category = "Obesity"
                    print(f"BMI Category: {category}")

                    maintenance_calories = self.calculate_maintenance_calories(weight_kg)
                    print(f"Maintenance Calories: {maintenance_calories}")

                    if user_data[1] == 'Lose Weight':
                        maintenance_calories -= 300
                        print(f"Target Calories To Lose Weight: {maintenance_calories}")
                    elif user_data[1] == 'Gain Weight':
                        maintenance_calories += 300
                        print(f"Target Calories To Gain Weight: {maintenance_calories}")

                else:
                    print("User not found.")
                    return

                cur.execute("""
                    SELECT SessionTime, t.Name FROM Sessions s
                    JOIN Trainers t ON s.TrainerID = t.TrainerID
                    WHERE s.MemberID = (SELECT MemberID FROM Members WHERE Email = %s)
                    ORDER BY s.SessionTime;
                """, (email,))
                sessions = cur.fetchall()
                if sessions:
                    print("\nScheduled Sessions:")
                    for session in sessions:
                        print(f"{session[0]} with Trainer {session[1]}")
                else:
                    print("No scheduled sessions.")

    def calculate_maintenance_calories(self, current_weight_kg):
        current_weight_lbs = current_weight_kg * 2.20462
        maintenance_calories = current_weight_lbs * 15
        return int(maintenance_calories)

    def schedule_session(self):
        member_email = input("\nEnter your email: ")
        use_saved_card = input("Do you want to use the saved card for payment? (yes/no): ")

        is_gram_member = member_email in [member.email for member in gram_list]

        if use_saved_card.lower() == "yes":
            with self.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT CardNumber, ExpirationDate, CVV FROM Members WHERE Email = %s;
                    """, (member_email,))
                    card_details = cur.fetchone()
                    if card_details and all(card_details):
                        print("Using saved card ending in:", card_details[0][-4:])
                        card_number, expiration_date, cvv = card_details
                    else:
                        print("No saved card details found.")
                        use_saved_card = "no"

        if use_saved_card.lower() == "no":
            card_number = input("Enter your card number: ")
            expiration_date = input("Enter expiration date (MM/YY): ")
            cvv = input("Enter CVV: ")

            save_payment_info = input("Would you like to save this payment information for future use? (yes/no): ")
            if save_payment_info.lower() == "yes":
                with self.get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE Members SET CardNumber = %s, ExpirationDate = %s, CVV = %s WHERE Email = %s;
                        """, (card_number, expiration_date, cvv, member_email))
                        conn.commit()
                        print("Payment information saved successfully!")
            else:
                print("Payment information not saved.")

        desired_date = input("Enter the date for the session (YYYY-MM-DD): ")
        desired_time = input("Enter the time for the session (HH:MM): ")
        full_desired_datetime = f"{desired_date} {desired_time}"

        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MemberID FROM Members WHERE Email = %s;", (member_email,))
                member_id = cur.fetchone()
                if not member_id:
                    print("Member not found.")
                    return

                cur.execute("""
                    SELECT TrainerID, Name FROM Trainers WHERE TrainerID NOT IN (
                        SELECT TrainerID FROM Sessions WHERE SessionTime = %s
                    );
                """, (full_desired_datetime,))
                available_trainers = cur.fetchall()
                if not available_trainers:
                    print("No trainers available at this time.")
                    return

                for trainer in available_trainers:
                    print(f"TrainerID: {trainer[0]}, Name: {trainer[1]}")
                trainer_id = input("Enter TrainerID of the trainer you wish to book: ")

                if counter <= 10:
                    session_cost = 19.99 * 0.9
                else:
                    session_cost = 19.99

                cur.execute("""
                    INSERT INTO Sessions (MemberID, TrainerID, SessionTime, Cost) VALUES (%s, %s, %s, %s) RETURNING SessionID;
                """, (member_id[0], trainer_id, full_desired_datetime, session_cost))
                session_id = cur.fetchone()[0]
                conn.commit()

                self.process_payment(member_email, session_id)

                if is_gram_member:
                    self.after_session_prompt()
                    self.post_session_attendance(member_email, full_desired_datetime, trainer_id)
    def post_session_attendance(self, member_email, session_time, trainer_id):
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Name FROM Members WHERE Email = %s;", (member_email,))
                member_name = cur.fetchone()[0]

        post = f"{member_name} attended a session with TrainerID {trainer_id} at {session_time}!"
        print("Posting to FitnessGram Network:", post)

    def process_payment(self, member_email, session_id):
        print("\nSession Scheduled Successfully!")
        print("Session details:")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT t.Name, s.SessionTime FROM Sessions s
                    JOIN Trainers t ON s.TrainerID = t.TrainerID
                    WHERE s.SessionID = %s;
                """, (session_id,))
                session_details = cur.fetchone()
                if session_details:
                    print(f"Trainer: {session_details[0]}")
                    print(f"Time: {session_details[1]}")

                    cur.execute("""
                        SELECT Cost FROM Sessions WHERE SessionID = %s;
                    """, (session_id,))
                    session_cost = cur.fetchone()[0]
                    print(f"Session Cost: ${session_cost}")

                    proceed_payment = input("Would you like to proceed with the payment? (yes/no): ")
                    if proceed_payment.lower() == "yes":
                        with conn.cursor() as cur:
                            cur.execute("""
                                SELECT CardNumber, ExpirationDate, CVV FROM Members WHERE Email = %s;
                            """, (member_email,))
                            card_details = cur.fetchone()
                            if card_details and all(card_details):
                                print("Using saved card ending in:", card_details[0][-4:])
                                print("Payment processed successfully!")
                            else:
                                print("No saved card details found. Please enter payment information.")
                    else:
                        print("Payment cancelled.")
                else:
                    print("Session details not found.")


