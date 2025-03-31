#import to leverage endpoints
from flask import Flask
#overcome Same Origin Policy
from flask_cors import CORS
#method to initialise database
from database import init_db
#all endpoints of the application
from routes import students_bp, student_details_bp, add_student_bp, sign_in_bp, update_student_bp, delete_student_bp
#method to encrypt the path to the database and save it in a file using AES encryption - calls 2 methods.
from encryption import load_data

# Setting up the Flask app
app = Flask(__name__)

# Enabling CORS for the whole application to handle requests from different origins
CORS(app)

# Allows the frontend running on localhost:5173 to make requests
CORS(app, resources={r"/*": {"origins": "*"}})
#Call load data before initialing the database.
load_data()
# Initialise the database
init_db()

@app.after_request
def set_csp(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' "
        "style-src 'self' "
        "font-src 'self'; "
        "img-src 'self' data:; "
        "connect-src 'self' https://127.0.0.1:5000 https://localhost:5000; "
        "frame-ancestors 'none'; "
        "base-uri 'self';"
    )
    return response


# Register the routes
app.register_blueprint(students_bp)
app.register_blueprint(student_details_bp)
app.register_blueprint(add_student_bp)
app.register_blueprint(sign_in_bp)
app.register_blueprint(update_student_bp)
app.register_blueprint(delete_student_bp)

if __name__ == "__main__":
    # Running the Flask app with SSL enabled
    app.run(debug=True, use_reloader=True,host='127.0.0.1', port=5000, ssl_context=('server.crt', 'privatekey.pem'))