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

    def test_edit_recipe(self):
        # Test editing an existing recipe
        recipe = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        self.recipe_book.add_recipe(recipe)
        
        # Save the recipe to file
        self.recipe_book.save_to_file(self.test_file)

        # Edit the recipe
        edited_recipe = RegularRecipe("Spaghetti Bolognese", ["pasta", "tomatoes", "meat"], ["boil", "fry", "serve"])
        self.recipe_book.edit_recipe("Spaghetti", edited_recipe)
        
        # Verify the recipe was edited
        self.assertEqual(self.recipe_book.recipes[0].name, "Spaghetti Bolognese")
        self.assertEqual(self.recipe_book.recipes[0].ingredients, ["pasta", "tomatoes", "meat"])

    def test_remove_recipe(self):
        # Test removing a recipe
        recipe = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        self.recipe_book.add_recipe(recipe)
        
        # Save the recipe to file
        self.recipe_book.save_to_file(self.test_file)
        
        # Remove the recipe
        self.recipe_book.remove_recipe("Spaghetti")
        
        # Verify the recipe was removed
        self.assertEqual(len(self.recipe_book.recipes), 0)

    def test_display_empty_recipe_list(self):
        # Test displaying when there are no recipes
        result = self.recipe_book.display_recipes()
        self.assertEqual(result, "No recipes found.")

    def test_empty_recipe_list(self):
        # Test if the recipe book handles no recipes correctly
        self.assertEqual(self.recipe_book.display_recipes(), "No recipes found.")

    def test_edit_non_existing_recipe(self):
        # Test if attempting to edit a non-existing recipe does not cause issues
        self.recipe_book.edit_recipe("NonExistentRecipe", RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"]))
        self.assertEqual(len(self.recipe_book.recipes), 0)

    def test_remove_non_existing_recipe(self):
        # Test if attempting to remove a non-existing recipe does not cause issues
        self.recipe_book.remove_recipe("NonExistentRecipe")
        self.assertEqual(len(self.recipe_book.recipes), 0)

    def test_add_duplicate_recipe(self):
        # Test adding a duplicate recipe
        recipe1 = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        self.recipe_book.add_recipe(recipe1)
    
        # Try to add the same recipe again
        recipe2 = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        self.recipe_book.add_recipe(recipe2)
    
        # Verify that the recipe list contains only one "Spaghetti" recipe
        self.assertEqual(len(self.recipe_book.recipes), 1)
    
    def test_multiple_recipes_in_file(self):
        # Add multiple recipes to the recipe book
        recipe1 = RegularRecipe("Spaghetti", ["pasta", "tomatoes"], ["boil", "drain", "serve"])
        recipe2 = RegularRecipe("Salad", ["lettuce", "tomatoes", "cucumber"], ["mix", "serve"])
    
        self.recipe_book.add_recipe(recipe1)
        self.recipe_book.add_recipe(recipe2)
    
        # Save to file
        self.recipe_book.save_to_file(self.test_file)
    
        # Load from file into a new RecipeBook instance
        new_recipe_book = RecipeBook()
        new_recipe_book.load_from_file(self.test_file)
    
        # Verify both recipes are loaded correctly
        self.assertEqual(len(new_recipe_book.recipes), 2)
        self.assertEqual(new_recipe_book.recipes[0].name, "Spaghetti")
        self.assertEqual(new_recipe_book.recipes[1].name, "Salad")
        
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

    def test_load_from_empty_file(self):
        # Create an empty file
        self.test_file.touch()
    
        # Load from the empty file
        self.recipe_book.load_from_file(self.test_file)
    
        # Verify that no recipes are loaded
        self.assertEqual(len(self.recipe_book.recipes), 0)
    
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