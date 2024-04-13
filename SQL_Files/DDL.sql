-- Members Table
CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    membership_type VARCHAR(50) NOT NULL,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    body_fat DECIMAL(5,2),
    cardio_fitness_level VARCHAR(50)
);

-- Trainers Table
CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    specialization VARCHAR(255),
    availability_start TIME,
    availability_end TIME
);

-- Administrative Staff Table
CREATE TABLE administrative_staff (
    admin_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(255),
    role VARCHAR(50)
);

-- Fitness Goals Table
CREATE TABLE fitness_goals (
    goal_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    goal_type VARCHAR(255) NOT NULL,
    target_value DECIMAL(10,2),
    target_date DATE,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Exercise Routines Table
CREATE TABLE exercise_routines (
    routine_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    routine_details TEXT,
    routine_date DATE,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Fitness Achievements Table
CREATE TABLE fitness_achievements (
    achievement_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    achievement_details TEXT,
    achievement_date DATE,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Rooms Table
CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    capacity INT
);

-- Adjusted Classes Table
CREATE TABLE classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    required_equipment TEXT,
    availability_start TIME,
    availability_end TIME,
    room_id INT,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- Bookings Table
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    trainer_id INT,
    class_id INT,
    booking_type VARCHAR(50),
    booking_start_time TIMESTAMP NOT NULL,
    booking_end_time TIMESTAMP,
    room_id INT, -- 
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id),
    FOREIGN KEY (class_id) REFERENCES classes(class_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- Equipment Table
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255) NOT NULL,
    last_maintenance_date DATE
);

-- Notifications Table
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    message TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Bills Table
CREATE TABLE bills (
    bill_id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    description TEXT,
    amount DECIMAL(10, 2),
    bill_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);
