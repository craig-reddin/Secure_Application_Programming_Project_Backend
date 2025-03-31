import unittest
import json
from app import app, init_db

# https://a-n-rose.github.io/2018/11/07/unittest-sqlite3-classes/
# https://python.plainenglish.io/introduction-to-unit-testing-d7c1fb0ee2ea

class FlaskAppTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Initialise the database before running tests
        cls.client = app.test_client()
    
    def setUp(self):
        # initialise database before each test
        init_db()  

    def test_get_students(self):
        response = self.client.get("/students")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
    
    def test_get_student_by_id(self):
        response = self.client.get("/student/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json)
    
    
    def test_get_student_by_id_invalid_id(self):
        response = self.client.get("/student/10")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json)
        


    def test_add_student(self):
        student = {
            "name": "Test Student",
            "date_of_birth": "2000-01-01",
            "email": "test_student@nci.com",
            "student_type": "Student",
            "course_name": "AI",
            "course_code": "AI101"
        }
        response = self.client.post("/student", data=json.dumps(student), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "Student added successfully")
        

    def test_sign_in_valid(self):
        admin = {
            "email": "patrick012@ncistaff.com",
            "password": "password"
        }
        response = self.client.post("/sign_in", data=json.dumps(admin), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Admin logged in successfully")

    def test_sign_in_invalid_password(self):
        admin = {
            "email": "patrick012@ncistaff.com",
            "password": "password1"
        }
        response = self.client.post("/sign_in", data=json.dumps(admin), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Incorrect Credentials")
        
    def test_sign_in_invalid_email(self):
        admin = {
            "email": "patrick012@nci.com",
            "password": "password1"
        }
        response = self.client.post("/sign_in", data=json.dumps(admin), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Incorrect Credentials")        

    def test_update_student(self):
        update_data = {
            "name": "New Craig"
        }
        response = self.client.put("/student/1", data=json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Student updated successfully")
    
    def test_delete_student(self):
        response = self.client.delete("/student/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Student deleted successfully")
        
    def test_delete_student_invalid_number(self):
        response = self.client.delete("/student/12")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Student not found")    
        
    

if __name__ == "__main__":
    unittest.main()
