import sqlite3
import os
from datetime import datetime
import bcrypt
from flask import jsonify
from encryption import encrypt, decrypt,read_encrypted_data, save_to_text_file, Secret_Key
#create table python
#https://www.geeksforgeeks.org/python-sqlite-create-table/

#Crud operations of Studnet Table
#https://medium.com/@sdmodels/a-guide-to-using-sqlite-with-python-a45d7fc68c36

def load_db_intitialisation_values():

    encrypted_file = "variables.txt"
    extracted_data = read_encrypted_data(encrypted_file)

    # Get the encrypted values from extracted data
    route_encrypted = extracted_data.get("DATABASE_ROUTE")
    iv_encrypted = extracted_data.get("DATABASE_IV")

    decrypted_message = decrypt(Secret_Key, route_encrypted, iv_encrypted)
    return decrypted_message




# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(load_db_intitialisation_values())
    # Makes fetching rows as dictionaries
    conn.row_factory = sqlite3.Row  
    return conn

# This function deletes the database if it already exists
def reset_database():
    if os.path.exists(load_db_intitialisation_values()):
        os.remove(load_db_intitialisation_values())
        print("Existing database deleted")

# Function to initialise the database and tables
def init_db():
    # Reset the database if it exists
    reset_database()  
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Student, Admi and Logging tables
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
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_name VARCHAR(100) NOT NULL,  
            admin_email VARCHAR(100) UNIQUE NOT NULL,  
            admin_password VARCHAR(50) NOT NULL 
        )
    ''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS ErrorLog (
            error_id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message TEXT NOT NULL,
            error_time VARCHAR(15) NOT NULL,
            error_source VARCHAR(75) NOT NULL
        )
    ''')

    # Inserting sample data
    insert_sample_admin(conn)
    insert_sample_students(conn)

    #commit transactions
    conn.commit()
    #close connection
    conn.close()
    print("database Created")

# Function to insert sample admin data into the Admin table
def insert_sample_admin(conn):
    #hardcoding a password to hash, I am using password as it is eay to remember, I understand this is not a safe passwrod to use in a production environment. 
    password = 'password'
    #hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor = conn.cursor()
    #Insert the new admin with hardcoded values and the hashed password
    cursor.executemany("INSERT INTO Admin (admin_name, admin_email, admin_password) VALUES (?, ?, ?)",
                       [("Patrick Yeats", "patrick012@ncistaff.com", hashed_password)])
    conn.commit()

# Function to insert sample students into the Student table
def insert_sample_students(conn):
    cursor = conn.cursor()
    #Array of Students inserted into the Student table
    students = [
        ("Steven Malone", "2005-12-05", "alice@nci.com", "Student", "Computer Science", "CS101"),
        ("Bob Johnson", "1995-05-05", "bob@nci.com", "Mature Student", "Data Science", "DS501"),
        ("Charlie Brown", "1991-04-12", "charlie@nci.com", "Student", "Cybersecurity", "CY202")
    ]
    cursor.executemany("INSERT INTO Student (name, date_of_birth, email, student_type, course_name, course_code) VALUES (?, ?, ?, ?, ?, ?)", students)
    conn.commit()

# Error logging function
def log_error(error_message, error_source):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ErrorLog (error_message, error_time, error_source) VALUES (?, ?, ?)", 
                       (error_message, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), error_source))
        conn.commit()
        conn.close()
    except Exception as e:
       print("")
