-- Members
INSERT INTO members (first_name, last_name, email, membership_type, weight, height, body_fat, cardio_fitness_level) VALUES
('John', 'Doe', 'johndoe@example.com', 'Premium', 81.6, 1.75, 20, 'High'),
('Jane', 'Smith', 'janesmith@example.com', 'Basic', 61.2, 1.65, 25, 'Medium'),
('Emily', 'Jones', 'emilyjones@example.com', 'VIP', 68.0, 1.70, 22, 'High'),
('Michael', 'Brown', 'michaelbrown@example.com', 'Basic', 74.8, 1.80, 15, 'Low'),
('Sarah', 'Wilson', 'sarahwilson@example.com', 'Premium', 54.4, 1.60, 18, 'Medium'),
('Kevin', 'Garcia', 'kevingarcia@example.com', 'VIP', 79.3, 1.75, 10, 'High'),
('Olivia', 'Martinez', 'oliviamartinez@example.com', 'Basic', 63.5, 1.65, 20, 'Medium'),
('James', 'Anderson', 'jamesanderson@example.com', 'Premium', 83.9, 1.85, 12, 'High');

-- Trainers 
INSERT INTO trainers (first_name, last_name, email, specialization, availability_start, availability_end) VALUES
('Alex', 'Taylor', 'alextaylor@example.com', 'Cardio and Endurance', '09:00', '17:00'),
('Morgan', 'Lee', 'morganlee@example.com', 'Strength Training', '10:00', '16:00'),
('Chris', 'Johnson', 'chrisjohnson@example.com', 'Yoga and Flexibility', '06:00', '12:00'),
('Rachel', 'Adams', 'racheladams@example.com', 'Nutrition', '08:00', '14:00'),
('Luke', 'Miller', 'lukemiller@example.com', 'Bodybuilding', '15:00', '21:00'),
('Sophia', 'Lee', 'sophialee@example.com', 'Pilates', '07:00', '13:00'),
('Ethan', 'Harris', 'ethanharris@example.com', 'Cardio', '12:00', '18:00'),
('Isabella', 'Clark', 'isabellaclark@example.com', 'Aerobics', '09:00', '15:00');

-- Administrative Staff
INSERT INTO administrative_staff (first_name, last_name, email, department, role) VALUES
('Patricia', 'Kim', 'patriciakim@example.com', 'Facilities', 'Manager'),
('Samuel', 'Brown', 'samuelbrown@example.com', 'Finance', 'Coordinator'),
('Andrea', 'Rodriguez', 'andrearodriguez@example.com', 'Member Services', 'Manager'),
('Nathan', 'Moore', 'nathanmoore@example.com', 'Customer Support', 'Assistant'),
('Chloe', 'Taylor', 'chloetaylor@example.com', 'Marketing', 'Manager'),
('Elijah', 'Davis', 'elijahdavis@example.com', 'IT Support', 'Technician'),
('Zoe', 'Evans', 'zoeevans@example.com', 'Human Resources', 'Coordinator'),
('Liam', 'Wilson', 'liamwilson@example.com', 'Maintenance', 'Supervisor');

-- Fitness Goals
INSERT INTO fitness_goals (member_id, goal_type, target_value, target_date) VALUES
(1, 'Weight Loss', 10, '2024-08-01'),
(2, 'Muscle Gain', 5, '2024-08-03'),
(3, 'Flexibility', 15, '2024-08-05'),
(4, 'Endurance', 20, '2024-08-07'),
(5, 'Weight Loss', 12, '2024-08-10'),
(6, 'Muscle Gain', 8, '2024-08-12'),
(7, 'Flexibility', 18, '2024-08-15'),
(8, 'Endurance', 25, '2024-08-17');

-- Exercise Routines
INSERT INTO exercise_routines (member_id, routine_details, routine_date) VALUES
(1, 'Cardio for 30 minutes', '2024-07-02'),
(2, 'Strength training - arms', '2024-08-04'),
(3, 'Yoga for flexibility', '2024-06-06'),
(4, 'HIIT workout', '2024-07-08'),
(5, 'Cardio for 45 minutes', '2024-06-11'),
(6, 'Strength training - legs', '2024-08-13'),
(7, 'Pilates for core strength', '2024-07-16'),
(8, 'Endurance training', '2024-08-18');

-- Fitness Achievements
INSERT INTO fitness_achievements (member_id, achievement_details, achievement_date) VALUES
(1, 'Lost 5 lbs in a month', '2024-03-05'),
(2, 'Increased muscle mass by 2%', '2024-04-07'),
(3, 'Improved flexibility by 10%', '2024-04-09'),
(4, 'Ran a 10k race', '2024-03-11'),
(5, 'Reached weight loss goal', '2024-03-14'),
(6, 'Gained 1 inch on biceps', '2024-03-16'),
(7, 'Mastered advanced yoga poses', '2024-02-19'),
(8, 'Completed a marathon', '2024-01-21');

-- Rooms
INSERT INTO rooms (room_name, capacity) VALUES
('Main Gym', 50),
('Yoga Studio', 15),
('Strength Training Room', 20),
('Cardio Room', 30),
('Dance Studio', 20),
('Free Weights Area', 25),
('Outdoor Training Area', 40),
('Private Training Room', 20);

-- Classes
INSERT INTO classes (class_name, required_equipment, availability_start, availability_end, room_id) VALUES
('Morning Yoga', 'Mats, Blocks', '08:00', '12:00', 2),
('Strength Training 101', 'Dumbbells, Barbells', '09:00', '13:00', 3),
('HIIT Circuit', 'None', '10:00', '14:00', 1),
('Advanced Yoga', 'Mats, Straps', '11:00', '15:00', 2),
('Kickboxing', 'Gloves, Pads', '12:00', '16:00', 5),
('Zumba Dance', 'None', '17:00', '20:00', 5),
('Cycling Class', 'Bikes', '07:00', '10:00', 4),
('CrossFit', 'Barbells, Dumbbells, Ropes', '16:00', '19:00', 1);

-- Bookings
INSERT INTO bookings (member_id, trainer_id, class_id, booking_type, booking_start_time, booking_end_time, room_id)
VALUES
-- Personal Training Sessions
(1, 1, NULL, 'Personal Training', '2024-05-13 09:00:00', '2024-05-13 11:00:00', 8),
(2, 2, NULL, 'Personal Training', '2024-05-13 10:00:00', '2024-05-13 12:00:00', 7),
(3, 3, NULL, 'Personal Training', '2024-05-13 10:00:00', '2024-05-13 12:00:00', 4),
(4, 4, NULL, 'Personal Training', '2024-05-13 11:00:00', '2024-05-13 13:00:00', 8),
-- Classes
(5, NULL, 1, 'Class', '2024-05-13 08:00:00', '2024-05-13 10:00:00', 2),
(6, NULL, 2, 'Class', '2024-05-13 09:00:00', '2024-05-13 12:00:00', 3),
(7, NULL, 3, 'Class', '2024-05-13 10:00:00', '2024-05-13 14:00:00', 1),
(8, NULL, 4, 'Class', '2024-05-13 11:00:00', '2024-05-13 13:00:00', 2);

-- Equipments
INSERT INTO equipment (equipment_name, last_maintenance_date) VALUES
('Treadmill #1', '2024-01-05'),
('Yoga Mats', '2024-01-15'),
('Barbell Set', '2024-01-20'),
('Elliptical #2', '2024-02-10'),
('Kettlebell Set', '2024-02-25'),
('Resistance Bands', '2024-03-05'),
('Rowing Machine #1', '2024-03-18'),
('Pull-up Bars', '2024-04-01');

-- Bills
-- Personal Training Session Bills
INSERT INTO bills (member_id, description, amount, bill_date, due_date)
SELECT b.member_id, 'session fee', 100, '2024-05-13', '2024-06-12'
FROM bookings b
WHERE b.booking_type = 'Personal Training';
-- Class Bills
INSERT INTO bills (member_id, description, amount, bill_date, due_date)
SELECT b.member_id, 'session fee', 65, '2024-05-13', '2024-06-12'
FROM bookings b
WHERE b.booking_type = 'Class';
