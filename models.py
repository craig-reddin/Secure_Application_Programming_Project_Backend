from datetime import datetime
import bcrypt

class Student:
    def __init__(self, id=None, name=None, date_of_birth=None, email=None, 
                 student_type=None, course_name=None, course_code=None):
        self.__id = id
        self.__name = name
        self.__date_of_birth = date_of_birth
        self.__email = email
        self.__student_type = student_type
        self.__course_name = course_name
        self.__course_code = course_code
    
    @classmethod
    def from_db_row(cls, row):
        #Create a Student object from a database row
        if not row:
            return None
        
        return cls(
            id=row['id'],
            name=row['name'],
            date_of_birth=row['date_of_birth'],
            email=row['email'],
            student_type=row['student_type'],
            course_name=row['course_name'],
            course_code=row['course_code']
        )
    
    @classmethod
    def from_json(cls, json_data):
        #Create a Student object from JSON data
        return cls(
            id=json_data.get('id'),
            name=json_data.get('name'),
            date_of_birth=json_data.get('date_of_birth'),
            email=json_data.get('email'),
            student_type=json_data.get('student_type'),
            course_name=json_data.get('course_name'),
            course_code=json_data.get('course_code')
        )
    
    def to_dict(self):
        #Convert Student object to dictionary
        return {
            'id': self.__id,
            'name': self.__name,
            'date_of_birth': self.__date_of_birth,
            'email': self.__email,
            'student_type': self.__student_type,
            'course_name': self.__course_name,
            'course_code': self.__course_code
        }
    
    def get_id(self):
        return self.__id
    
    def get_name(self):
        return self.__name
    
    def get_date_of_birth(self):
        return self.__date_of_birth
    
    def get_email(self):
        return self.__email
    
    def get_student_type(self):
        return self.__student_type
    
    def get_course_name(self):
        return self.__course_name
    
    def get_course_code(self):
        return self.__course_code
    
    def set_name(self, name):
        self.__name = name
    
    def set_date_of_birth(self, date_of_birth):
        self.__date_of_birth = date_of_birth
    
    def set_email(self, email):
        self.__email = email
    
    def set_student_type(self, student_type):
        self.__student_type = student_type
    
    def set_course_name(self, course_name):
        self.__course_name = course_name
    
    def set_course_code(self, course_code):
        self.__course_code = course_code

class Admin:
    def __init__(self, admin_id=None, admin_name=None, admin_email=None, admin_password=None):
        self.__admin_id = admin_id
        self.__admin_name = admin_name
        self.__admin_email = admin_email
        self.__admin_password = admin_password
    
    @classmethod
    def from_db_row(cls, row):
        #Create an Admin object from a databas
        if not row:
            return None
        
        return cls(
            admin_id=row['admin_id'],
            admin_name=row['admin_name'],
            admin_email=row['admin_email'],
            admin_password=row['admin_password']
        )
    
    @classmethod
    def from_json(cls, json_data):
        #Create an Admin object from JSON data
        # Hash the password if provided
        password = json_data.get('password')
        hashed_password = None
        if password:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
        return cls(
            admin_id=json_data.get('admin_id'),
            admin_name=json_data.get('admin_name'),
            admin_email=json_data.get('email'),
            admin_password=hashed_password
        )
    
    def to_dict(self):
        #Convert Admin object to dictionary
        return {
            'admin_id': self.__admin_id,
            'admin_name': self.__admin_name,
            'admin_email': self.__admin_email,
            # Password is not included for security
        }
    
    def verify_password(self, password):
        #Verify a password against the stored hash
        if not password or not self.__admin_password:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), self.__admin_password)
    
    def get_admin_id(self):
        return self.__admin_id
    
    def get_admin_name(self):
        return self.__admin_name
    
    def get_admin_email(self):
        return self.__admin_email

class ErrorLog:
    def __init__(self, error_id=None, error_message=None, error_time=None, error_source=None):
        self.__error_id = error_id
        self.__error_message = error_message
        self.__error_time = error_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__error_source = error_source
    
    @classmethod
    def from_db_row(cls, row):
        #Create an ErrorLog object from database
        if not row:
            return None
        
        return cls(
            error_id=row['error_id'],
            error_message=row['error_message'],
            error_time=row['error_time'],
            error_source=row['error_source']
        )
    
    def to_dict(self):
        #Convert ErrorLog object to dictionary
        return {
            'error_id': self.__error_id,
            'error_message': self.__error_message,
            'error_time': self.__error_time,
            'error_source': self.__error_source
        }