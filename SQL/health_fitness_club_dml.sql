INSERT INTO Trainers (Name, Specialization)
VALUES
    ('Michael Johnson', 'Cardio'),
    ('Emily Rodriguez', 'Weightlifting');

INSERT INTO Rooms (Name, Capacity, Status)
VALUES
    ('Cardio', 20, 'Available'),
    ('Weightlifting', 15, 'Available');

INSERT INTO Equipment (Name, Quantity, Condition)
VALUES
    ('Treadmill', 5, 'Good'),
    ('Dumbbells', 50, 'Fair');

INSERT INTO Classes (Name, Instructor, Schedule)
VALUES
    ('Cardio', 'Instructor 1', 'Monday, Wednesday, Friday 8:00 AM - 9:00 AM'),
    ('Weightlifting', 'Instructor 2', 'Tuesday, Thursday 6:00 PM - 7:00 PM');

INSERT INTO Admins (Username, Password)
VALUES
    ('admin', 'pass');
