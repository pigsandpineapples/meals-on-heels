import sqlite3
from db import IngredientPrepDb
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
db = IngredientPrepDb(sqlite3.connect("mohdb", check_same_thread=False))

def reset_db(db_name : str):
    global db
    db = IngredientPrepDb(sqlite3.connect(db_name, check_same_thread=False))
    db.build_empty()

@app.route("/rebuild-database")
def rebuild_db():
    db.build_empty()
    return index()

@app.route("/")
def index():
    ingredient_list = []
    for ingredient_id, ingredient_name in db.get_all_ingredients():
        ingredient_list.append({"name" : ingredient_name, "href" : url_for('get_ingredient', ingredient_id=ingredient_id)})

    return render_template("index.html", ingredients=ingredient_list)

@app.route("/add-ingredient", methods = ['POST'])
@app.route("/add-ingredient/<ingredient>")
def add_ingredient(ingredient = None):
    if request.method == 'POST':
        db.add_ingredient(request.form['newIngredient'])
    else:
        db.add_ingredient(ingredient)
    return index()

@app.route("/ingredient/<ingredient_id>")
def get_ingredient(ingredient_id):
    ingredient = db.get_ingredient(ingredient_id)
    prep_list = []
    preps = db.get_preparations_of(ingredient_id)
    for prep_id, prep_name in preps:
        prep_list.append({"name" : prep_name, 
                          "href" : url_for('get_preparation', ingredient_id=ingredient_id, prep_id=prep_id)})

    return render_template("ingredient.html", 
                           ingredient={"id" : ingredient_id, "name" : ingredient[1]},
                           preparations=prep_list)

@app.route("/ingredient/<ingredient_id>/add-preparation", methods = ['POST'])
def add_preparation(ingredient_id):
    db.add_preparation(ingredient_id, request.form['newPrep'])
    return get_ingredient(ingredient_id)

@app.route("/ingredient/<ingredient_id>/update-preparation/<prep_id>/", methods= ['POST'])
def update_preparation(ingredient_id : int, prep_id : int):
    db.update_preparation(prep_id, request.form['ingredientAmount'], request.form['numGuests'])
    return get_ingredient(ingredient_id)

@app.route("/ingredient/<ingredient_id>/get-preparation/<prep_id>")
def get_preparation(ingredient_id : int, prep_id : int):
    ingredient = db.get_ingredient(ingredient_id)
    prep = db.get_preparation(prep_id)
    return render_template("preparation.html", ingredient={"id" : ingredient[0],
                                                           "name" : ingredient[1]},
                                               prep={"id" : prep[0],
                                                     "name" : prep[1],
                                                     "amount" : prep[5],
                                                     "guests" : prep[4]})