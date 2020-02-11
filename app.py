import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGODB_NAME"] = os.environ.get("MONGODB_NAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/breakfast_recipes")
def breakfast_recipes():
    return render_template("breakfast_recipes.html",
    recipes=mongo.db.recipes.find())

@app.route("/main_recipes")
def main_recipes():
    return render_template("main_recipes.html",
    recipes=mongo.db.recipes.find())

@app.route("/dessert_recipes")
def dessert_recipes():
    return render_template("dessert_recipes.html",
    recipes=mongo.db.recipes.find())

@app.route("/add_recipes")
def add_recipes():
    return render_template("add_recipes.html",
    categories=mongo.db.categories.find())

@app.route("/edit_recipes")
def edit_recipes():
    return render_template("edit_recipes.html",
    recipes=mongo.db.recipes.find())

@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes

    form_data = request.form.to_dict()

    ingredients_list = form_data["ingredients"].split("\n")
    instructions_list = form_data["instructions"].split("\n")

    recipes.insert_one(
        {
        "category_name": form_data["category_name"],
        "recipe_name": form_data["recipe_name"],
        "image_link": form_data["image_link"],
        "ingredients": ingredients_list,
        "instructions": instructions_list
        }
    )

    return redirect(url_for("add_recipes"))

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
    port=int(os.environ.get("PORT")),
    debug=True)
