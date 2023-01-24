from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.model_user import User 
from flask_app.models.model_recipe import Recipe 
from flask_app.controllers import controller_user 

@app.route('/recipe/create')
def recipe_create():
    if "user_id" not in session:
        return redirect('/')
    data={
        'id': session['user_id']
    }
    return render_template("recipe_create.html", user=User.get_by_id(data)) 

@app.route('/recipe/new/', methods=["POST"])
def recipe_add():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipe/create')
    data={
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under': int(request.form['under']),
        'date_cooked': request.form['date_cooked'],
        'user_id': session['user_id'],
    }
    Recipe.validate_recipe(request.form)
    Recipe.create(data)
    print("adding recipe")
    return redirect('/recipes')


@app.route('/recipe/view/<int:id>')
def recipe_view(id):
    data={
        'id': id
    }
    user_data={
        'id' : session['user_id']
    }
    Recipe.get_by_id(data)
    print("showing recipe")
    return render_template("recipe_view.html", recipe=Recipe.get_by_id(data), user=User.get_by_id(user_data))


@app.route('/recipe/edit/<int:id>')
def recipe_edit(id):
    data={
        'id': id
    }
    user_data={
        'id' : session['user_id']
    }
    edit=Recipe.get_by_id(data)
    user=User.get_by_id(user_data)
    return render_template("recipe_edit.html", edit=edit, user=user) 

@app.route('/recipe/update/<int:id>', methods=['POST'])
def recipe_update(id):
    if "user_id" not in session:
        return redirect('/')
    data = { 
        'id':id,
        'name': request.form['name'],
        'description': request.form['descrsiption'],
        'instructions': request.form['instructions'],
        'under': int(request.form['under']),
        'date_cooked': request.form['date_cooked'],
        'user_id': session['user_id'],
    }   
    Recipe.validate_recipe(request.form)
    Recipe.edit(data)
    print("editing recipe")
    return redirect("/recipes")

@app.route("/myrecipes")
def show_users_recipes():
    user_in_db= User.get_recipes_by_id({'id':session['user_id']})
    print(User.get_recipes_by_id({'id':session['user_id']}))
    return render_template("my_recipes.html", user_in_db=user_in_db)


@app.route('/recipe/delete/<int:id>')
def delete(id):
    data = { 
    'id' : id
    }    
    Recipe.delete(data)
    print("deleting recipe")
    return redirect("/recipes")