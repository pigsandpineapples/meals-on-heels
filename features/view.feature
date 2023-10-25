Feature: viewing ingredients and preparations

Scenario: view all ingredients
Given some ingredients and preparations have already been added
When I click to see all ingredients
Then I see a list of all the existing ingredients

Scenario: ingredient search
Given some ingredients and preparations have already been added
When I search for an existing ingredient 
Then I see a list of all existing preparations for that ingredient

Scenario: viewing a given preparation of a given ingredient
Given some ingredients and preparations have already been added
When I click an existing preparation of a given ingredient
Then I see the amount of ingredient used
And I see the number of people fed by that amount