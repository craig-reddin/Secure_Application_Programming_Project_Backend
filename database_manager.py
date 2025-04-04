import sqlite3
import os
from datetime import datetime
import bcrypt


class DatabaseManager:
    def __init__(self, encryption_manager):
        self.__encryption_manager = encryption_manager
        self.__db_path = None
    
    def initialise_database(self):
        #Initialise the database by creating tables and sample data
        self.__reset_database()
        conn = self.__get_connection()
        
        # Create tables
        self.__create_tables(conn)
        
        # Insert sample data
        self.__insert_sample_data(conn)
        
        conn.close()
        print("Database Created Successfully")
    
    def __reset_database(self):
        #Delete existing database if it exists
        db_path = self.__get_db_path()
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Existing database deleted")
    
    def __get_db_path(self):
        #Get the decrypted database path
        if not self.__db_path:
            #extract encrypted data from variables.txt
            encrypted_data = self.__encryption_manager.read_encrypted_data("variables.txt")
            #Allocate Encrpted database route
            route_encrypted = encrypted_data.get("DATABASE_ROUTE")
            #Allocate encrytpion iv
            iv_encrypted = encrypted_data.get("DATABASE_IV")
            #decrypt the database file path
            self.__db_path = self.__encryption_manager.decrypt(route_encrypted, iv_encrypted)
            #return the database path 
        return self.__db_path
    
    def __create_tables(self, conn):
        #Create all required database tables
        cursor = conn.cursor()
        # Create Student table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                name VARCHAR(100) NOT NULL,  
                date_of_birth VARCHAR(12) NOT NULL,  
                email VARCHAR(100) UNIQUE NOT NULL,  
                student_type VARCHAR(25) NOT NULL,  
                course_name VARCHAR(25) NOT NULL,  
                course_code VARCHAR(10) NOT NULL  
            )
        ''')
        
        # Create Admin table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS Admin (
                admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin_name VARCHAR(100) NOT NULL,  
                admin_email VARCHAR(100) UNIQUE NOT NULL,  
                admin_password VARCHAR(100) NOT NULL  
            )
        ''')
        
        # Create ErrorLog table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS ErrorLog (
                error_id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_message TEXT NOT NULL,
                error_time VARCHAR (100) NOT NULL,
                error_source VARCHAR (30) NOT NULL
            )
        ''')
        
        conn.commit()
        
    
    def __insert_sample_data(self, conn):
        #Insert sample data into the database
        cursor = conn.cursor()
        
        # Insert sample students
        students = [
            ("Steven Malone", "2005-12-05", "alice@nci.com", "Student", "Computer Science", "CS101"),
            ("Bob Johnson", "1995-05-05", "bob@nci.com", "Mature Student", "Data Science", "DS501"),
            ("Charlie Brown", "1991-04-12", "charlie@nci.com", "Student", "Cybersecurity", "CY202")
        ]
        cursor.executemany(
            "INSERT INTO Student (name, date_of_birth, email, student_type, course_name, course_code) VALUES (?, ?, ?, ?, ?, ?)",
            students
        )
        
        # Insert sample admin with hashed password
        password = "password"
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO Admin (admin_name, admin_email, admin_password) VALUES (?, ?, ?)",
            ("Patrick Yeats", "patrick012@ncistaff.com", hashed_password)
        )
        
        conn.commit()
    
    def get_connection(self):
        #Public method to get a database connection
        return self.__get_connection()
    
    def __get_connection(self):
        #Private method to get a database connection
        conn = sqlite3.connect(self.__get_db_path())
        # Enables fetching rows as dictionaries - easier for sending to the frontend
        conn.row_factory = sqlite3.Row  
        return conn
    
    def log_error(self, error_message, error_source):
        #Log an error to the database
        try:
            conn = self.__get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ErrorLog (error_message, error_time, error_source) VALUES (?, ?, ?)",
                (error_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), error_source)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error logging failed: {str(e)}")
        finally:
            if conn:
                conn.close()