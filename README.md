# Health Club Management System

## Video Demonstration
https://drive.google.com/drive/u/0/my-drive

## Authors
- Amin-Wilson Robleh #101248420
- Mahad Mohamed Yonis #101226808

## Introduction
The Health Club Management System is part of COMP 3005 Course at Carleton University's Final Project.

## Classes

### 1. Admin

**Purpose:**  
The Admin class provides functionality for administrators to manage various aspects of the health club, including member profiles, room bookings, equipment maintenance, class schedules, and billing/payment processing.

**Features:**
- View and manage member profiles
- Manage room bookings (view, add, update, delete)
- Manage equipment maintenance (view, add, update, delete)
- Update class schedules (view, add, update, delete)
- Process billing and payments for members

### 2. Member

**Purpose:**  
The Member class allows members to register, update their profiles, view their dashboards, schedule sessions, and interact with the FitnessGram network.

**Features:**
- User registration
- Profile update
- Dashboard display (including BMI calculation)
- Session scheduling
- Interaction with FitnessGram network

### 3. FitnessGramFeed

**Purpose:**  
The FitnessGramFeed class provides a feed of motivational posts for health club members to interact with. Members can like posts and share their session experiences.

**Features:**
- Display random motivational posts
- Like posts
- Share session experiences

### 4. Trainer

**Purpose:**  
The Trainer class handles trainer-related operations, including setting availability and viewing member lists.

**Features:**
- Set availability for trainers
- View member lists

  ### 5. App.py (Main Class)

**Purpose:**  
The App class serves as the main entry point for the Health Club Management System. It handles user authentication and role-based navigation within the system.

**Features:**
- User authentication
- Role-based menu selection for members, trainers, and administrators
- Integration with other classes such as Member, Trainer, and Admin for functionality execution


## Requirements
 - Install Python 3.x if not already installed on your system.
   - Install the `psycopg2` Python library by running the following command in your terminal:
     ```
     pip install psycopg2
     ```
  - PostgreSQL

## Setup Instructions
1. **Install PostgreSQL**: Ensure PostgreSQL is installed and running on your system. Create a database named `healthclub`.

2. **Create the `healthclub` Table** by Downloading the `health_fitness_club_ddl.sql` file and executing it in your PostgreSQL environment. 

3. **Populate the `healthclub` Table** by Downloading the `health_fitness_club_dml.sql` file and executing it in your PostgreSQL environment. 

## Running The Application
   - Navigate to the project directory containing `app.py` in your terminal.
   - Run the following command to start the application:
     ```
     python app.py
     ```

