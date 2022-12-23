from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
# PHONE_REGEX = re.compile(r'^\([0-9]{3}\)[0-9]{3}-[0-9]{4}$')
DATABASE = 'login_and_registration'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    # # ! READ ALL THE USERS
    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM users;"
    #     results = connectToMySQL(DATABASE).query_db(query)
    #     users = []
    #     # Iterate over the db results and create instances of users with cls.
    #     for user in results:
    #         users.append(cls(user))
    #     return users

    # ! READ/RETRIEVE ONE USER
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        user = User(result[0])
        return user

    # ! GET ONE USER BY EMAIL
    @classmethod
    def get_one_with_email(cls, data) -> object or bool:
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        else:
            user = User(result[0])
        return user

    # ! CREATE/SAVE A USER TO THE DB (RETURNS AN ID)
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    # ! VALIDATE A USER
    @staticmethod
    def validate_user(user: dict) -> bool:
        is_valid = True
        # check if first name is empty or less than 2 characters
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters long.", 'first_name')
            is_valid = False
        # check if last name is empty or less than 2 characters
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters long.", 'last_name')
            is_valid = False
        # check if email doesnt match the regex
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'email')
            is_valid = False
        # check if email already exists in the db
        if User.get_one_with_email(user):
            flash("Email already exists!", 'email')
            is_valid = False
        # check if password doesnt match the regex
        if not PASSWORD_REGEX.match(user['password']):
            flash("Password must be at least 8 characters long and contain at least 1 uppercase letter and 1 number.", 'password')
            is_valid = False
        # check if password confirmation doesnt match the password
        if user['password'] != user['password_confirm']:
            flash("Passwords do not match!", 'password_confirm')
            is_valid = False
        return is_valid


