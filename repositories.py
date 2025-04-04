import sqlite3
from models import Student, Admin, ErrorLog

class StudentRepository:
    def __init__(self, db_manager):
        self.__db_manager = db_manager
    
    def get_all_students(self):
        #Get all students from the database
        try:
            conn = self.__db_manager.get_connection()
            cursor = conn.cursor()
            # In this case I did a select all as I reuqire all fields, If I did not I would only select the reuqired ones as is more secure.
            cursor.execute("SELECT * FROM Student")
            #fetchall required in this case
            rows = cursor.fetchall()
            
            students = [Student.from_db_row(row) for row in rows]
            return students
        except Exception as e:
            #If an error occurs,Initialise WErrorLog object and store the error with the error message and source, the time is generated the method
            error_log = ErrorLog(error_message=str(e), error_source="StudentRepository.get_all_students")
            #call the log error method and pass hte variable
            self.__db_manager.log_error(error_log.to_dict()['error_message'], error_log.to_dict()['error_source'])
            raise
        finally:
            #check if connection is open and if so close it
            if conn:
                conn.close()
    
    def get_student_by_id(self, student_id):
        #Get a student by Id
        try:
            conn = self.__db_manager.get_connection()
            cursor = conn.cursor()
            #Secure Prepared Statement
            cursor.execute(
                "SELECT * FROM Student WHERE id = ?", 
                (student_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return Student.from_db_row(row)
        except Exception as e:
            error_log = ErrorLog(error_message=str(e), error_source="StudentRepository.get_student_by_id")
             #call the log error method and pass the object variables
            self.__db_manager.log_error(error_log.to_dict()['error_message'], error_log.to_dict()['error_source'])
            #raise the exception to repositories.py
            raise
        finally:
            if conn:
                conn.close()
    
    def add_student(self, student):
        #Add a new student to the database
        try:
            conn = self.__db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO Student (name, date_of_birth, email, student_type, course_name, course_code) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    student.get_name(),
                    student.get_date_of_birth(),
                    student.get_email(),
                    student.get_student_type(),
                    student.get_course_name(),
                    student.get_course_code()
                )
            )
            
            conn.commit()
            #return the last row inserted Id
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            #Integrity Error if for example an email is trying to be inserted in the database and already exists.
            #Log the Error
            error_log = ErrorLog(error_message=str(e), error_source="StudentRepository.add_student")
            self.__db_manager.log_error(error_log.to_dict()['error_message'], error_log.to_dict()['error_source'])
            raise
        except Exception as e:
            #Log Error
            error_log = ErrorLog(error_message=str(e), error_source="StudentRepository.add_student")
            self.__db_manager.log_error(error_log.to_dict()['error_message'], error_log.to_dict()['error_source'])
            raise
        finally:
            if conn:
                conn.close()
    
    def update_student(self, student):
        #Update an existing student in the database
        try:
            conn = self.__db_manager.get_connection()
            cursor = conn.cursor()
            #Inser passed Student object variables into insert statement
            cursor.execute(
                """UPDATE Student SET 
                name = ?, 
                date_of_birth = ?, 
                student_type = ?, 
                course_name = ?, 
                course_code = ? 
                WHERE id = ?""",
                (
                    student.get_name(),
                    student.get_date_of_birth(),
                    student.get_student_type(),
                    student.get_course_name(),
                    student.get_course_code(),
                    student.get_id()
                )
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            #If error occurs log it
            error_log = ErrorLog(error_message=str(e), error_source="StudentRepository.update_student")
            self.__db_manager.log_error(error_log.to_dict()['error_message'], error_log.to_dict()['error_source'])
            raise
        finally:
            if conn:
                conn.close()
    
    def delete_student(self, student_id):
        #Delete a student from the database
        try:
            conn = self.__db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM Student WHERE id = ?", (student_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            error_log = ErrorLog(error_message=str(e), error_source="StudentRepository.delete_student")
            self.__db_manager.log_error(error_log.to_dict()['error_message'], error_log.to_dict()['error_source'])
            raise
        finally:
            if conn:
                conn.close()

class AdminRepository:
    def __init__(self, db_manager):
        self.__db_manager = db_manager
    
    def get_admin_by_email(self, email):
        #Get an admin by email
        try:
            conn = self.__db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM Admin WHERE admin_email = ?", 
                (email,)
            )
            
            row = cursor.fetchone()
            
            if not row:
                return None
            
            return Admin.from_db_row(row)
        except Exception as e:
            error_log = ErrorLog(error_message=str(e), error_source="AdminRepository.get_admin_by_email")
            self.__db_manager.log_error(error_log.to_dict()['error_message'], error_log.to_dict()['error_source'])
            raise
        finally:
            if conn:
                conn.close()