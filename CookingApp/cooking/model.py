from . import db
from sqlalchemy import CheckConstraint
import flask_login

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    recipes = db.relationship('Recipe', back_populates='user')
    ratings = db.relationship('Rating', back_populates='user')
    photos = db.relationship('Photo', back_populates='user')
    bookmarks = db.relationship('Bookmark', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')
    

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='recipes')

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)    
    n_people = db.Column(db.Integer, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    finished = db.Column(db.Boolean, nullable=False)

    ingredients = db.relationship('QuantifiedIngredient', back_populates='recipe')
    steps = db.relationship('Step', back_populates='recipe')
    ratings = db.relationship('Rating', back_populates='recipe')
    photos = db.relationship('Photo', back_populates='recipe')
    bookmarks = db.relationship('Bookmark', back_populates='recipe')
    comments = db.relationship('Comment', back_populates='recipe')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    quantified_ingredients = db.relationship('QuantifiedIngredient', back_populates='ingredient')

class QuantifiedIngredient(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    ingredient = db.relationship('Ingredient', back_populates='quantified_ingredients')

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='ingredients')

    quantity = db.Column(db.String(30), nullable=False)
    unit = db.Column(db.String(30), nullable=False)

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='steps')

    description = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='ratings')

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='ratings')

    value = db.Column(db.Integer, nullable=False) 
    __table_args__ = (
        CheckConstraint('value >= 0 AND value <= 5', name='check_rating_value'), 
    )

class Photo(db.Model):
    id  = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='photos')

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='photos')

    extension = db.Column(db.String(20), nullable=False)

class Bookmark(db.Model):
    id  = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='bookmarks')
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='bookmarks')

class Comment(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')
    
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    recipe = db.relationship('Recipe', back_populates='comments')


    