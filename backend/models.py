from datetime import datetime

class Recipe:
    def __init__(self, title, image, ingredients, instructions, sourceURL, recipeId):
        self.title = title
        self.image = image
        self.ingredients = ingredients
        self.instructions = instructions
        self.sourceURL = sourceURL
        self.recipeId = recipeId

    def save(self, db):
        if db is None:
            raise ValueError("Database connection failed")
        collection = db['recipes']
        recipe_data = {
            "title": self.title,
            "image": self.image,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "sourceURL": self.sourceURL,
            "recipeId": self.recipeId,
            "createdAt": datetime.now()
        }
        result = collection.insert_one(recipe_data)
        return result.inserted_id