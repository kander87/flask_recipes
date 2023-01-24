from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt     
from flask_app import app, DATABASE
from flask import flash, session
from flask_app.models import model_recipe

import re
DATABASE = 'recipes_schema'

bcrypt = Bcrypt(app) 

# DATABASE = "login_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$') #add to name checks
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$') #password check


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #Hashing Upon Registration
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    #Comparing Upon Login
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        #Didn't find a matching user
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_recipes_by_id(cls,data):
        query = "SELECT * FROM users JOIN recipes ON recipes.user_id=users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        #Didn't find a matching user
        if results:
            recipe_list=[]
            this_user_instance=cls(results[0])
            # row=results[0]
            for row in results:
                recipe_data={
                    **row,
                    'id':row['recipes.id'],
                    'created_at':row['recipes.created_at'],
                    'updated_at':row['recipes.updated_at'],
                }
                this_recipe_instance = model_recipe.Recipe(recipe_data)
                recipe_list.append(this_recipe_instance)
            this_user_instance.recipes=recipe_list
            return this_user_instance
        return False


    @staticmethod
    def validate_user(user):
        is_valid = True   

        if len(user['first_name'])<2:
            flash("First name must be at least 2 characters.", "first")
            is_valid =False
        if len(user['last_name'])<2:
            flash("Last name must be at least 2 characters.", "last")
            is_valid =False
        if len(user['email'])<1:
            is_valid=False
            flash("Please enter email.", "email")
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "email")
            is_valid = False
        else: 
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query,user)
            if len(results) >= 1:
                flash("Email is already taken! If you forgot your login info, good luck!!!", "email")
                is_valid=False
        if len(user['password'])<8:
            flash("Password must be at least 8 characters.", "pass")
            is_valid =False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match!", "passcheck") 
            is_valid =False
        return is_valid

