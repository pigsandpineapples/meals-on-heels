import sqlite3
from threading import Lock

class IngredientPrepDb:
    def __init__(self, db_conn : sqlite3.Connection = None):
        self.mutex = Lock()
        if db_conn == None:
            db_conn = sqlite3.connect(":memory:")

        self.db_conn = db_conn
    
    def __del__(self):
        self.db_conn.close()

    def build_empty(self):
        schema = [{"name" : 'Ingredients',
                   "columns" : 'id INTEGER PRIMARY KEY ASC, name'},
                  {"name" : 'Preparations',
                   "columns" : 'id INTEGER PRIMARY KEY ASC, name, ingredientId, dateOfPrep, numGuests, ingredientAmount'}]

        existingTables = []
        for table in self.db_conn.cursor().execute("SELECT name FROM sqlite_master"):
            existingTables.append(table[0])

        for table in schema:
            if table["name"] in existingTables:
                self.db_conn.cursor().execute(f'DROP TABLE {table["name"]}')
            self.db_conn.cursor().execute(f'CREATE TABLE {table["name"]}({table["columns"]})')

    def add_ingredient(self, ingredient_name : str):
        with self.mutex:
            self.db_conn.cursor().execute("INSERT INTO Ingredients(name) VALUES (:ingredient)", {"ingredient" : ingredient_name })
            self.db_conn.commit()
    
    def get_all_ingredients(self):
        with self.mutex:
            ingredients = []
            for row in self.db_conn.cursor().execute("SELECT name FROM Ingredients"):
                ingredients.append(row[0])

            return ingredients

