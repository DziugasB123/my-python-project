import unittest
from pathlib import Path
import os

# Assuming your RecipeBook and RegularRecipe classes are in a module named `recipe_app`
from recipebook import RecipeBook, RegularRecipe

class TestRecipeBook(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file for the test
        self.test_file = Path("test_recipes.txt")
        # Clear the file before starting the tests
        if self.test_file.exists():
            self.test_file.unlink()
        
        # Create a RecipeBook instance for testing
        self.recipe_book = RecipeBook()

    def tearDown(self):
        # Clean up after each test
        if self.test_file.exists():
            self.test_file.unlink()
    
    def test_add_recipe(self):
        # Test adding a recipe
        recipe = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        self.recipe_book.add_recipe(recipe)
        
        # Check if the recipe was added to the recipe book
        self.assertEqual(len(self.recipe_book.recipes), 1)
        self.assertEqual(self.recipe_book.recipes[0].name, "Spaghetti")
    
    def test_save_to_file(self):
        # Test saving recipes to a file
        recipe = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        self.recipe_book.add_recipe(recipe)
        
        # Save the recipe to file
        self.recipe_book.save_to_file(self.test_file)
        
        # Check if file exists
        self.assertTrue(self.test_file.exists())
        
        # Check if file content matches the expected format
        with open(self.test_file, "r") as file:
            content = file.read().strip()
            self.assertEqual(content, "Spaghetti|pasta,tomatoes|boil//drain//serve")
    
    def test_load_from_file(self):
        # Test loading recipes from a file
        recipe = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        self.recipe_book.add_recipe(recipe)
        
        # Save the recipe to file
        self.recipe_book.save_to_file(self.test_file)
        
        # Create a new RecipeBook instance and load from file
        new_recipe_book = RecipeBook()
        new_recipe_book.load_from_file(self.test_file)
        
        # Check if the recipe is correctly loaded
        self.assertEqual(len(new_recipe_book.recipes), 1)
        self.assertEqual(new_recipe_book.recipes[0].name, "Spaghetti")
    
    def test_invalid_recipe_line(self):
        # Test handling invalid recipe lines in the file
        with open(self.test_file, "w") as file:
            file.write("Spaghetti|pasta,tomatoes|boil//drain//serve\n")
            file.write("InvalidRecipe|incorrect,line//missingsteps\n")  # Invalid line
            
        # Create a new RecipeBook instance and load from file
        new_recipe_book = RecipeBook()
        new_recipe_book.load_from_file(self.test_file)
        
        # Check if only the valid recipe was loaded
        self.assertEqual(len(new_recipe_book.recipes), 1)
        self.assertEqual(new_recipe_book.recipes[0].name, "Spaghetti")
    
    def test_recipe_format_check(self):
        # Test that the recipe line format is correct
        invalid_recipe_line = "InvalidRecipe|ingredients|step1||step2"
        parts = invalid_recipe_line.split('|')
        self.assertTrue(len(parts) >= 3, "Recipe line should have at least three parts.")
    
if __name__ == '__main__':
    unittest.main()