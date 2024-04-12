-- Table: Members
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    FitnessGoals VARCHAR(50),
    WeightKG FLOAT,
    HeightCM FLOAT,
    Gender VARCHAR(10),
    Age INTEGER,
    CardNumber VARCHAR(16),
    ExpirationDate VARCHAR(7),
    CVV VARCHAR(3)
);


-- Table: Trainers
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Specialization VARCHAR(255),
    ExperienceYears INTEGER
);

-- Table: Sessions
CREATE TABLE Sessions (
    SessionID SERIAL PRIMARY KEY,
    MemberID INTEGER REFERENCES Members(MemberID),
    TrainerID INTEGER REFERENCES Trainers(TrainerID),
    SessionTime TIMESTAMP,
    Cost NUMERIC(10,2)
);

-- Table: TrainerAvailability
CREATE TABLE TrainerAvailability (
    AvailabilityID SERIAL PRIMARY KEY,
    TrainerID INTEGER REFERENCES Trainers(TrainerID),
    AvailableDate DATE,
    Start TIME,
    lEnd TIME
);

-- Table: Admins
CREATE TABLE Admins (
    AdminID SERIAL PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL
);

-- Table: Rooms
CREATE TABLE Rooms (
    RoomID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Capacity INTEGER,
    Status VARCHAR(50)
);

-- Table: Equipment
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Quantity INTEGER,
    Condition VARCHAR(50)
);

-- Table: Classes
CREATE TABLE Classes (
    ClassID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Instructor VARCHAR(255),
    Schedule VARCHAR(100)
);
