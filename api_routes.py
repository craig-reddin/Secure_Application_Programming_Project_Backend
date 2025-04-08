from functools import wraps
from flask import Blueprint, request, jsonify, make_response
from models import ErrorLog, Student
import sqlite3
from transactions import StudentRepository, AdminRepository;
from encryption_manager import EncryptionManager, verify_jwt

class StudentController:

    def __init__(self, student_repository):
        self.__student_repository = student_repository
    
    @verify_jwt  
    def get_all_students(self):
        #API endpoint to get all students
        try:
            #call get all students method 
            students = self.__student_repository.get_all_students()
            #loop through stuudent and change each student to dictionary data structure
            dictionary = [student.to_dict() for student in students]
            #return JSON dictionary
            return jsonify(dictionary)
        except Exception:
            #return error message
            return jsonify({"error": "Internal Server Error"}), 500
    
    
    @verify_jwt  
    def get_student_by_id(self, student_id):
        #API endpoint to get a student by Id
        try:
            student = self.__student_repository.get_student_by_id(student_id)
            
            if student:
                return jsonify(student.to_dict())
            
            return jsonify({"error": "Student not found"}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500
    
    @verify_jwt  
    def add_student(self):
        #API endpoint to add a new student
        try:
            data = request.json
            student = Student.from_json(data)
            
            student_id = self.__student_repository.add_student(student)
            
            return jsonify({"message": "Student added successfully", "id": student_id}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already exists"}), 400
        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500
    
    @verify_jwt  
    def update_student(self, student_id):
        #API endpoint to update a student
        try:
            data = request.json
            
            # Get existing student first
            existing_student = self.__student_repository.get_student_by_id(student_id)
            
            if not existing_student:
                return jsonify({"error": "Student not found"}), 404
            
            # Update with new data retrieved from the database
            if 'name' in data:
                existing_student.set_name(data['name'])
            if 'date_of_birth' in data:
                existing_student.set_date_of_birth(data['date_of_birth'])
            if 'student_type' in data:
                existing_student.set_student_type(data['student_type'])
            if 'course_name' in data:
                existing_student.set_course_name(data['course_name'])
            if 'course_code' in data:
                existing_student.set_course_code(data['course_code'])
            #update the student in the database with student object new values - returns boolean
            success = self.__student_repository.update_student(existing_student)
            
            if success:
                return jsonify({"message": "Student updated successfully"})
            
            return jsonify({"error": "Failed to update student"}), 500
        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500
  
    @verify_jwt  
    def delete_student(self, student_id):
        #API endpoint to delete a student
        try:
            # Check if student exists before deleting student
            existing_student = self.__student_repository.get_student_by_id(student_id)
            
            if not existing_student:
                return jsonify({"error": "Student not found"}), 404
            
            success = self.__student_repository.delete_student(student_id)
            
            if success:
                return jsonify({"message": "Student deleted successfully"})
            
            return jsonify({"error": "Failed to delete student"}), 501
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error"}), 500

class AuthController:
    def __init__(self, admin_repository):
        self.__admin_repository = admin_repository
    
    def sign_in(self):
        #API endpoint for admin sign-in
        try:
            em = EncryptionManager()
            data = request.json
            email = data.get("email")
            password = data.get("password")
            
            if not email or not password:
                return jsonify({"error": "Email and password are required"}), 400
            
            admin = self.__admin_repository.get_admin_by_email(email)
            
            if not admin or not admin.verify_password(password):
                return jsonify({"error": "Incorrect Credentials"}), 400
            
            token = em.generate_jwt(email)
            response = make_response(jsonify({"message": "Admin logged in successfully","token": token}))
            response.set_cookie("jwt", token, httponly=True, secure=True, samesite="Strict")
            return response
        except Exception as e:
            print(e)
            return jsonify({"error": "Internal Server Error"}), 500

def register_all_routes(app, db_manager):
    #Register all API routes
    # Create repositories
    student_repository = StudentRepository(db_manager)
    admin_repository = AdminRepository(db_manager)
    
    # Create controllers
    student_controller = StudentController(student_repository)
    auth_controller = AuthController(admin_repository)
    
    # Register student routes
    students_bp = Blueprint('students', __name__)
    students_bp.route("/students", methods=["GET"])(student_controller.get_all_students)
    app.register_blueprint(students_bp)
    
    student_details_bp = Blueprint('student_details', __name__)
    student_details_bp.route("/student/<int:student_id>", methods=["GET"])(student_controller.get_student_by_id)
    app.register_blueprint(student_details_bp)
    
    add_student_bp = Blueprint('add_student', __name__)
    add_student_bp.route("/student", methods=["POST"])(student_controller.add_student)
    app.register_blueprint(add_student_bp)
    
    update_student_bp = Blueprint('update_student', __name__)
    update_student_bp.route("/student/<int:student_id>", methods=["PUT"])(student_controller.update_student)
    app.register_blueprint(update_student_bp)
    
    delete_student_bp = Blueprint('delete_student', __name__)
    delete_student_bp.route("/student/<int:student_id>", methods=["DELETE"])(student_controller.delete_student)
    app.register_blueprint(delete_student_bp)
    
    # Register authentication routes
    sign_in_bp = Blueprint('sign_in', __name__)
    sign_in_bp.route("/sign_in", methods=["POST"])(auth_controller.sign_in)
    app.register_blueprint(sign_in_bp)
    
    