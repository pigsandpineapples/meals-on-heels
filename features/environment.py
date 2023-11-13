from app import app, reset_db

def before_all(context):
    app.testing = True

def before_scenario(context, scenario):
    context.client = app.test_client()
    reset_db(":memory:")