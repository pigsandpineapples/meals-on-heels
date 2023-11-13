from behave import *

@given('some ingredients and preparations have already been added')
def step_impl(context):
    context.existingIngredient = "Potatoes"
    context.existingPreparation = "Roasted"
    context.client.post("/add-ingredient", data={"newIngredient" : "Carrots"})
    context.client.post("/add-ingredient", data={"newIngredient" : "Spaghetti"})
    context.client.post("/add-ingredient", data={"newIngredient" : context.existingIngredient})
    context.client.post("/ingredient/1/add-preparation", data={"newPrep" : "Snarfed"})
    context.client.post("/ingredient/2/add-preparation", data={"newPrep" : "Snarfed"})
    context.client.post("/ingredient/2/add-preparation", data={"newPrep" : context.existingPreparation})
    context.client.post("/ingredient/3/add-preparation", data={"newPrep" : context.existingPreparation})

