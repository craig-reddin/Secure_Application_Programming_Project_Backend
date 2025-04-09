Student Management System

A secure web application for managing student records with Flask backend, SQLite Database.

Features

    •	Student record management (create, read, update, delete)

    •	Secure admin authentication

    •	Encrypted database storage

    •	JWT token-based API authorisation

    •	Error logging

    •	HTTPS/ SSL 

    •	Security protections (CORS, Content Security Policy)

Requirements

    •	Python 3.7 or higher

    •	pip (Python package installer)

    •	OpenSSL (for HTTPS certificate generation)

Setup Instructions
    1. Clone the Repository

    git clone https://github.com/craig-reddin/Secure_Application_Programming_Project_Backend.git
    
    cd Secure_Application_Programming_Project_Backend

    2. Install Dependencies

    Install all required packages:

    pip install flask flask-cors cryptography pyjwt bcrypt sqlite3 datetime secrets

    3. Generate SSL Certificate for HTTPS

    Create a self-signed certificate for development:

    openssl req -x509 -newkey rsa:4096 -nodes -out server.crt -keyout privatekey.pem -days 365

    When prompted, fill in the information for your certificate or use defaults.
     
    4. Database and Encryption Setup

    The application will automatically create and initialise the database when ran. The database file and encryption keys will be stored in a variables.txt file created by the application.

    5. Running the Application

    python app.py

    The server will run at https://127.0.0.1:5000.

    6. API Access
    For testing API endpoints, you will obtain a JWT token by signing in through the /sign_in endpoint. Use the following default admin credentials:

        •	Email: patrick012@ncistaff.com

        •	Password: password

API Endpoints

Method	Endpoint	Description	Authentication Required

    POST	/sign_in	Admin authentication	No

    GET	/students	Get all students	Yes

    GET	/student/{id}	Get student by ID	Yes

    POST	/student	Add a new student	Yes

    PUT	/student/{id}	Update student	Yes

    DELETE	/student/{id}	Delete student	Yes

Frontend
The API is configured to work with a frontend running on:

    •	https://localhost:5173

    •	https://localhost:5174
    
Available at: https://github.com/craig-reddin/Secure_Application_Programming_Project_Frontend/tree/main

If you want to connect from a different origin, update the CORS configuration in app.py.

Running Tests

python unit_tests.py

Security Notes
This application implements several security measures:

    •	Database encryption
    
    •	Password hashing

    •	JWT authentication

    •	Content Security Policy

    •	HTTPS/SSL

    •	CORS protection

    •	Prepared SQL statements to prevent injection

For production use, you would need to:

    1.	Use a proper certificate

    2.	Store encryption keys securely (not in the variable.txt file)

    3.	Set up proper environment variables

    4.	Other unforeseen security precautions

Troubleshooting
    1.	Browser Security Warnings: Since the application uses a self-signed certificate, browsers may show security warnings when using Chrome.

        If issues occur communicating from the frontend to backend, follow the below steps:
        
        a.	Open the Run dialog (Win + R) and type mmc, then press Enter.

        b.	In the Microsoft Management Console (MMC), go to File then click Add/Remove Snap-in.
        c.	Select Certificates and click Add.
        d.	Choose Computer account and click Next, then select Local Computer and click Ok.

        e.	Press Win + R, type certmgr.msc, and press Enter to open the Certificate Manager.
        
        f.	Navigate to Trusted Root Certification Authorities > Certificates.
        
        g.	Right-click on Certificates, select All Tasks > Import.
        
        h.	Import your Cert.
        
        i.	Go to chrome
        
        j.	Click on 3 dots, top right corner.
        
        k.	Click on settings, got to privacy and security
        
        l.	Click Security
        
        m.	Click manage certificates
        
        n.	Ensure “Use imported local certificates from your operating system” is toggled on.
        
        o.	Click “Manage imported certificates from Windows”


    2.	CORS Issues: If connecting from a frontend with a different origin, update the CORS configuration.
    
    3.	Database Reset: If you need to reset the database, restart the application.
    
    4.	SSL Certificate Issues: Make sure the generated SSL certificate files (server.crt and privatekey.pem) are in the same directory as app.py.

Project Structure
    
    •	app.py: Main application entry point
    
    •	api_routes.py: API endpoints
    
    •	database_manager.py: Database operations
    
    •	encryption_manager.py: Encryption and JWT utilities
    
    •	models.py: Data models
    
    •	transactions.py: Database repository classes
    
    •	unit_tests.py: Endpoint Unit Tests 
