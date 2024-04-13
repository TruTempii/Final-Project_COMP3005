#importing modules
import psycopg2
from datetime import datetime, timedelta

#general password for registering accounts with trainers and admins
GENERAL_PASSWORD = "password123"

#function for connecting to database
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='Project',
            user='postgres',
            password='000111',
            host='localhost'
        )
        cur = conn.cursor()
        print("Connected to the database successfully")
        return conn, cur
    except Exception as e:
        print("Unable to connect to the database")
        print(e)

#function for logging in
def user_login(conn, cur):
    email = input("Enter your email: ")
    #checking each table for the email
    cur.execute("SELECT member_id FROM members WHERE email = %s;", (email,))
    member = cur.fetchone()
    if member:
        return ('member', member[0])

    cur.execute("SELECT trainer_id FROM trainers WHERE email = %s;", (email,))
    trainer = cur.fetchone()
    if trainer:
        return ('trainer', trainer[0])

    cur.execute("SELECT admin_id FROM administrative_staff WHERE email = %s;", (email,))
    admin = cur.fetchone()
    if admin:
        return ('admin', admin[0])

    print("User not found.")
    return (None, None)

#function for ensuring valid input for dates
def get_date_input(prompt, allow_empty=False):
    #get a date input from the user and validate it
    while True:
        user_input = input(prompt).strip()
        if not user_input and allow_empty:
            #allowing empty input if specified
            return None  
        try:
            #trying to convert the user input into a date
            return datetime.strptime(user_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

#similar to function above but for specific times
def get_time_input_for_booking(prompt):
    #ensure valid time format input for bookings
    while True:
        time_input = input(prompt)
        try:
            return datetime.strptime(time_input, "%H:%M").time()
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM format.")

#again, similar to above two functions but instead for strings and integers
def get_input(prompt, expected_type=str, allow_empty=False):
    #get user input and validate it based on the expected type
    while True:
        user_input = input(prompt).strip()
        if not user_input and allow_empty:
            #allowing empty input for certain fields
            return None  
        elif not user_input:
            print("Input cannot be empty. Please try again.")
            continue

        if expected_type != str:
            try:
                return expected_type(user_input)
            except ValueError:
                print(f"Invalid input type. Expected a {expected_type.__name__}. Please try again.")
        else:
            return user_input

#function for users to get valid role
def get_valid_role():
    #ensure user inputs a valid role
    valid_roles = ['member', 'trainer', 'admin']
    while True:
        role = input("Are you registering as a member, trainer, or admin? (member/trainer/admin): ").lower()
        if role in valid_roles:
            return role
        print("Invalid role. Please enter 'member', 'trainer', or 'admin'.")

#function to register user
def register_user(conn, cur):
    role = get_valid_role()

    #checking and prompt for the general password for trainer or admin roles first
    if role in ['trainer', 'admin']:
        entered_password = get_input("Enter the general password to proceed: ")
        if entered_password != GENERAL_PASSWORD:
            print("Incorrect general password. You are not authorized to register as a trainer or admin.")
            #early return if the password does not match
            return  

    #proceeding to collect other registration details
    first_name = get_input("Enter your first name: ")
    last_name = get_input("Enter your last name: ")
    email = get_input("Enter your email: ")

    if role == 'member':
        membership_type = get_input("Enter membership type (Basic/Premium/VIP): ")
        weight = get_input("Enter your weight in kilograms: ", float)
        height = get_input("Enter your height in meters: ", float)
        body_fat = get_input("Enter your body fat percentage: ", float)
        cardio_fitness_level = get_input("Enter your cardio fitness level (High/Medium/Low): ")
        query = """INSERT INTO members (first_name, last_name, email, membership_type, weight, height, body_fat, cardio_fitness_level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(query, (first_name, last_name, email, membership_type, weight, height, body_fat, cardio_fitness_level))
    elif role == 'trainer':
        specialization = get_input("Enter your specialization: ")
        availability = get_input("Enter your availability: ")
        query = """INSERT INTO trainers (first_name, last_name, email, specialization, availability) VALUES (%s, %s, %s, %s, %s);"""
        cur.execute(query, (first_name, last_name, email, specialization, availability))
    elif role == 'admin':
        department = get_input("Enter your department: ")
        admin_role = get_input("Enter your role (Manager/Supervisor/Coordinator/Assistant/Technician): ")
        query = """INSERT INTO administrative_staff (first_name, last_name, email, department, role) VALUES (%s, %s, %s, %s, %s);"""
        cur.execute(query, (first_name, last_name, email, department, admin_role))

    conn.commit()
    print(f"Registration successful as {role}!")

#function to update profiles for users
def update_profile(conn, cur, user_role, user_id):
    #defining input prompts for all user roles, including additional fields for members
    if user_role == 'member':
        input_prompts = {
            'first_name': "Enter new first name (or press Enter to keep current): ",
            'last_name': "Enter new last name (or press Enter to keep current): ",
            'email': "Enter new email (or press Enter to keep current): ",
            'membership_type': "Enter new membership type (or press Enter to keep current): ",
            'weight': "Enter new weight in pounds (or press Enter to keep current): ",
            'height': "Enter new height in meters (or press Enter to keep current): ",
            'body_fat': "Enter new body fat percentage (or press Enter to keep current): ",
            'cardio_fitness_level': "Enter new cardio fitness level (High/Medium/Low) (or press Enter to keep current): "
        }
    else:
        input_prompts = {
            'first_name': "Enter new first name (or press Enter to keep current): ",
            'last_name': "Enter new last name (or press Enter to keep current): ",
            'email': "Enter new email (or press Enter to keep current): "
        }

    update_fields = []
    update_values = []

    #collecting new values from user, skipping empty inputs
    for field, prompt in input_prompts.items():
        if field in ['weight', 'height', 'body_fat'] and user_role == 'member':
            user_input = get_input(prompt, expected_type=float, allow_empty=True)
        else:
            user_input = input(prompt).strip()

        if user_input:
            update_fields.append(f"{field} = %s")
            if field in ['weight', 'body_fat']:
                #converting numeric inputs to float
                update_values.append(float(user_input))  
            else:
                update_values.append(user_input)

    if not update_fields:
        print("No updates provided.")
        return

    #constructing the SQL update statement using the correct column name for the user role
    id_column_name = f"{user_role}_id"
    sql_statement = f"UPDATE {user_role}s SET {', '.join(update_fields)} WHERE {id_column_name} = %s;"
    update_values.append(user_id)

    try:
        cur.execute(sql_statement, update_values)
        conn.commit()
        print("Profile updated successfully." if cur.rowcount else "No profile was updated. Please check your input.")
    except Exception as e:
        print(f"Failed to update profile: {e}")
        conn.rollback()

#function to display the dashboard for members
def display_member_dashboard(conn, cur, member_id):
    print("\n--- Member Dashboard ---")
    
    #fetching and displaying basic member info
    cur.execute("""
        SELECT first_name, last_name, email, membership_type, weight, height, body_fat, cardio_fitness_level
        FROM members WHERE member_id = %s;
    """, (member_id,))
    member_info = cur.fetchone()
    if member_info:
        print(f"Name: {member_info[0]} {member_info[1]}\nEmail: {member_info[2]}\nMembership Type: {member_info[3]}")
        print(f"Weight: {member_info[4]} kg\nHeight: {member_info[5]} m\nBody Fat: {member_info[6]}%\nCardio Fitness Level: {member_info[7]}")
        
        #calculating and displaying BMI
        bmi = member_info[4] / (member_info[5] ** 2)
        print("\n--- Health Statistics ---")
        print(f"Body Mass Index (BMI): {bmi:.2f}")
    else:
        print("Member not found.")
        return
    
    #displaying fitness goals within the dashboard
    print("\n--- Fitness Goals ---")
    cur.execute("SELECT goal_type, target_value, target_date FROM fitness_goals WHERE member_id = %s ORDER BY target_date;", (member_id,))
    goals = cur.fetchall()
    if goals:
        for goal in goals:
            print(f"Goal Type: {goal[0]}, Target: {goal[1]}, Target Date: {goal[2]}")
    else:
        print("No fitness goals set yet.")

    #displaying exercise routines
    print("\n--- Exercise Routines ---")
    cur.execute("SELECT routine_details, routine_date FROM exercise_routines WHERE member_id = %s ORDER BY routine_date;", (member_id,))
    routines = cur.fetchall()
    if routines:
        for routine in routines:
            print(f"Details: {routine[0]}, Date: {routine[1]}")
    else:
        print("No exercise routines set yet.")
    
    #displaying fitness achievements
    print("\n--- Fitness Achievements ---")
    cur.execute("SELECT achievement_details, achievement_date FROM fitness_achievements WHERE member_id = %s ORDER BY achievement_date;", (member_id,))
    achievements = cur.fetchall()
    if achievements:
        for achievement in achievements:
            print(f"Details: {achievement[0]}, Date: {achievement[1]}")
    else:
        print("No fitness achievements logged yet.")
    
    print()  

    #displaying all types of bookings for the member
    print("--- Bookings ---")
    cur.execute("""
        SELECT 
            CASE 
                WHEN class_id IS NOT NULL THEN 'Class'
                WHEN trainer_id IS NOT NULL THEN 'Personal Training'
            END AS booking_type,
            CASE 
                WHEN class_id IS NOT NULL THEN (SELECT class_name FROM classes WHERE class_id = bookings.class_id)
                WHEN trainer_id IS NOT NULL THEN (SELECT first_name || ' ' || last_name FROM trainers WHERE trainer_id = bookings.trainer_id)
            END AS booking_name,
            booking_start_time,
            booking_end_time
        FROM bookings
        WHERE member_id = %s
        ORDER BY booking_start_time;
    """, (member_id,))
    bookings = cur.fetchall()
    if bookings:
        for booking in bookings:
            print(f"{booking[0]}: {booking[1]} from {booking[2]} to {booking[3]}")
    else:
        print("No bookings found.")

    #displaying notifications for the member, emphasizing unread notifications
    print("\n--- Notifications ---")
    cur.execute("""
        SELECT message, created_at, read, notification_id 
        FROM notifications 
        WHERE member_id = %s 
        ORDER BY created_at DESC;
    """, (member_id,))
    notifications = cur.fetchall()
    if notifications:
        for notification in notifications:
            read_status = 'Read' if notification[2] else 'Unread'
            #highlighting unread notifications
            #if notification is unread
            if not notification[2]:  
                print(f"🔔 [Unread] Date: {notification[1].strftime('%Y-%m-%d %H:%M')}, Message: {notification[0]}")
                #optionally mark as read
                cur.execute("""
                    UPDATE notifications 
                    SET read = TRUE 
                    WHERE notification_id = %s;
                """, (notification[3],))
            else:
                print(f"Date: {notification[1].strftime('%Y-%m-%d %H:%M')}, Status: {read_status}, Message: {notification[0]}")
        conn.commit()
    else:
        print("No new notifications.")

    print()

#function to add fitness goals for members
def add_fitness_goal(conn, cur, member_id):
    print("\n--- Add Fitness Goal ---")
    goal_type = get_input("Enter goal type (e.g., 'Lose Weight', 'Increase Running Distance'): ")
    target_value = get_input("Enter target value (e.g., weight in lbs, distance in miles): ", float)
    target_date = get_date_input("Enter target date (YYYY-MM-DD): ")
    
    query = """
    INSERT INTO fitness_goals (member_id, goal_type, target_value, target_date) 
    VALUES (%s, %s, %s, %s);
    """
    cur.execute(query, (member_id, goal_type, target_value, target_date))
    conn.commit()
    print("Fitness goal added successfully.")

#function to add exercise routines for members
def add_exercise_routine(conn, cur, member_id):
    print("\n--- Add Exercise Routine ---")
    routine_details = get_input("Enter the details of your exercise routine: ")
    routine_date = get_date_input("Enter the date you plan to start or have started this routine (YYYY-MM-DD): ")
    
    query = """
    INSERT INTO exercise_routines (member_id, routine_details, routine_date) 
    VALUES (%s, %s, %s);
    """
    cur.execute(query, (member_id, routine_details, routine_date))
    conn.commit()
    print("Exercise routine added successfully.")

#function to log fitness achievements for members
def log_fitness_achievement(conn, cur, member_id):
    print("\n--- Log Fitness Achievement ---")
    achievement_details = get_input("Enter details of your achievement: ")
    achievement_date = get_date_input("Enter the date of your achievement (YYYY-MM-DD): ")
    
    query = """
    INSERT INTO fitness_achievements (member_id, achievement_details, achievement_date) 
    VALUES (%s, %s, %s);
    """
    cur.execute(query, (member_id, achievement_details, achievement_date))
    conn.commit()
    print("Fitness achievement logged successfully.")

#function for trainers to view their schedules
def view_trainer_schedule(conn, cur, trainer_id):
    print("\n--- Trainer Schedule ---")
    cur.execute("""
        SELECT b.booking_start_time, b.booking_end_time, m.first_name, m.last_name, c.class_name 
        FROM bookings b
        LEFT JOIN members m ON b.member_id = m.member_id
        LEFT JOIN classes c ON b.class_id = c.class_id
        WHERE b.trainer_id = %s
        ORDER BY b.booking_start_time;
    """, (trainer_id,))
    schedule = cur.fetchall()
    if schedule:
        for session in schedule:
            start_time, end_time, first_name, last_name, class_name = session
            session_info = f"Class: {class_name}" if class_name else f"Personal Training with {first_name} {last_name}"
            print(f"{session_info} from {start_time} to {end_time}")
    else:
        print("No scheduled sessions.")

#function for trainers to update their availabilities
def update_trainer_availability(conn, cur, trainer_id):
    print("\n--- Update Availability ---")

    #function to safely convert time input
    def get_time_input(prompt):
        while True:
            time_input = input(prompt)
            try:
                return datetime.strptime(time_input, "%H:%M").time()
            except ValueError:
                print("Invalid time format. Please enter the time in HH:MM format.")

    new_start_time = get_time_input("Enter your new availability start time (HH:MM): ")
    new_end_time = get_time_input("Enter your new availability end time (HH:MM): ")

    #identifying conflicting bookings
    cur.execute("""
        SELECT booking_id, booking_start_time, booking_end_time, member_id, trainer_id
        FROM bookings
        WHERE trainer_id = %s AND NOT (
            booking_start_time::time >= %s OR 
            booking_end_time::time <= %s
        );
    """, (trainer_id, new_end_time, new_start_time))
    conflicts = cur.fetchall()

    if conflicts:
        print("Conflicting bookings found. These bookings will be cancelled if you proceed:")
        for conflict in conflicts:
            booking_id, start_time, end_time, member_id, trainer_id = conflict

            #fetching trainer's full name for each conflict
            cur.execute("SELECT first_name, last_name FROM trainers WHERE trainer_id = %s;", (trainer_id,))
            trainer_name = cur.fetchone()
            full_name = " ".join(trainer_name) if trainer_name else "Unknown Trainer"

            print(f"Booking with {full_name}: ID {booking_id}, Start: {start_time}, End: {end_time}")

        proceed = input("Do you want to proceed and cancel these booking(s)? (yes/no): ")
        if proceed.lower() == 'yes':
            for conflict in conflicts:
                booking_id, _, _, member_id, _ = conflict
                #cancelling the booking
                cur.execute("DELETE FROM bookings WHERE booking_id = %s;", (booking_id,))
                #also deleting the bill
                cur.execute("DELETE FROM bills WHERE member_id = %s AND description LIKE %s;", (member_id, '%session fee%'))
                #notifying the affected member with the trainer's full name in the message
                notification_msg = f"Your booking with {full_name} (ID: {booking_id}) has been cancelled due to trainer availability changes."
                cur.execute("INSERT INTO notifications (member_id, message) VALUES (%s, %s);", (member_id, notification_msg))
            conn.commit()
            print("Conflicting bookings have been cancelled.")
        else:
            print("Your availability remains unchanged. No bookings have been cancelled.")
            return
    else:
        print("No conflicting bookings found.")

    #updating trainer availability
    cur.execute("UPDATE trainers SET availability_start = %s, availability_end = %s WHERE trainer_id = %s;", (new_start_time, new_end_time, trainer_id))
    conn.commit()
    print("Trainer availability updated successfully.")

#functin for trainers to view members in the system
def view_member_profile(conn, cur):
    print("\n--- Member Profiles ---")  
    first_name = input("Enter the member's first name (or part of it): ")
    last_name = input("Enter the member's last name (or part of it): ")

    query = """
    SELECT first_name, last_name, email, weight, height, body_fat, cardio_fitness_level
    FROM members
    WHERE first_name ILIKE %s AND last_name ILIKE %s;
    """
    cur.execute(query, (f'%{first_name}%', f'%{last_name}%'))
    profiles = cur.fetchall()

    if profiles:
        print("\n--- Members ---")  
        for profile in profiles:
            print(f"\nName: {profile[0]} {profile[1]}\nEmail: {profile[2]}\nWeight: {profile[3]}\nHeight: {profile[4]}\nBody Fat: {profile[5]}\nCardio Level: {profile[6]}")
    else:
        print("No member profiles found with the given name.")

#function to view all available rooms for bookings
def get_available_rooms(cur, start_datetime, end_datetime):
    #fetching available rooms that don't have bookings overlapping the provided times
    query = """
    SELECT room_id, room_name, capacity FROM rooms
    WHERE room_id NOT IN (
        SELECT DISTINCT room_id FROM bookings
        WHERE NOT (
            booking_end_time <= %s OR
            booking_start_time >= %s
        )
    );
    """
    cur.execute(query, (start_datetime, end_datetime))
    return cur.fetchall()

#function to check room capacities
def check_room_capacity(cur, room_id, booking_date, start_time, end_time):
    #checking if adding a booking would exceed the room's capacity
    start_datetime = datetime.combine(booking_date, start_time)
    end_datetime = datetime.combine(booking_date, end_time)
    
    query = """
    SELECT count(*) FROM bookings
    WHERE room_id = %s AND NOT (
        booking_end_time <= %s OR
        booking_start_time >= %s
    );
    """
    cur.execute(query, (room_id, start_datetime, end_datetime))
    current_bookings = cur.fetchone()[0]

    cur.execute("SELECT capacity FROM rooms WHERE room_id = %s;", (room_id,))
    room_capacity = cur.fetchone()[0]

    return current_bookings < room_capacity

#function to check if a given time falls within a range
def is_time_between(begin_time, end_time, check_time):
    return begin_time <= check_time <= end_time

#function to check if booking times are valid for a class
def validate_class_booking(cur, class_id, start_time, end_time):
    cur.execute("SELECT availability_start, availability_end FROM classes WHERE class_id = %s;", (class_id,))
    availability = cur.fetchone()
    if availability:
        class_start = availability[0]
        class_end = availability[1]
        return is_time_between(class_start, class_end, start_time) and is_time_between(class_start, class_end, end_time)
    return False

#function to check if booking times are valid for a trainer
def validate_trainer_availability(cur, trainer_id, start_time, end_time):
    cur.execute("SELECT availability_start, availability_end FROM trainers WHERE trainer_id = %s;", (trainer_id,))
    availability = cur.fetchone()
    if availability:
        trainer_start = availability[0]
        trainer_end = availability[1]
        return is_time_between(trainer_start, trainer_end, start_time) and is_time_between(trainer_start, trainer_end, end_time)
    return False

#function to book a class
def book_class(conn, cur, member_id):
    print("\n--- Book a Class ---")
    #fetching and displaying classes with their times and location (room name)
    cur.execute("""
        SELECT c.class_id, c.class_name, c.availability_start, c.availability_end, r.room_name
        FROM classes c
        JOIN rooms r ON c.room_id = r.room_id;
    """)
    classes = cur.fetchall()
    if not classes:
        print("No classes available.")
        return
    
    for cls in classes:
        print(f"ID: {cls[0]}, Name: {cls[1]}, Available: {cls[2]} to {cls[3]}, Location: {cls[4]}")
    
    class_id = get_input("Enter the ID of the class you want to book: ", int)
    
    #checking if the class ID exists
    cur.execute("SELECT EXISTS(SELECT 1 FROM classes WHERE class_id = %s);", (class_id,))
    if not cur.fetchone()[0]:
        print("Invalid class ID. Please select a valid class.")
        return
    
    booking_date = get_date_input("Enter the date for the class (YYYY-MM-DD): ")
    start_time = get_time_input_for_booking("Enter the start time for the class (HH:MM): ")
    end_time = get_time_input_for_booking("Enter the end time for the class (HH:MM): ")

    if not validate_class_booking(cur, class_id, start_time, end_time):
        print("Invalid booking time for this class.")
        return
    
    start_datetime = datetime.combine(booking_date, start_time)
    end_datetime = datetime.combine(booking_date, end_time)

    #inserting booking into the database
    cur.execute("""
        INSERT INTO bookings (member_id, class_id, booking_type, booking_start_time, booking_end_time, room_id)
        SELECT %s, %s, 'Class', %s, %s, room_id
        FROM classes WHERE class_id = %s;
    """, (member_id, class_id, start_datetime, end_datetime, class_id))
    conn.commit()
    #generate a bill
    generate_bill(conn, cur, member_id, 'Class')
    print("Class booked successfully.")

#function to book personal training sessions
def book_personal_training(conn, cur, member_id):
    print("\n--- Available Personal Trainers ---")
    cur.execute("SELECT trainer_id, first_name || ' ' || last_name AS name, availability_start, availability_end FROM trainers;")
    trainers = cur.fetchall()
    if not trainers:
        print("No trainers available.")
        return

    for trainer in trainers:
        print(f"ID: {trainer[0]}, Name: {trainer[1]}, Available: {trainer[2]} to {trainer[3]}")

    trainer_id = get_input("Enter the ID of the trainer you want to book: ", int)
    
    #checking if the trainer ID exists
    cur.execute("SELECT EXISTS(SELECT 1 FROM trainers WHERE trainer_id = %s);", (trainer_id,))
    if not cur.fetchone()[0]:
        print("Invalid trainer ID. Please select a valid trainer.")
        return
    
    booking_date = get_date_input("Enter booking date (YYYY-MM-DD): ")
    start_time = get_time_input_for_booking("Enter start time (HH:MM): ")
    end_time = get_time_input_for_booking("Enter end time (HH:MM): ")

    if not validate_trainer_availability(cur, trainer_id, start_time, end_time):
        print("Selected trainer is not available during this time.")
        return

    start_datetime = datetime.combine(booking_date, start_time)
    end_datetime = datetime.combine(booking_date, end_time)

    #fetching available rooms
    print("\n--- Available Rooms for Personal Training ---")
    available_rooms = get_available_rooms(cur, start_datetime, end_datetime)
    if not available_rooms:
        print("No rooms available for the selected time.")
        return

    for room in available_rooms:
        print(f"{room[0]}: {room[1]} (Capacity: {room[2]})")

    room_id = get_input("Select a room by ID, or press Enter to skip: ", int, allow_empty=True)
    
    if room_id:
        if not check_room_capacity(cur, room_id, booking_date, start_time, end_time):
            print("Selected room cannot accommodate more bookings at this time.")
            return

    #inserting booking into the database, including room_id if selected
    cur.execute("""
        INSERT INTO bookings (member_id, trainer_id, booking_type, booking_start_time, booking_end_time, room_id)
        VALUES (%s, %s, 'Personal Training', %s, %s, %s);
    """, (member_id, trainer_id, start_datetime, end_datetime, room_id if room_id else None))
    conn.commit()
    #generate a bill
    generate_bill(conn, cur, member_id, 'Personal Training')
    print("Personal training session booked successfully.")

#function to reschedule a booking
def reschedule_booking(conn, cur, member_id):
    print("\n--- Your Bookings for Rescheduling ---")
    cur.execute("""
        SELECT booking_id, 
            CASE 
                WHEN class_id IS NOT NULL THEN 'Class'
                WHEN trainer_id IS NOT NULL THEN 'Personal Training'
            END AS booking_type,
            CASE 
                WHEN class_id IS NOT NULL THEN (SELECT class_name FROM classes WHERE class_id = bookings.class_id)
                WHEN trainer_id IS NOT NULL THEN (SELECT first_name || ' ' || last_name FROM trainers WHERE trainer_id = bookings.trainer_id)
            END AS booking_name,
            booking_start_time,
            booking_end_time
        FROM bookings
        WHERE member_id = %s
        ORDER BY booking_start_time;
    """, (member_id,))
    bookings = cur.fetchall()
    if not bookings:
        print("You have no bookings to reschedule.")
        return
    
    for booking in bookings:
        print(f"Booking ID: {booking[0]}, Type: {booking[1]}, Name: {booking[2]}, From: {booking[3]} To: {booking[4]}")

    booking_id = get_input("Enter the booking ID you want to reschedule: ", int)
    if not booking_id:
        print("Invalid input. Please enter a valid booking ID.")
        return

    new_date = get_date_input("Enter the new date for this booking (YYYY-MM-DD): ")
    new_start_time = get_time_input_for_booking("Enter the new start time (HH:MM): ")
    new_end_time = get_time_input_for_booking("Enter the new end time (HH:MM): ")

    #using datetime.combine to merge date and time inputs into datetime objects
    new_start_datetime = datetime.combine(new_date, new_start_time)
    new_end_datetime = datetime.combine(new_date, new_end_time)

    #checking for conflicts
    cur.execute("""
        SELECT booking_id
        FROM bookings
        WHERE member_id = %s
        AND (
            (%s, %s) OVERLAPS (booking_start_time, booking_end_time)
            OR %s BETWEEN booking_start_time AND booking_end_time
            OR %s BETWEEN booking_start_time AND booking_end_time
        );
    """, (member_id, new_start_datetime, new_end_datetime, new_start_datetime, new_end_datetime))
    conflicting_bookings = cur.fetchall()

    if conflicting_bookings:
        print("This rescheduled booking conflicts with existing bookings.")
        return

    #proceeding to update the booking with new times
    cur.execute("""
        UPDATE bookings 
        SET booking_start_time = %s, booking_end_time = %s
        WHERE booking_id = %s AND member_id = %s;
    """, (new_start_datetime, new_end_datetime, booking_id, member_id))
    conn.commit()
    print("Booking rescheduled successfully.")

#function to cancel bookings
def cancel_booking(conn, cur, member_id):
    print("\n--- Your Bookings ---")
    cur.execute("""
        SELECT booking_id, 
            CASE 
                WHEN class_id IS NOT NULL THEN 'Class'
                WHEN trainer_id IS NOT NULL THEN 'Personal Training'
            END AS booking_type,
            CASE 
                WHEN class_id IS NOT NULL THEN (SELECT class_name FROM classes WHERE class_id = bookings.class_id)
                WHEN trainer_id IS NOT NULL THEN (SELECT first_name || ' ' || last_name FROM trainers WHERE trainer_id = bookings.trainer_id)
            END AS booking_name,
            booking_start_time,
            booking_end_time
        FROM bookings
        WHERE member_id = %s
        ORDER BY booking_start_time;
    """, (member_id,))
    bookings = cur.fetchall()
    if not bookings:
        print("You have no bookings to cancel.")
        return

    for booking in bookings:
        print(f"Booking ID: {booking[0]}, Type: {booking[1]}, Name: {booking[2]}, From: {booking[3]} To: {booking[4]}")

    booking_id = get_input("Enter the booking ID you want to cancel: ", str, allow_empty=False)
    if not booking_id.isdigit():
        print("Invalid input. Please enter a valid booking ID.")
        return

    #converting input to int after validation
    booking_id = int(booking_id)  
    #checking if the booking ID exists and belongs to the member
    cur.execute("SELECT * FROM bookings WHERE booking_id = %s AND member_id = %s;", (booking_id, member_id))
    booking = cur.fetchone()
    if not booking:
        print("No such booking found or the booking does not belong to you.")
        return

    #deleting the booking
    cur.execute("DELETE FROM bookings WHERE booking_id = %s;", (booking_id,))

    #deleting the bill related to the canceled booking
    if booking[2] == 'Class':
        #for class bookings
        cur.execute("DELETE FROM bills WHERE member_id = %s AND description = 'session fee' AND booking_id = %s;", (member_id, booking_id))
    elif booking[2] == 'Personal Training':
        #for personal training bookings
        cur.execute("DELETE FROM bills WHERE member_id = %s AND description = 'session fee' AND booking_id = %s;", (member_id, booking_id))

    conn.commit()
    print("Booking cancelled successfully.")

#function for admins to manage rooms, given a menu
def manage_rooms(conn, cur):
    while True:
        print("\n--- Room Management ---")
        print("1. Add Room")
        print("2. Modify Room")
        print("3. Delete Room")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_room(conn, cur)
        elif choice == '2':
            list_rooms(conn, cur)  
            modify_room(conn, cur)
        elif choice == '3':
            list_rooms(conn, cur)  
            delete_room(conn, cur)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

#function to list all available rooms for admins to see
def list_rooms(conn, cur):
    print("Fetching all available rooms...")
    try:
        cur.execute("SELECT room_id, room_name, capacity FROM rooms;")
        rooms = cur.fetchall()
        print("\nAvailable Rooms:")
        for room in rooms:
            print(f"ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
    except Exception as e:
        print(f"Failed to fetch rooms: {e}")

#function to add rooms 
def add_room(conn, cur):
    room_name = get_input("Enter room name: ")
    capacity = get_input("Enter room capacity: ", int)
    try:
        cur.execute("INSERT INTO rooms (room_name, capacity) VALUES (%s, %s);", (room_name, capacity))
        conn.commit()
        print("Room added successfully.")
    except Exception as e:
        print(f"Failed to add room: {e}")
        conn.rollback()

#function to modify rooms
def modify_room(conn, cur):
    room_id = get_input("Enter room ID to modify: ", int)
    new_name = get_input("Enter new name for the room (or press Enter to skip): ", allow_empty=True)
    new_capacity = get_input("Enter new capacity for the room (or press Enter to skip): ", int, allow_empty=True)

    updates = []
    params = []
    if new_name:
        updates.append("room_name = %s")
        params.append(new_name)
    if new_capacity:
        updates.append("capacity = %s")
        params.append(new_capacity)

    if not updates:
        print("No changes made.")
        return

    params.append(room_id)
    update_query = "UPDATE rooms SET " + ", ".join(updates) + " WHERE room_id = %s;"
    try:
        cur.execute(update_query, params)
        conn.commit()
        print("Room modified successfully.")
    except Exception as e:
        print(f"Failed to modify room: {e}")
        conn.rollback()

#function to delete rooms
def delete_room(conn, cur):
    room_id = get_input("Enter room ID to delete: ", int)
    try:
        cur.execute("SELECT room_name FROM rooms WHERE room_id = %s;", (room_id,))
        room_info = cur.fetchone()
        if not room_info:
            print("Room not found.")
            return

        room_name = room_info[0]

        #fetching bookings linked to this room
        cur.execute("""
            SELECT booking_id, member_id, booking_start_time, booking_end_time
            FROM bookings
            WHERE room_id = %s;
        """, (room_id,))
        bookings = cur.fetchall()

        for booking_id, member_id, start_time, end_time in bookings:
            #checking for available alternative rooms
            cur.execute("""
                SELECT room_id FROM rooms WHERE room_id != %s AND room_id NOT IN (
                    SELECT room_id FROM bookings WHERE NOT (
                        booking_end_time <= %s OR
                        booking_start_time >= %s
                    )
                );
            """, (room_id, end_time, start_time))
            alternative_room = cur.fetchone()

            if alternative_room:
                #reassigning the booking to the new room
                new_room_id = alternative_room[0]
                cur.execute("UPDATE bookings SET room_id = %s WHERE booking_id = %s;", (new_room_id, booking_id))
                notification_msg = f"Your booking has been moved to another room due to room deletion."
            else:
                #no alternative rooms available, cancel the booking
                cur.execute("DELETE FROM bookings WHERE booking_id = %s;", (booking_id,))
                #deleting the bill as the booking is cancelled
                cur.execute("DELETE FROM bills WHERE member_id = %s AND description LIKE 'session fee' AND booking_id = %s;", (member_id, booking_id))
                notification_msg = f"Your booking has been cancelled as no alternative room is available."

            #notifying the member
            cur.execute("INSERT INTO notifications (member_id, message) VALUES (%s, %s);", (member_id, notification_msg))

        #now deletinging the room
        cur.execute("DELETE FROM rooms WHERE room_id = %s;", (room_id,))
        conn.commit()
        print(f"Room '{room_name}' and all associated bookings have been successfully deleted.")
    except Exception as e:
        print(f"Failed to delete room: {e}")
        conn.rollback()

#function to monitor the equipments
def monitor_equipment_maintenance(conn, cur):
    while True:
        print("\n--- Equipment Maintenance Monitoring ---")
        print("Fetching all equipments and their last maintenance dates...")
        
        #fetching all equipments and their maintenance dates from the database
        cur.execute("SELECT equipment_id, equipment_name, last_maintenance_date FROM equipment;")
        equipments = cur.fetchall()
        
        if not equipments:
            print("No equipment found.")
            return

        print("\nList of Equipment:")
        for equipment in equipments:
            equipment_id, name, last_maintenance_date = equipment
            print(f"ID: {equipment_id}, Name: {name}, Last Maintenance: {last_maintenance_date}")

        print("\nOptions:")
        print("1. Update an equipment's maintenance date")
        print("2. Back to Main Menu")

        choice = input("Enter your choice (1-2): ")
        if choice == '1':
            equipment_id = get_input("Enter the ID of the equipment to update: ", int)
            new_date = get_date_input("Enter the new maintenance date (YYYY-MM-DD): ")
            
            #updating the maintenance date in the database
            try:
                cur.execute("UPDATE equipment SET last_maintenance_date = %s WHERE equipment_id = %s;", (new_date, equipment_id))
                conn.commit()
                print("Maintenance date updated successfully.")
            except Exception as e:
                print(f"Failed to update maintenance date: {e}")
                conn.rollback()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

#function to ensure valid time input
def get_time_input(prompt, allow_empty=False):
    #safely convert time input and handle cases where input can be skipped
    while True:
        time_input = input(prompt).strip()
        if not time_input and allow_empty:
            #allowing skipping by returning none if empty input is allowed
            return None  
        elif not time_input:
            print("No input provided. Please enter a time or press Enter to skip if allowed.")
            continue
        try:
            return datetime.strptime(time_input, "%H:%M").time()
        except ValueError:
            print("Invalid time format. Please enter the time in HH:MM format.")

#function to add a class
def add_class(conn, cur):
    print("\n--- Add New Class ---")
    class_name = get_input("Enter class name: ")
    required_equipment = get_input("Enter required equipment: ")
    availability_start = get_time_input("Enter start time (HH:MM): ")
    availability_end = get_time_input("Enter end time (HH:MM): ")

    #displaying available rooms
    list_rooms(conn, cur)
    room_id = get_input("Choose a room by ID: ", int)

    query = """
    INSERT INTO classes (class_name, required_equipment, availability_start, availability_end, room_id)
    VALUES (%s, %s, %s, %s, %s);
    """
    try:
        cur.execute(query, (class_name, required_equipment, availability_start, availability_end, room_id))
        conn.commit()
        print("Class added successfully.")
    except Exception as e:
        print(f"Failed to add class: {e}")
        conn.rollback()

#function to list all available classes for admins to see
def list_classes(cur):
    #listing all available classes for selection
    print("\nFetching all available classes...")
    cur.execute("SELECT class_id, class_name FROM classes ORDER BY class_name;")
    classes = cur.fetchall()
    if classes:
        print("\nAvailable Classes:")
        for cls in classes:
            print(f"ID: {cls[0]}, Name: {cls[1]}")
    else:
        print("No classes available.")
    return classes

#function to modify classes
def modify_class(conn, cur):
    classes = list_classes(cur)
    if not classes:
        return

    class_id = get_input("Enter the class ID to modify: ", int)
    cur.execute("SELECT EXISTS(SELECT 1 FROM classes WHERE class_id = %s);", (class_id,))
    if not cur.fetchone()[0]:
        print("Invalid class ID. Please select a valid class.")
        return

    new_name = get_input("Enter new class name (or press Enter to skip): ", allow_empty=True)
    new_equipment = get_input("Enter new required equipment (or press Enter to skip): ", allow_empty=True)
    new_start = get_time_input("Enter new start time (HH:MM) (or press Enter to skip): ", allow_empty=True)
    new_end = get_time_input("Enter new end time (HH:MM) (or press Enter to skip): ", allow_empty=True)

    list_rooms(conn, cur)
    new_room_id = get_input("Enter new room ID (or press Enter to skip): ", int, allow_empty=True)

    updates = []
    params = []

    if new_name:
        updates.append("class_name = %s")
        params.append(new_name)
    if new_equipment:
        updates.append("required_equipment = %s")
        params.append(new_equipment)
    if new_start:
        updates.append("availability_start = %s")
        params.append(new_start)
    if new_end:
        updates.append("availability_end = %s")
        params.append(new_end)
    if new_room_id:
        updates.append("room_id = %s")
        params.append(new_room_id)

    if not updates:
        print("No changes made.")
        return

    params.append(class_id)
    update_query = "UPDATE classes SET " + ", ".join(updates) + " WHERE class_id = %s;"
    try:
        cur.execute(update_query, params)
        conn.commit()
        print("Class modified successfully.")
    except Exception as e:
        print(f"Failed to modify class: {e}")
        conn.rollback()

#function to delete classes
def delete_class(conn, cur):
    classes = list_classes(cur)
    if not classes:
        print("No classes available to delete.")
        return

    class_id = get_input("Enter the class ID to delete: ", int)

    #firstly, handle existing bookings for the class
    cur.execute("SELECT booking_id, member_id FROM bookings WHERE class_id = %s;", (class_id,))
    bookings = cur.fetchall()

    if bookings:
        print(f"There are {len(bookings)} bookings associated with this class that will be affected.")
        for booking_id, member_id in bookings:
            #notifying members about the cancellation
            notification_msg = f"Your booking (ID: {booking_id}) has been cancelled due to class deletion."
            cur.execute("INSERT INTO notifications (member_id, message) VALUES (%s, %s);", (member_id, notification_msg))
            #cancelling the booking
            cur.execute("DELETE FROM bookings WHERE booking_id = %s;", (booking_id,))
            #deleting the associated bills
            cur.execute("DELETE FROM bills WHERE member_id = %s AND description LIKE 'session fee' AND booking_id = %s;", (member_id, booking_id))
        print("Affected bookings have been cancelled and members notified.")

    #now, deleting the class
    try:
        cur.execute("DELETE FROM classes WHERE class_id = %s;", (class_id,))
        conn.commit()
        print("Class and all associated bookings and bills have been successfully deleted.")
    except Exception as e:
        print(f"Failed to delete class: {e}")
        conn.rollback()

#function with a menu for managing the classes (used by admins)
def class_management(conn, cur):
    while True:
        print("\n--- Class Management ---")
        print("1. Add Class")
        print("2. Modify Class")
        print("3. Delete Class")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_class(conn, cur)
        elif choice == '2':
            modify_class(conn, cur)
        elif choice == '3':
            delete_class(conn, cur)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

def generate_bill(conn, cur, member_id, booking_type):
    #$65 for classes, $100 for personal training
    fee = 65 if booking_type == 'Class' else 100  
    description = f"{booking_type} session fee"
    #due date 30 days from now
    due_date = datetime.now() + timedelta(days=30)  
    query = """
    INSERT INTO bills (member_id, description, amount, due_date, status)
    VALUES (%s, %s, %s, %s, 'Pending');
    """
    cur.execute(query, (member_id, description, fee, due_date))
    conn.commit()

#function to view all of the bills 
def view_all_bills(conn, cur):
    print("\n--- View All Bills ---")
    cur.execute("SELECT b.bill_id, m.first_name, m.last_name, b.amount, b.due_date, b.status FROM bills b JOIN members m ON b.member_id = m.member_id;")
    bills = cur.fetchall()
    if bills:
        for bill in bills:
            print(f"Bill ID: {bill[0]}, Member: {bill[1]} {bill[2]}, Amount: ${bill[3]}, Due Date: {bill[4]}, Status: {bill[5]}")
    else:
        print("No bills to display.")

#function to pay the bills
def view_and_pay_bills(conn, cur, member_id):
    print("\n--- Your Bills ---")
    cur.execute("""
        SELECT bill_id, description, amount, due_date, status
        FROM bills
        WHERE member_id = %s AND status = 'Pending';
    """, (member_id,))
    bills = cur.fetchall()
    if not bills:
        print("You have no pending bills.")
        return

    for bill in bills:
        print(f"Bill ID: {bill[0]}, Description: {bill[1]}, Amount: ${bill[2]}, Due Date: {bill[3].strftime('%Y-%m-%d')}, Status: {bill[4]}")

    print("Enter the bill ID to pay or press '2' to go back to the menu.")
    choice = input("Choice: ")

    if choice == '2':
        return  
    else:
        pay_bill(conn, cur, member_id, choice)

def pay_bill(conn, cur, member_id, bill_id):
    if not bill_id.isdigit():
        print("Invalid input. Please enter a numeric bill ID.")
        return

    #converting bill ID to integer after validating it's numeric
    bill_id = int(bill_id)  
    cur.execute("""
        SELECT * FROM bills WHERE bill_id = %s AND member_id = %s AND status = 'Pending';
    """, (bill_id, member_id))
    bill = cur.fetchone()

    if not bill:
        print("Invalid bill ID or the bill has already been paid.")
        return

    cur.execute("UPDATE bills SET status = 'Paid' WHERE bill_id = %s;", (bill_id,))
    conn.commit()
    print(f"Bill ID {bill_id} has been paid successfully.")
        
#main menu function
def main():
    conn, cur = connect_to_db()
    main_menu(conn, cur)
    
#main menu for the system
def main_menu(conn, cur):
    while True:
        print("\nWelcome to the Health and Fitness Club Management System")
        print("0. Register New User")
        print("1. Login")
        print("2. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '0':
            register_user(conn, cur)
        elif choice == '1':
            user_role, user_id = user_login(conn, cur)
            if user_role == 'member':
                member_menu(conn, cur, user_id)
            elif user_role == 'trainer':
                trainer_menu(conn, cur, user_id)
            elif user_role == 'admin':
                admin_menu(conn, cur, user_id)
            else:
                print("Login failed.")
        elif choice == '2':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please enter a number between 0-2.")
    
    #closing cursor
    cur.close() 
    #closing connection 
    conn.close()  

#member menu
def member_menu(conn, cur, member_id):
    while True:
        print("\n--- Member Menu ---")
        print("1. View Dashboard")
        print("2. Update Profile")
        print("3. Book a Class")
        print("4. Book Personal Training")
        print("5. Cancel a Booking")
        print("6. Reschedule a Booking")
        print("7. Add Fitness Goal")
        print("8. Add Exercise Routine")
        print("9. Log Fitness Achievement")
        print("10. View and Pay Bills")
        print("11. Logout")

        choice = get_input("Enter your choice: ")
        if choice == '1':
            display_member_dashboard(conn, cur, member_id)
        elif choice == '2':
            update_profile(conn, cur, 'member', member_id)
        elif choice == '3':
            book_class(conn, cur, member_id)
        elif choice == '4':
            book_personal_training(conn, cur, member_id)
        elif choice == '5':
            cancel_booking(conn, cur, member_id)
        elif choice == '6':
            reschedule_booking(conn, cur, member_id)
        elif choice == '7':
            add_fitness_goal(conn, cur, member_id)
        elif choice == '8':
            add_exercise_routine(conn, cur, member_id)
        elif choice == '9':
            log_fitness_achievement(conn, cur, member_id)
        elif choice == '10':
            view_and_pay_bills(conn, cur, member_id)
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")

#trainer menu
def trainer_menu(conn, cur, trainer_id):
    while True:
        print("\n--- Trainer Menu ---")
        print("1. View Schedule")
        print("2. View Member Profile")
        print("3. Update Availability")
        print("4. Logout")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_trainer_schedule(conn, cur, trainer_id)
        elif choice == '2':
            view_member_profile(conn, cur)
        elif choice == '3':
            update_trainer_availability(conn, cur, trainer_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

#admin menu
def admin_menu(conn, cur, admin_id):
    while True:
        print("\n--- Administrative Menu ---")
        print("1. Manage Room Bookings")
        print("2. Monitor Equipment Maintenance")
        print("3. Update Class Schedules")
        print("4. Oversee Billing and Payments")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            manage_rooms(conn, cur)
        elif choice == '2':
            monitor_equipment_maintenance(conn, cur)
        elif choice == '3':
            class_management(conn, cur)
        elif choice == '4':
            view_all_bills(conn, cur)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
