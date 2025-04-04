from flask import Flask
from flask_cors import CORS
from database_manager import DatabaseManager
from api_routes import register_all_routes
from encryption_manager import EncryptionManager


class StudentManagementApp:
    def __init__(self):
        self.__app = Flask(__name__)
        self.__configure_app()
        
    def __configure_app(self):
        #Configure the Flask application with necessary middleware and settings
        # Enable CORS for specific origins
        CORS(self.__app,supports_credentials=True, resources={r"/*": {"origins": ["https://localhost:5173", "https://localhost:5174"]}})
        
        # Set up Content Security Policy
        self.__app.after_request(self.__set_csp)
        
        # Initialise variable encryption and database 
        encryption_managers = EncryptionManager()
        encryption_managers.initialise_encrypted_storage()
        
        db_manager = DatabaseManager(encryption_managers)
        db_manager.initialise_database()
        
        # Register  api endpoint routes
        register_all_routes(self.__app, db_manager)
    
    @staticmethod
    def __set_csp(response):
        #Set Content Security Policy headers
        ##Ensuring all scripts images, fonts, objects, media etc are self sourced
        #Informing communication will be coming from https://127.0.0.1:5000 (The flask server)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "font-src 'self'; "
            "img-src 'self' data:; "
            "connect-src 'self' https://127.0.0.1:5000; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "object-src 'none'; "
            "media-src 'self'; "
            "form-action 'self'; "
        )
        return response
    
    def run(self):
        #Run Flask application with SSL enabled
        self.__app.run(
            #any changes reload server
            debug=True, 
            use_reloader=True,
            
            host='127.0.0.1', 
            port=5000, 
            #Cert and Key used for https communication - not pushed to github - listed in .gitignore file.
            ssl_context=('server.crt', 'privatekey.pem')
        )

if __name__ == "__main__":
    app = StudentManagementApp()
    app.run()

