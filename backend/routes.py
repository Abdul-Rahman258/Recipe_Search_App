from flask import Flask, request, jsonify
import requests
import os
from config import get_db
from models import Recipe

app = Flask(__name__)

SPOONACULAR_API_KEY = os.environ.get("SPOONACULAR_API_KEY")
if not SPOONACULAR_API_KEY:
    raise ValueError("SPOONACULAR_API_KEY not set")

@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    try:
        url = f'https://api.spoonacular.com/recipes/complexSearch?apiKey={SPOONACULAR_API_KEY}&query={query}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save/<recipe_id>', methods=['POST'])
def save_recipe(recipe_id):
    try:
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOONACULAR_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        recipe_data = response.json()

        new_recipe = Recipe(
            title=recipe_data['title'],
            image=recipe_data.get('image', ''),
            ingredients=recipe_data.get('extendedIngredients', []),
            instructions=recipe_data.get('instructions', ''),
            sourceURL=recipe_data.get('sourceUrl', ''),
            recipeId=recipe_id
        )

        db = get_db()
        inserted_id = new_recipe.save(db)
        return jsonify({'message': 'Recipe saved successfully', 'id': str(inserted_id)}), 201
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except ValueError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/saved', methods=['GET'])
def get_saved_recipes():
    db = get_db()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    recipes = list(db['recipes'].find({}))
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])
    return jsonify(recipes)

@app.route('/delete/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    db = get_db()
    if db is None:
        return jsonify({'error': 'Database connection failed'}), 500
    result = db['recipes'].delete_one({'recipeId': recipe_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Recipe deleted successfully'}), 200
    else:
        return jsonify({'error': 'Recipe not found'}), 404