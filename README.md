Insecure Student Management System

A basic web application for managing students, built with Flask and SQLite.

Features

•	Student record management (create, read, update, delete)

•	Admin login endpoint (without authentication)

•	SQLite database storage

•	RESTful API endpoint

•	Cross-Origin Resource Sharing (CORS) support

Requirements

•	Python 3.7 or higher

•	pip (Python package installer)


Setup Instructions
    
    1. Clone the Repository

    git clone https://github.com/craig-reddin/Secure_Application_Programming_Project_Backend.git

    cd Secure_Application_Programming_Project_Backend

    2. Install Dependencies

    Install all required packages:
    
    pip install flask flask-cors
    
    Note: sqlite3 and os are part of the Python standard library and don't need to be installed separately.
 
    3. Running the Application
    
    python app.py
    
    The server will start at http://127.0.0.1:5000 by default.
    
    The database (students.db) will be automatically created and populated with sample data when the application starts.

API Endpoints

    Method	Endpoint	Description

    POST	/sign_in	Admin login 

    GET	/students	Get all students

    GET	/student/{id}	Get student by ID

    POST	/student	Add a new student

    PUT	/student/{id}	Update student

    DELETE	/student/{id}	Delete student

Frontend 

    The API has CORS enabled, allowing it to be called from web applications running on different origins.

    Available at: https://github.com/craig-reddin/Secure_Application_Programming_Project_Backend/tree/insecure

Security Notes

    1.	No Password hashing
    
    2.	No Input validation and sanitisation (current implementation is vulnerable to SQL injection)
    
    3.	No Proper authentication / session management implemented
    
    4.	HTTP is implemented and HTTPS/SSL is not supported
    
    5.	No proper error handling
