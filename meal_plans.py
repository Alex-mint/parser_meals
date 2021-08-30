import json
import os
import requests
from dotenv import load_dotenv


def load_meal_plans(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath) as json_file:
        meal_plans = json.load(json_file)
        return meal_plans


def parse_meal_plans(meal_plans):
    parsed_meal_plans = {}
    for number, day in enumerate(meal_plans['week'], 1):
        #print(f'Day {number} {day}')
        meals = meal_plans['week'][day]['meals']
        id = []
        for recipe in meals:
            #print(recipe['title'])
            id.append(recipe['id'])
            parsed_meal_plans[day] = id
        #print()
    return parsed_meal_plans


def get_recipe(api_key, reipe_id):
    url = f"https://api.spoonacular.com/recipes/{reipe_id}/information"
    params = {
        "apiKey": api_key,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    recipe = response.json()
    print_recipe(recipe)



def print_recipe(recipe):
    steps = recipe["analyzedInstructions"][0]["steps"]
    for ingredient in recipe["extendedIngredients"]:
        print(ingredient["originalString"])
    print()



if __name__ == '__main__':
    load_dotenv()
    api_key = os.environ['SPOON_API']
    filepath = 'mealplans/mealplans.json'
    meal_plans = load_meal_plans(filepath)
    parsed_meal_plans = parse_meal_plans(meal_plans)

    day = input('Какой день вас интересует?')
    for id in parsed_meal_plans[day]:
        recipe = get_recipe(api_key, id)