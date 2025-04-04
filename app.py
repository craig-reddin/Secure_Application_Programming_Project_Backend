# Import libraries
import sqlite3
import os
from flask import Flask, request, jsonify

# Import the CORS function to allow cross-origin requests
from flask_cors import CORS  

# Initialising Flask app
app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Path to the database file
DATABASE_PATH = "students.db"

# Function to delete the database if it exists
def reset_database():
    # Checking if the database exists, if does, delete it
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("Existing database deleted.")

# Function to connect to SQLite database
def get_db_connection():
    # connect to the SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries
    return conn

# Function to create the database and tables
def init_db():
    # Reset the database if it exists
    reset_database()  
    conn = get_db_connection()
    cursor = conn.cursor()

    # Creating the Student table
    cursor.execute(''' 
        CREATE TABLE Student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            student_type TEXT NOT NULL,
            course_name TEXT NOT NULL,
            course_code TEXT NOT NULL
        )
    ''')
    conn.commit()
    print("Database and Student table created.")
    
    # Creating the Admin table
    cursor.execute(''' 
        CREATE TABLE Admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_name TEXT NOT NULL,
            admin_email TEXT UNIQUE NOT NULL,
            admin_password TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Insert sample students and admin
    insert_sample_students(conn)
    insert_sample_admin(conn)
    
    conn.close()

# Function to insert sample admin data
def insert_sample_admin(conn):
    # Sample admin data to insert into the Admin table
    admin = [
        ("Patrick Yeats", "patrick012@ncistaff.com", "password")
    ]
    cursor = conn.cursor()
    # Inserting the sample admin
    cursor.executemany("INSERT INTO Admin (admin_name, admin_email, admin_password) VALUES (?, ?, ?)", admin)
    conn.commit()
    print("Sample Admin inserted.")

# Function to insert sample student data
def insert_sample_students(conn):
    cursor = conn.cursor()

    # Sample student data
    students = [
        ("Steven Malone", "2005-12-05", "alice@nci.com", "Student", "Computer Science", "CS101"),
        ("Bob Johnson", "1995-05-05", "bob@nci.com", "Mature Student", "Data Science", "DS501"),
        ("Charlie Brown", "1991-04-12", "charlie@nci.com", "Student", "Cybersecurity", "CY202")
    ]
    # Inserting the sample students
    cursor.executemany("INSERT INTO Student (name, date_of_birth, email, student_type, course_name, course_code) VALUES (?, ?, ?, ?, ?, ?)", students)
    conn.commit()
    print("Sample students inserted.")

# Route to get all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Querying the Student table to get all students
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    conn.close()
    # Returning the list of students as JSON
    return jsonify([dict(student) for student in students])

# Route to get a student by Id
@app.route("/student/<int:id>", methods=["GET"])
def get_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Querying the Student table for a specific student by Id
    cursor.execute("SELECT * FROM Student WHERE id = "+ str(id) )
    student = cursor.fetchone()
    conn.close()
    if student:
        # Returning the student as json if found
        return jsonify(dict(student))
    # Returning an error message if student is not found
    return jsonify({"error": "Student not found"}), 404

# Route to add a new student
@app.route("/student", methods=["POST"])
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Inserting a new student into the Student table
        cursor.execute("INSERT INTO Student VALUES ('" 
               + data["name"] + "', '" 
               + data["date_of_birth"] + "', '" 
               + data["email"] + "', '" 
               + data["student_type"] + "', '" 
               + data["course_name"] + "', '" 
               + data["course_code"] + "')")
        conn.commit()
        conn.close()
        # Returning a success message
        return jsonify({"message": "Student added successfully"}), 201
    except sqlite3.IntegrityError:
        conn.close()
        # If email already exists
        return jsonify({"error": "Email already exists"}), 400

# Route for sign-in
@app.route("/sign_in", methods=["POST"])
def sign_in():
    data = request.json
    email = data.get("email")
    password = data.get("password") 
    print(email)
    print(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Query the Admin table to validate the admin credentials
        cursor.execute("SELECT admin_email, admin_password FROM Admin WHERE admin_email = '" + email + "'")        
        admin = cursor.fetchone()  # Retrieve the first result
        if admin is None:
            # If admin not found, return an error
            return jsonify({"error": "Incorrect Credentials"}), 400

        # Checking if the passed password matches the stored password
        if (password == admin["admin_password"]):
            # If login is successful, return a success message
            return jsonify({"message": "Admin logged in successfully"})
        else:
            # If the password does not match, return an error
            return jsonify({"error": "Incorrect Credentials"}), 400

    except sqlite3.DatabaseError as e:
        # Handling any database errors
        return jsonify({"error": "Database error", "message": str(e)}), 500
    finally:
        conn.close()

# Route to update a student
@app.route("/student/<int:id>", methods=["PUT"])
def update_student(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Student WHERE id = ?", (id,))
    student = cursor.fetchone()

    if student:
        # Updating student details in the database
        cursor.executescript("UPDATE Student SET name = '" + data.get("name", student["name"]) + 
               "', date_of_birth = '" + data.get("date_of_birth", student["date_of_birth"]) + 
               "', student_type = '" + data.get("student_type", student["student_type"]) + 
               "', course_name = '" + data.get("course_name", student["course_name"]) + 
               "', course_code = '" + data.get("course_code", student["course_code"]) + 
               "' WHERE id = " + str(id))
        conn.commit()
        conn.close()
        # Returning a success message
        return jsonify({"message": "Student updated successfully"})

    # Returning an error if the student is not found
    return jsonify({"error": "Student not found"}), 404

# Route to delete a student
@app.route("/student/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Student WHERE id = "  + str(id))
    student = cursor.fetchone()

    if student:
        # Deleting the student from the database
        cursor.execute("DELETE FROM Student WHERE id = " + str(id))
        conn.commit()
        conn.close()
        # Returning a success message
        return jsonify({"message": "Student deleted successfully"})

    # Returning an error if the student is not found
    return jsonify({"error": "Student not found"}), 404

# Initialises the database and creating tables before running the Flask app
init_db()

# Run the Flask app with debugging enabled
if __name__ == "__main__":
    app.run(
        debug=True, 
    )
