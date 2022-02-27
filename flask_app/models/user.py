from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class User:
    db_log= 'login_registration'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def new_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"
        result = connectToMySQL(cls.db_log).query_db(query,data)
        return result

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_log).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL(cls.db_log).query_db(query, data)
        print(result)
        return cls(result[0])

    @staticmethod
    def valid_register(data):
        is_valid = True
        if not data['first_name']:
            is_valid = False
            flash('This is a required field', 'error_firstname')
        elif len(data['first_name']) < 2:
            is_valid = False
            flash('First name must be at least 2 characters', 'error_firstname')
        if not data['last_name']:
            is_valid = False
            flash('This is a required field', 'error_lastname')
        elif len(data['last_name']) < 3:
            is_valid = False
            flash('Last name must be at least 2 characters', 'error_lastname')
        if not data['email']:
            is_valid = False
            flash('This is a required field', 'error_email')
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_log).query_db(query,data)
        if len(results) >= 1:
            is_valid = False
            flash('Email already in system', 'error_email')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Invalid Email', 'error_email')
        if not data['password']:
            is_valid = False
            flash('This is a required field', 'error_password')
        if not data['password2']:
            is_valid = False
            flash('This is a required field', 'error_password2')
        if data['password'] != data['password2']:
            is_valid = False
            flash('Password must match', 'error_password')
        elif len(data['password']) < 8:
            is_valid = False
            flash('Must be greater than 8 characters', 'error_password')
        return is_valid

    @staticmethod
    def valid_login(data):
        is_valid = True
        user_in_db = User.get_email(data)
        if not user_in_db:
            flash("Invalid login/password", 'error_login')
            is_valid = False
        elif not bcrypt.check_password_hash(user_in_db.password, data["password"]):
            flash("Invalid login/password", 'error_login')
            is_valid = False
        return is_valid