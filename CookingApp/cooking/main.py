import datetime
import dateutil.tz


from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, current_app


from . import model, db

import flask_login
from flask_login import current_user
import pathlib

from datetime import datetime


# Import the func module from SQLAlchemy for SQL functions, in
# this case for using random()
from sqlalchemy import func, and_

from sqlalchemy.orm import joinedload

bp = Blueprint("main", __name__)


@bp.route('/search')
def search():
    ingredient = request.args.get('ingredient')

    query = (
        db.session.query(model.Recipe)
        .join(model.QuantifiedIngredient, model.Recipe.id == model.QuantifiedIngredient.recipe_id)
        .join(model.Ingredient, model.QuantifiedIngredient.ingredient_id == model.Ingredient.id)
        .filter(model.Ingredient.name.ilike(f"%{ingredient}%"))
        .options(joinedload(model.Recipe.ingredients))
        .all()
    )

    return render_template('main/search_results.html', ingredient=ingredient, results=query)


# A controller for the main view of our website, in which we are displaying 70
# complete (with ingredients and steps) random recipes from the database
@bp.route('/')
def index():
    # Building the query to get 70 finished random recipes (finished should be equals True),
    # using order_by, func.random() and limit(70)(for only getting 70 recipes)
    query = (db.select(model.Recipe).where(and_(model.Recipe.finished == True)).order_by(func.random()).limit(70))

    # Execute the query and get all the results
    recipes = db.session.execute(query).scalars().all()

    ingredients = db.session.execute(db.select(model.Ingredient)).scalars().all()

    return render_template("main/index.html", recipes = recipes, ingredients=ingredients)


@bp.route('/my_profile/<int:user_id>')
@flask_login.login_required
def my_profile(user_id):
    current_user = flask_login.current_user
    
    # Check if the user_id in the URL matches the id of the current user
    if current_user.id == user_id:
        return render_template('main/my_profile.html', user=current_user, on_my_profile=True)
    

# A controller for the user view of our website
@bp.route('/user/<int:user_id>')
def user(user_id):

    # Get the user with the corresponding user_id from the database
    user = db.session.get(model.User, user_id)

    # We check if the user exists
    if not user:
        # If the user does not exist, we return a 404 error response
        abort(404, f"User id {user_id} doesn't exist.")

    all_users = model.User.query.all()

    # If the user is the current user, it will render the my_profile.html template
    # in which the finished and unfinished recipes can be seen
    if current_user.is_authenticated and current_user.id == user.id:
        #return render_template('main/my_profile.html', user=user)
        return redirect(url_for("main.my_profile", user_id=user.id))
    else:   
        # If the user exists, we render the user_view template with the user data
        return render_template('main/user_view.html', user=user, on_my_profile=False, all_users=all_users)


@bp.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id):
    user = flask_login.current_user

    # Get the recipe with the corresponding recipe_id from the database
    recipe = db.session.get(model.Recipe, recipe_id)

    # We check if the recipe exists
    if not recipe:
        # If the recipe does not exist, we return a 404 error response
        abort(404, f"Recipe id {recipe_id} doesn't exist.")

    # Calculate the average rating for the recipe
    avg_rating = db.session.query(func.avg(model.Rating.value)).filter_by(recipe_id=recipe_id).scalar()
    if avg_rating is not None:
        avg_rating = round(avg_rating, 1)
    # BOOKMARKS
    if current_user.is_authenticated:
        user_id = current_user.id
        existing_bookmark = model.Bookmark.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    else:
        existing_bookmark = None

    bookmarked = existing_bookmark is not None

    if request.method == "POST":
        if existing_bookmark:
            bookmarked = False
        else:
            bookmarked = True

    return render_template('main/recipe_view.html', recipe=recipe, avg_rating = avg_rating, bookmarked=bookmarked)


@bp.route('/bookmarks/<int:recipe_id>', methods=['POST'])
@flask_login.login_required
def bookmarks(recipe_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        existing_bookmark = model.Bookmark.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    else:
        existing_bookmark = None

    bookmarked = existing_bookmark is not None

    if request.method == "POST":
        if existing_bookmark:
            db.session.delete(existing_bookmark)
            bookmarked = False
        else:
            db.session.add(model.Bookmark(user_id=user_id, recipe_id=recipe_id))
            bookmarked = True

        db.session.commit()

    return redirect(url_for('main.recipe', recipe_id=recipe_id, bookmarked=bookmarked))


@bp.route("/creating_recipe", methods=["GET", "POST"])
@flask_login.login_required
def creating_recipe(): 
    user = current_user.id

    if request.method == "POST":
        # Retrieve the form data from the request
        title = request.form.get("title")
        description = request.form.get("description")
        number_people = request.form.get("number_people")
        cooking_time = request.form.get("cooking_time")

        created_recipe = model.Recipe(user_id = user, title = title, description = description, n_people = number_people, cooking_time = cooking_time, finished = False)
        db.session.add(created_recipe)
        db.session.commit()
        
        return redirect(url_for('main.finishing_recipe', recipe_id = created_recipe.id))


    unfinished_recipes = model.Recipe.query.filter_by(user_id=user, finished=False).all()

    return render_template("main/creating_recipe.html", unfinished_recipes=unfinished_recipes)


@bp.route("/finishing_recipe/<int:recipe_id>", methods=["GET", "POST"])
@flask_login.login_required
def finishing_recipe(recipe_id):
    if request.method=="GET":
        selected_recipe = model.Recipe.query.get(recipe_id)
        ingredients = db.session.execute(db.select(model.Ingredient)).scalars().all()
        return render_template("main/finishing_recipe.html", selected_recipe=selected_recipe, ingredients=ingredients)

    if request.method == "POST":

        ingredient_names = request.form.getlist('ingredientName[]')
        quantities = request.form.getlist('quantity[]')
        units = request.form.getlist('unit[]')

        for ingredient_name, quantity, unit in zip(ingredient_names, quantities, units):
            existing_ingredient = model.Ingredient.query.filter_by(name=ingredient_name).first()
            if existing_ingredient:
                # If the ingredient already exists, reuse it
                ingredient_id = existing_ingredient.id
            else:
                # If the ingredient doesn't exist, add it to the database
                new_ingredient = model.Ingredient(name=ingredient_name)
                db.session.add(new_ingredient)
                db.session.commit()

                # Retrieve the ID of the newly added ingredient
                ingredient_id = new_ingredient.id


            quantified_ingredient = model.QuantifiedIngredient(
                recipe_id=recipe_id,
                ingredient_id=ingredient_id,
                quantity=quantity,
                unit=unit
            )
            db.session.add(quantified_ingredient)
            db.session.commit()

        steps = request.form.getlist("stepDescription[]")
        for order, step in enumerate(steps):
            new_step = model.Step(recipe_id = recipe_id,
            description = step,
            order = order + 1
            )
            db.session.add(new_step)
            db.session.commit()

        selected_recipe = model.Recipe.query.get(recipe_id)
        selected_recipe.finished = True
        db.session.commit()

       
        return redirect(url_for('main.recipe', recipe_id = selected_recipe.id))


@bp.route('/upload_photo', methods=['POST'])
@flask_login.login_required
def upload_photo():
    uploaded_file = request.files['photo']
    if uploaded_file.filename != '':
        content_type = uploaded_file.content_type
        if content_type == "image/png":
            extension = "png"
        elif content_type == "image/jpeg":
            extension = "jpg"
        else:
            abort(400, f"Unsupported file type {content_type}")

        # Assuming you have a way to get the current recipe (replace with your logic)
        recipe_id = request.form['recipe_id']
        recipe = model.Recipe.query.get_or_404(recipe_id)

        photo = model.Photo(
            user=flask_login.current_user,
            recipe=recipe,
            extension=extension
        )
        db.session.add(photo)
        db.session.commit()

        path = (
            pathlib.Path(current_app.root_path)
            / "static"
            / "photos"
            / f"photo-{photo.id}.{extension}"
        )
        uploaded_file.save(path)
        return redirect(url_for('main.recipe', recipe_id=recipe.id))
    else:
        flash('No file selected')
        return redirect(url_for('main.recipe', recipe_id=recipe.id))


@bp.route('/ratings/<int:recipe_id>', methods=["GET",'POST'])
@flask_login.login_required
def ratings(recipe_id):
    if request.method == "POST":
        rating_value = int(request.form['rating'])
        if 1 <= rating_value <= 5:
            user_id = flask_login.current_user.id
            rating = model.Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

            if rating:
                rating.value = rating_value
            else:
                rating = model.Rating(user_id=user_id, recipe_id=recipe_id, value=rating_value)
                db.session.add(rating)

            db.session.commit()

    return redirect(url_for('main.recipe', recipe_id=recipe_id))

@bp.route('/comments/<int:recipe_id>', methods=['POST'])
@flask_login.login_required
def comments(recipe_id):
    description = request.form['description']
    user_id = flask_login.current_user.id
    
    if description:
        timestamp = datetime.utcnow()
        comment = model.Comment(user_id=user_id, recipe_id=recipe_id, description=description, timestamp=timestamp)
        db.session.add(comment)
        db.session.commit()

    return redirect(url_for('main.recipe', recipe_id=recipe_id))


