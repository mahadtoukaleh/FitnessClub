import psycopg2


class Admin:
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
            print(f"An error occurred while connecting to the database: {e}")
            return None

    def view_member_profile(self):
        search_name = input("\nEnter the name of the member to search for: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT Name, Email, FitnessGoals, WeightKG, HeightCM, Age FROM Members WHERE Name ILIKE %s;
                """, ('%' + search_name + '%',))
                profiles = cur.fetchall()
                if profiles:
                    print("\nFound Member Profiles:")
                    for profile in profiles:
                        print(f"""
    Name: {profile[0]}
    Email: {profile[1]}
    Fitness Goals: {profile[2]}
    Weight: {profile[3]} kg
    Height: {profile[4]} cm
    Age: {profile[5]} years""")
                else:
                    print("No profiles found.")

    def manage_room_bookings(self):
        print("\nRoom Booking Management")
        print("1. View All Rooms")
        print("2. Add New Room")
        print("3. Update Room Details")
        print("4. Delete Room")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.view_all_rooms()
        elif choice == "2":
            self.add_new_room()
        elif choice == "3":
            self.update_room_details()
        elif choice == "4":
            self.delete_room()
        else:
            print("Invalid choice. Please try again.")

    def view_all_rooms(self):
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM Rooms;")
                rooms = cur.fetchall()
                if rooms:
                    print("\nAll Rooms:")
                    for room in rooms:
                        print(f"Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}, Status: {room[3]}")
                else:
                    print("No rooms found.")

    def add_new_room(self):
        name = input("Enter the name of the new room: ")
        capacity = input("Enter the capacity of the new room: ")
        status = input("Enter the status of the new room (e.g., available, occupied): ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Rooms (Name, Capacity, Status) VALUES (%s, %s, %s);", (name, capacity, status))
                conn.commit()
                print("Room added successfully.")

    def update_room_details(self):
        room_id = input("Enter the ID of the room to update: ")
        new_name = input("Enter the new name for the room: ")
        new_capacity = input("Enter the new capacity for the room: ")
        new_status = input("Enter the new status for the room: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Rooms SET Name = %s, Capacity = %s, Status = %s WHERE RoomID = %s;",
                            (new_name, new_capacity, new_status, room_id))
                conn.commit()
                print("Room details updated successfully.")

    def delete_room(self):
        room_id = input("Enter the ID of the room to delete: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Rooms WHERE RoomID = %s;", (room_id,))
                conn.commit()
                print("Room deleted successfully.")

    def manage_equipment_maintenance(self):
        print("\nEquipment Maintenance Management")
        print("1. View All Equipment")
        print("2. Add New Equipment")
        print("3. Update Equipment Details")
        print("4. Delete Equipment")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.view_all_equipment()
        elif choice == "2":
            self.add_new_equipment()
        elif choice == "3":
            self.update_equipment_details()
        elif choice == "4":
            self.delete_equipment()
        else:
            print("Invalid choice. Please try again.")

    def view_all_equipment(self):
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM Equipment;")
                equipment = cur.fetchall()
                if equipment:
                    print("\nAll Equipment:")
                    for item in equipment:
                        print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}, Condition: {item[3]}")
                else:
                    print("No equipment found.")

    def add_new_equipment(self):
        name = input("Enter the name of the new equipment: ")
        quantity = input("Enter the quantity of the new equipment: ")
        condition = input("Enter the condition of the new equipment: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Equipment (Name, Quantity, Condition) VALUES (%s, %s, %s);",
                            (name, quantity, condition))
                conn.commit()
                print("Equipment added successfully.")

    def update_equipment_details(self):
        equipment_id = input("Enter the ID of the equipment to update: ")
        new_name = input("Enter the new name for the equipment: ")
        new_quantity = input("Enter the new quantity for the equipment: ")
        new_condition = input("Enter the new condition for the equipment: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Equipment SET Name = %s, Quantity = %s, Condition = %s WHERE ID = %s;",
                            (new_name, new_quantity, new_condition, equipment_id))
                conn.commit()
                print("Equipment details updated successfully.")

    def delete_equipment(self):
        equipment_id = input("Enter the ID of the equipment to delete: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Equipment WHERE ID = %s;", (equipment_id,))
                conn.commit()
                print("Equipment deleted successfully.")

    def update_class_schedule(self):
        print("\nClass Schedule Management")
        print("1. View All Classes")
        print("2. Add New Class")
        print("3. Update Class Details")
        print("4. Delete Class")
        choice = input("Enter your choice: ")

        if choice == "1":
            self.view_all_classes()
        elif choice == "2":
            self.add_new_class()
        elif choice == "3":
            self.update_class_details()
        elif choice == "4":
            self.delete_class()
        else:
            print("Invalid choice. Please try again.")

    def view_all_classes(self):
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM Classes;")
                classes = cur.fetchall()
                if classes:
                    print("\nAll Classes:")
                    for cls in classes:
                        print(f"ID: {cls[0]}, Name: {cls[1]}, Instructor: {cls[2]}, Schedule: {cls[3]}")
                else:
                    print("No classes found.")

    def add_new_class(self):
        name = input("Enter the name of the new class: ")
        instructor = input("Enter the instructor of the new class: ")
        schedule = input("Enter the schedule of the new class: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Classes (Name, Instructor, Schedule) VALUES (%s, %s, %s);", (name, instructor, schedule))
                conn.commit()
                print("Class added successfully.")

    def update_class_details(self):
        class_id = input("Enter the ID of the class to update: ")
        new_name = input("Enter the new name for the class: ")
        new_instructor = input("Enter the new instructor for the class: ")
        new_schedule = input("Enter the new schedule for the class: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Classes SET Name = %s, Instructor = %s, Schedule = %s WHERE ID = %s;",
                            (new_name, new_instructor, new_schedule, class_id))
                conn.commit()
                print("Class details updated successfully.")

    def delete_class(self):
        class_id = input("Enter the ID of the class to delete: ")
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Classes WHERE ID = %s;", (class_id,))
                conn.commit()
                print("Class deleted successfully.")

    def process_billing_and_payment(self):
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT M.Name, CASE WHEN S.SessionID IS NULL THEN 'Not Paid' ELSE 'Paid' END AS Payment_Status
                        FROM Members M
                        LEFT JOIN Sessions S ON M.MemberID = S.MemberID;
                    """)
                    billing_info = cur.fetchall()
                    if billing_info:
                        print("\nBilling and Payment Status:")
                        for member in billing_info:
                            print(f"Member Name: {member[0]}, Payment Status: {member[1]}")
                    else:
                        print("No billing information available.")
        except psycopg2.Error as e:
            print(f"An error occurred while processing billing and payment: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
