from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, DATABASE
from flask import flash, session, redirect
from flask_app.models import model_user
# from flask_app.models.model_user import User
DATABASE = 'recipes_schema'



class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.date_cooked = data['date_cooked']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes ( name, description, instructions, under, date_cooked, user_id) VALUES ( %(name)s , %(description)s , %(instructions)s ,%(under)s, %(date_cooked)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes=[]
        if results:
            for row in results:
                this_recipe=cls(row)
                user_data={
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    **row
                }
                this_user = model_user.User(user_data)
                this_recipe.maker=this_user
                all_recipes.append(this_recipe)
        return all_recipes

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id =users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            this_recipe = cls(results[0])
            row= results[0]
            user_data ={
                **row,
                'id':row['users.id'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at'],
            }
            this_user = model_user.User(user_data)
            this_recipe.maker =this_user
            return this_recipe
        return False


    @classmethod
    def edit(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description= %(description)s  , instructions = %(instructions)s ,under = %(under)s, date_cooked= %(date_cooked)s,user_id =%(user_id)s WHERE id= %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM recipes WHERE id= %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(DATABASE).query_db( query, data )

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True   
        if len(recipe['name'])<1:
            flash("Please enter a name for your recipe!", "name")
            is_valid =False
        if len(recipe['description'])<5:
            flash("Please enter a description for your recipe! It must be at least 5 characters!", "description")
            is_valid =False
        if len(recipe['instructions'])<10:
            flash("Please enter instructions for your recipe! It must be at least 10 characters!", "instructions")
            is_valid =False
        if len(recipe['date_cooked']) <8:
            flash("Please enter a date for your recipe!", "date_cooked")
            is_valid =False
        if 'under' not in recipe:
            flash("Please select if your recipe is under 30 minutes or not!", "under")
            is_valid =False
        return is_valid