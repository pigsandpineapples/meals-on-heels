from bs4 import BeautifulSoup
from behave import *

@given('I am an authorized user of the system')
def step_impl(context):
    # TODO: need to figure out if/how to authorize users
    pass

@when('I add a new ingredient')
def step_impl(context):
    context.newIngredient = "Cauliflower"
    context.client.post("/add-ingredient", data={"newIngredient" : context.newIngredient})

@when('I add a new preparation for an existing ingredient')
def step_impl(context):
    pass

@when('I update an existing preparation for an existing ingredient')
def step_impl(context):
    pass

@then('the ingredient should be added')
def step_impl(context):
    page = context.client.get("/")
    tags = BeautifulSoup(page.get_data(as_text=True), 'html.parser')
    ingredientDropdown = tags.find(id='myDropdown')
    assert(ingredientDropdown.find(string=context.newIngredient))

@then('the preparation should be added')
def step_impl(context):
    pass

@then('the preparation should be updated')
def step_impl(context):
    pass
