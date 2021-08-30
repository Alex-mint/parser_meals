import json
import os
import pathlib

import requests
from dotenv import load_dotenv


def generate_meal_plan(api_key):
    url = f'https://api.spoonacular.com/mealplanner/generate'
    params = {
        'apiKey': api_key,
        'timeFrame': 'week',
        'targetCalories': 2000,
        'diet': 'vegan'
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    meal_plan = response.json()
    return meal_plan


def save_meal_plans(filepath, meal_plan):
    with open(filepath, 'w') as file:
        json.dump(meal_plan, file)


if __name__ == '__main__':
    load_dotenv()
    filename = 'mealplans.json'
    folder = 'mealplans'
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(folder, f'{filename}')

    hash = os.environ['SPOON_HASH']
    login = os.environ['SPOON_LOGIN']
    api_key = os.environ['SPOON_API']
    meal_plan = generate_meal_plan(api_key)
    save_meal_plans(filepath, meal_plan)