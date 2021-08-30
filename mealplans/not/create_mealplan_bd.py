import os
import requests
import re
import json

from dotenv import load_dotenv
from parser_meals.meal_plans import load_meal_plans


def parse_meal_plans(meal_plans):
    parsed_meal_plans = {}
    for number, day in enumerate(meal_plans['week'], 1):
        meals = meal_plans['week'][day]['meals']
        id = []
        for recipe in meals:
            id.append(recipe['id'])
            parsed_meal_plans[day] = id
    return parsed_meal_plans


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def create_bd(filepath):
    week_days = ["понедельник", "вторник", "среда",
                 "четверг", "пятница", "суббота", "воскресенье"]
    week_meal_plan = load_meal_plans(filepath)
    week_meal_plan = parse_meal_plans(week_meal_plan)
    daily_recipes = {}
    for number, day in enumerate(week_meal_plan):
        daily_recipes[week_days[number]] = get_daily_recipes(week_meal_plan[day])
        get_daily_recipes(week_meal_plan[day])
        with open(f'mealplans/{week_days[number]}.json', 'w') as file:
            json.dump(get_daily_recipes(week_meal_plan[day]), file)


def get_daily_recipes(daily_recipes_id):
    recipes = []
    for number, recipe in enumerate(daily_recipes_id):
        recipe_id = daily_recipes_id[number]
        recipe = get_recipe(api_key, recipe_id)
        recipes.append(recipe)
    return recipes


def get_recipe(api_key, resipe_id):
     url = f"https://api.spoonacular.com/recipes/{resipe_id}/information"
     params = {
         "apiKey": api_key,
     }
     response = requests.get(url, params=params)
     response.raise_for_status()
     recipe = response.json()
     resipe = parser_recipe(recipe)
     return resipe


def parser_recipe(recipe):
    parsered_resipe = {}
    parsered_resipe["title"] = recipe["title"]
    parsered_resipe["summary"] = clean_html(recipe["summary"])
    steps = recipe["analyzedInstructions"][0]["steps"]
    for step in steps:
        parsered_resipe["steps"] = [f"{step['number']}. {step['step']}" for step in steps]
    parsered_resipe["extendedIngredients"] = [ingredient["originalString"] for ingredient in recipe["extendedIngredients"]]
    parsered_resipe["pricePerServing"] = recipe["pricePerServing"]
    return parsered_resipe


if __name__ == '__main__':
    load_dotenv()
    api_key = os.environ['SPOON_API']
    filepath = '../mealplans.json'
    create_bd(filepath)
