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

        for table in schema:
            self.db_conn.cursor().execute(f'DROP TABLE IF EXISTS {table["name"]}')
            self.db_conn.cursor().execute(f'CREATE TABLE {table["name"]}({table["columns"]})')

    def add_ingredient(self, ingredient_name : str):
        with self.mutex:
            insert = "INSERT INTO Ingredients(name) VALUES (:ingredient)"
            self.db_conn.cursor().execute(insert, {"ingredient" : ingredient_name})
            self.db_conn.commit()
    
    def get_ingredient(self, ingredient_id : int):
        with self.mutex:
            select = "SELECT * FROM Ingredients WHERE id = (:ingredient_id)"
            return self.db_conn.cursor().execute(select, {"ingredient_id" : ingredient_id}).fetchone()
    
    def get_all_ingredients(self):
        with self.mutex:    
            return self.db_conn.cursor().execute("SELECT * FROM Ingredients")
    
    def update_preparation(self, prep_id : int, ingredient_amount, num_guests):
        with self.mutex:
            update = "UPDATE Preparations SET numGuests=:guests, ingredientAmount=:amt WHERE id=:id"
            self.db_conn.cursor().execute(update, {"id" : prep_id, "guests" : num_guests, "amt" : ingredient_amount})
            self.db_conn.commit()

    def add_preparation(self, ingredient_id : int, prep_name : str):
        with self.mutex:
            insert = "INSERT INTO Preparations(name, ingredientId) VALUES (:name, :id)"
            self.db_conn.cursor().execute(insert, {"name" : prep_name, "id" : ingredient_id})
            self.db_conn.commit()

    def get_preparation(self, prep_id : int):
        with self.mutex:
            select = "SELECT * FROM Preparations WHERE id = (:prep_id)"
            return self.db_conn.cursor().execute(select, {"prep_id" : prep_id}).fetchone()
        
    def get_preparations_of(self, ingredient_id : int):
        preparations = []

        with self.mutex:
            select = "SELECT * FROM Preparations WHERE ingredientId = (:id)"
            for row in self.db_conn.cursor().execute(select, {"id" : ingredient_id}):
                preparations.append((row[0], row[1]))

        return preparations
    