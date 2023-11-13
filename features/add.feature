Feature: adding and updating ingredients and preparations

Scenario: adding ingredients
Given I am an authorized user of the system
When I add a new ingredient
Then the ingredient should be added

Scenario: adding preparations
Given I am an authorized user of the system
And some ingredients and preparations have already been added
When I add a new preparation for an existing ingredient
Then the preparation should be added

Scenario: updating preparations
Given I am an authorized user of the system
And some ingredients and preparations have already been added
When I update an existing preparation for an existing ingredient
Then the preparation should be updated
