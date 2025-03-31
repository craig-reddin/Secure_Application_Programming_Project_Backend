from flask import Blueprint, request, jsonify
from database import get_db_connection, log_error
import bcrypt
import sqlite3

# Blueprints for different routes
students_bp = Blueprint('students', __name__)  
student_details_bp = Blueprint('student_details', __name__)  
add_student_bp = Blueprint('add_student', __name__)  
sign_in_bp = Blueprint('sign_in', __name__) 
update_student_bp = Blueprint('update_student', __name__)  
delete_student_bp = Blueprint('delete_student', __name__)  

# Route to get all students
@students_bp.route("/students", methods=["GET"])
def get_students():
    try:
        #connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        #database query
        cursor.execute("SELECT * FROM Student")
        #fetch all students 
        students = cursor.fetchall()
        #close connection
        conn.close()
        #return students in JSON format. 
        return jsonify([dict(student) for student in students])
    except Exception as e:
        #log the error in the error log table - pass the error and the method name in which it occured
        log_error(str(e), "get_students")
        #return JSON message back to user for user friendly interaction
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

# Route to get a student by ID
@student_details_bp.route("/student/<int:id>", methods=["GET"])
def get_student(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        #database query with the passed user id.
        cursor.execute("SELECT * FROM Student WHERE id = ?", (id,))
        #single student
        student = cursor.fetchone()
        #close connection
        conn.close()

        #if student is returned
        if student:
            #return the student in JSON format
            return jsonify(dict(student))
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        # Log error and return message to user
        log_error(str(e), "get_student")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

# Route to add a new student
@add_student_bp.route("/student", methods=["POST"])
def add_student():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        #Database query inserting new student with passed values from front end form.
        cursor.execute("INSERT INTO Student (name, date_of_birth, email, student_type, course_name, course_code) VALUES (?, ?, ?, ?, ?, ?)",
                       (data["name"], data["date_of_birth"], data["email"], data["student_type"], data["course_name"], data["course_code"]))
        conn.commit()
        conn.close()
        #return successful message to user
        return jsonify({"message": "Student added successfully"}), 201
    #SQLite exception
    except sqlite3.IntegrityError as e:
        log_error(str(e), "add_student")
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()
    

# Route to handle admin sign-in
@sign_in_bp.route("/sign_in", methods=["POST"])
def sign_in():
    try:
        data = request.json
        #email and password are passed from client
        email = data.get("email")
        password = data.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        #QUery to select Student email and password and compare password to passed value that is hashed
        cursor.execute("SELECT admin_email, admin_password FROM Admin WHERE admin_email = ?", (email,))
        admin = cursor.fetchone()
        conn.close()
        #check if there is no admin or if the hashed password does not match the passed hashed password 
        if admin is None or not bcrypt.checkpw(password.encode('utf-8'), admin["admin_password"]):
            return jsonify({"error": "Incorrect Credentials"}), 400
        #if does match, send message to user
        return jsonify({"message": "Admin logged in successfully"})
    except Exception as e:
        log_error(str(e), "sign_in")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()
        

# Route to update a student's information
@update_student_bp.route("/student/<int:id>", methods=["PUT"])
def update_student(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        #Select query to ensure student exists before updating 
        cursor.execute("SELECT * FROM Student WHERE id = ?", (id,))
        student = cursor.fetchone()

        #if a student is returned, update the student with the passed values
        if student:
            cursor.execute("""
                UPDATE Student SET name = ?, date_of_birth = ?, student_type = ?, course_name = ?, course_code = ?
                WHERE id = ?""", 
                (data.get("name", student["name"]),
                 data.get("date_of_birth", student["date_of_birth"]),
                 data.get("student_type", student["student_type"]),
                 data.get("course_name", student["course_name"]),
                 data.get("course_code", student["course_code"]),
                 id))
            conn.commit()
            conn.close()
            #return message to user
            return jsonify({"message": "Student updated successfully"}),200
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        log_error(str(e), "update_student")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()

# Route to delete a student
@delete_student_bp.route("/student/<int:id>", methods=["DELETE"])
def delete_student(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

   
        # select to ensure the student exists befoee deleting
        cursor.execute("SELECT * FROM Student WHERE id = ?", (id,))
        student = cursor.fetchone()

        if student:
            cursor.execute("DELETE FROM Student WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            return jsonify({"message": "Student deleted successfully"})
        
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    except Exception as e:
        log_error(str(e), "delete_student")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        conn.close()
