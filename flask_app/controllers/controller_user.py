from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.model_user import User 
from flask_app.models.model_recipe import Recipe 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def register_login():
    if "user_id" in session:
        del session["user_id"]
    return render_template("index.html") 


#Hashing Upon Registration
@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    # if reque
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
        "confirm_password": bcrypt.generate_password_hash(request.form['confirm_password'])
    }

    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/recipes')


#Comparing Upon Login
@app.route('/login', methods=['POST'])
def login():
    print(request.form['email'])
    user_in_db = User.get_by_email(request.form)

    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/recipes")


@app.route('/recipes')
def success():
    if "user_id" not in session:
        return redirect('/')
    data ={
        "id": session["user_id"]
    }
    user_in_db =User.get_by_id(data)
    all_recipes = Recipe.get_all()
    return render_template("dashboard_recipes.html", user_in_db =user_in_db, all_recipes=all_recipes) 