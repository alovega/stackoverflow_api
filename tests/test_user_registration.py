'''tests/test_user_registration.py'''
import json
from tests.base_test import BaseTest

class RegisterUserTestCase(BaseTest):
    '''Class testing user registration, login and logout'''
    def test_register_user(self):
        '''Test handling user registration'''
        #test successful registration
        result = self.client().post('/api/v1/auth/signup',
                                    content_type="application/json",
                                    data=json.dumps({"name": "Njeri", "username": "njery",
                                                     "email": "njery@to.cm", "password": "Test123",
                                                     "confirm_password": "Test123"}))
        #test using the same username
        result2 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Njeri", "username": "njery",
                                                      "email": "njery@to.cm", "password": "Test123",
                                                      "confirm_password": "Test123"}))
        #test using the same email
        result3 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Switch", "username": "switch",
                                                      "email": "njery@to.cm", "password": "Test123",
                                                      "confirm_password": "Test123"}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("Welcome njery!", my_data["message"])

        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 409)
        self.assertEqual("Username already exists. Try a different one.", my_data2["message"])

        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 409)
        self.assertEqual("Email already in use. Try a different one.", my_data3["message"])
        #test missing fields
        result4 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({}))
        my_data3 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("Field(s) cannot be empty", my_data3["message"])
        #test missing data fields
        result5 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Njeri", "username": "njery"}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("name, username, email, password or confirm_password fields missing",
                         my_data5["message"])

    def test_validate_data(self):
        '''Test validating user input'''
        #test invalid name with special characters
        result = self.client().post('/api/v1/auth/signup',
                                    content_type="application/json",
                                    data=json.dumps({"name": "Njeri@#", "username": "njery",
                                                     "email": "njery@to.cm", "password": "Test123",
                                                     "confirm_password": "Test123"}))
        my_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual("Name cannot contain special characters and numbers", my_data["message"])
        #test invalid email
        result2 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Njeri", "username": "njery",
                                                      "email": "abc", "password": "Test123",
                                                      "confirm_password": "Test123"}))
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 400)
        self.assertEqual("Enter a valid email address", my_data2["message"])
        #test short password
        result3 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Njeri", "username": "njery",
                                                      "email": "njery@to.cm", "password": "123",
                                                      "confirm_password": "123"}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 400)
        self.assertEqual("password is too short. Minimum length is 6 characters.", my_data3["message"])
        #test weak password
        result4 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Njeri", "username": "njery",
                                                      "email": "njery@to.cm", "password": "123456",
                                                      "confirm_password": "123456"}))
        my_data4 = json.loads(result4.data)
        self.assertEqual(result4.status_code, 400)
        self.assertEqual("password must contain a mix of upper and lowercase letters",
                         my_data4["message"])
        #test weak password
        result5 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Njeri", "username": "njery",
                                                      "email": "njery@to.cm", "password": "Testing",
                                                      "confirm_password": "Testing"}))
        my_data5 = json.loads(result5.data)
        self.assertEqual(result5.status_code, 400)
        self.assertEqual("password must contain atleast one numeric or special character",
                         my_data5["message"])
        #test unmatching passwords
        result6 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "Njeri", "username": "njery",
                                                      "email": "njery@to.cm", "password": "Test123",
                                                      "confirm_password": "Test13"}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Passwords don't match", my_data6["message"])
        #test for whitespaces
        result7 = self.client().post('/api/v1/auth/signup',
                                     content_type="application/json",
                                     data=json.dumps({"name": "  ", "username": "  ",
                                                      "email": "njery@to.cm", "password": "Test123",
                                                      "confirm_password": "Test123"}))
        my_data7 = json.loads(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Enter valid data. Look out for whitespaces in field(s).", my_data7["message"])

    def test_login_logout(self):
        '''Test user login and logout'''
        self.client().post('/api/v1/auth/signup',
                           content_type="application/json",
                           data=json.dumps({"name": "Messi", "username": "messi",
                                            "email": "messi@to.cm", "password": "Test123",
                                            "confirm_password": "Test123"}))
        #test successful login
        result = self.client().post('/api/v1/auth/login',
                                    content_type="application/json",
                                    data=json.dumps({"username": "messi", "password":"Test123"}))
        my_data = json.loads(result.data)
        a_token = my_data["token"]
        self.assertEqual(result.status_code, 200)
        self.assertEqual("Welcome back, messi!", my_data["message"])
        self.assertIn("token", my_data)
        #test wrong username
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type="application/json",
                                     data=json.dumps({"username": "none", "password":"Test123"}))
        my_data2 = json.loads(result2.data)
        self.assertEqual(result2.status_code, 401)
        self.assertEqual("Username doesn't exixt. Try Signing up.", my_data2["message"])
        #test wrong password
        result3 = self.client().post('/api/v1/auth/login',
                                     content_type="application/json",
                                     data=json.dumps({"username": "messi", "password":"Testing"}))
        my_data3 = json.loads(result3.data)
        self.assertEqual(result3.status_code, 401)
        self.assertEqual("Incorrect password", my_data3["message"])
        #test logout
        result4 = self.client().post('/api/v1/auth/logout',
                                     headers=dict(Authorization="Bearer " + a_token))
        result5 = self.client().post('/api/v1/auth/logout',
                                     headers=dict(Authorization="Bearer " + a_token))
        my_data4 = json.loads(result4.data)
        my_data5 = json.loads(result5.data)
        self.assertEqual(result4.status_code, 200)
        self.assertEqual(result5.status_code, 401)
        self.assertEqual("Leaving so soon?", my_data4["message"])
        self.assertEqual("Token has been revoked", my_data5["msg"])
        #test missing input data
        result6 = self.client().post('/api/v1/auth/login',
                                    content_type="application/json",
                                    data=json.dumps({}))
        my_data6 = json.loads(result6.data)
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Field(s) cannot be empty", my_data6["message"])
        #test empty content
        result7 = self.client().post('/api/v1/auth/login',
                                    content_type="application/json",
                                    data=json.dumps({"username":"", "password":""}))
        my_data7 = json.loads(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Username or password fields missing", my_data7["message"])
