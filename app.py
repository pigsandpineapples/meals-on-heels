import sqlite3
from db import IngredientPrepDb
from flask import Flask, render_template, request, url_for


db = IngredientPrepDb(sqlite3.connect("mohdb", check_same_thread=False))
app = Flask(__name__)

@app.route("/rebuild-database")
def rebuild_db():
    db.build_empty()
    return index()

@app.route("/")
def index():
    ingredientList = []
    for ingredient in db.get_all_ingredients():
        ingredientList.append({"name" : ingredient, "href" : url_for('get_ingredient', ingredient=ingredient)})

    return render_template("index.html", ingredients=ingredientList)

@app.route("/add-ingredient", methods = ['POST'])
@app.route("/add-ingredient/<ingredient>")
def add_ingredient(ingredient = None):
    if request.method == 'POST':
        print(f'add_ingredient(POST={request.form['newIngredient']})')
        db.add_ingredient(request.form['newIngredient'])
    else:
        print(f'add_ingredient(ingredient={ingredient})')
        db.add_ingredient(ingredient)
    return index()

@app.route("/get-ingredient/<ingredient>")
def get_ingredient(ingredient):
    return ingredient
