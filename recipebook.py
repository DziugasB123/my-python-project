import os
import getpass
from pathlib import Path
from abc import ABC, abstractmethod


# Abstract Recipe class (Abstraction)
class Recipe(ABC):
    def __init__(self, name, ingredients, steps):
        self._name = name
        self._ingredients = ingredients
        self._steps = steps

    @property
    def name(self):
        return self._name

    @property
    def ingredients(self):
        return self._ingredients

    @property
    def steps(self):
        return self._steps

    @abstractmethod
    def display(self):
        pass


# Concrete Recipe class (Inheritance)
class RegularRecipe(Recipe):
    def display(self):
        steps_formatted = "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(self.steps)])
        return f"\nRecipe: {self.name}\nIngredients: {', '.join(self.ingredients)}\nSteps:\n{steps_formatted}"


# RecipeBook class for managing recipes (Encapsulation)
class RecipeBook:
    def __init__(self):
        self.recipes = []

    def add_recipe(self, recipe):
        if any(r.name == recipe.name for r in self.recipes):
            print(f"Recipe '{recipe.name}' already exists.")
            return
        self.recipes.append(recipe)

    def remove_recipe(self, recipe_name):
        self.recipes = [r for r in self.recipes if r.name != recipe_name]

    def edit_recipe(self, old_recipe_name, new_recipe):
        for i, recipe in enumerate(self.recipes):
            if recipe.name == old_recipe_name:
                self.recipes[i] = new_recipe

    def display_recipes(self):
        if not self.recipes:
            return "No recipes found."
        return "\n".join([recipe.display() for recipe in self.recipes])

    def save_to_file(self, filepath):
        with open(filepath, "w") as file:
            for recipe in self.recipes:
                steps_combined = "//".join(recipe.steps)
                file.write(f"{recipe.name}|{','.join(recipe.ingredients)}|{steps_combined}\n")

    def load_from_file(self, filepath):
        self.recipes = []
        if not filepath.exists():
            return
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('|')
                if len(parts) == 3:
                    name, ingredients, steps_combined = parts
                    ingredients_list = ingredients.split(',')
                    steps_list = steps_combined.split('//') if steps_combined else []
                    recipe = RegularRecipe(name, ingredients_list, steps_list)
                    self.recipes.append(recipe)
                else:
                    print(f"Skipping invalid line: {line}")


# Account class (for account management)
class Account:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self.recipe_book = RecipeBook()
        self.base_path = Path.home() / "Documents" / "RecipeApp" / self._username
        self.account_file = self.base_path / "account.txt"
        self.recipes_file = self.base_path / "recipes.txt"

    def create_account(self):
        os.makedirs(self.base_path, exist_ok=True)
        with open(self.account_file, "w") as f:
            f.write(f"{self._username}\n{self._password}\n")
        print(f"Account for {self._username} created successfully!")

    def login(self):
        if not self.account_file.exists():
            print(f"No account found for {self._username}")
            return None
        with open(self.account_file, "r") as f:
            stored_username = f.readline().strip()
            stored_password = f.readline().strip()
            if stored_username == self._username and stored_password == self._password:
                print(f"Logged in as {self._username}")
                self.recipe_book.load_from_file(self.recipes_file)
                return self.recipe_book
            else:
                print("Incorrect username or password.")
                return None


# Decorator to log actions (Decorator Design Pattern)
def action_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Action logged: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


# RecipeApp class to manage user interaction
class RecipeApp:
    def __init__(self):
        self.user_account = None
        self.recipe_book = None

    def create_account(self, username, password):
        account_folder = Path.home() / "Documents" / "RecipeApp" / username
        if account_folder.exists():
            print("Account already exists. Please choose a different username.")
            return
        self.user_account = Account(username, password)
        self.user_account.create_account()
        self.recipe_book = self.user_account.recipe_book

    def login(self, username, password):
        self.user_account = Account(username, password)
        self.recipe_book = self.user_account.login()
        if self.recipe_book is None:
            self.user_account = None

    @action_logger
    def add_recipe(self, name, ingredients, steps):
        recipe = RegularRecipe(name, ingredients, steps)
        self.recipe_book.add_recipe(recipe)
        self.recipe_book.save_to_file(self.user_account.recipes_file)
        print(f"Recipe {name} added.")

    @action_logger
    def remove_recipe(self, recipe_name):
        self.recipe_book.remove_recipe(recipe_name)
        self.recipe_book.save_to_file(self.user_account.recipes_file)
        print(f"Recipe {recipe_name} removed.")

    @action_logger
    def edit_recipe(self, old_recipe_name, name, ingredients, steps):
        recipe = RegularRecipe(name, ingredients, steps)
        self.recipe_book.edit_recipe(old_recipe_name, recipe)
        self.recipe_book.save_to_file(self.user_account.recipes_file)
        print(f"Recipe {old_recipe_name} edited.")

    def display_all_recipes(self):
        print(self.recipe_book.display_recipes())



if __name__ == "__main__":
    app = RecipeApp()

    base_folder = Path.home() / "Documents" / "RecipeApp"
    os.makedirs(base_folder, exist_ok=True)

    existing_accounts = [folder.name for folder in base_folder.iterdir()
                         if folder.is_dir()]

    # Login menu
    while True:
        print("\n=== Welcome to RecipeApp ===")
        print("[1] Login")
        print("[2] Create New Account")
        print("[3] Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            existing_accounts = [folder.name for folder in base_folder.iterdir()
                                 if folder.is_dir()]
            if not existing_accounts:
                print("No accounts exist yet. Please create an account first.\n")
                continue

            login_attempts = 0
            while login_attempts < 3:
                login_username = input("Login - Enter username: ")
                login_password = getpass.getpass("Login - Enter password: ")
                app.login(login_username, login_password)
                if app.recipe_book:
                    break
                else:
                    login_attempts += 1
                    print(f"Login failed. Attempts left: {3 - login_attempts}\n")
            
            if not app.recipe_book:
                print("Too many failed login attempts. Exiting...")
                exit()

            break  # Successful login, move on to the main app

        elif choice == "2":
            username = input("Create account - Enter username: ")
            password = getpass.getpass("Create account - Enter password: ")
            account_folder = base_folder / username
            if account_folder.exists():
                print("Account already exists. Please choose a different username.\n")
                continue  # Don't proceed if folder exists
            app.create_account(username, password)
            existing_accounts = [folder.name for folder in base_folder.iterdir()
                                 if folder.is_dir()]

        elif choice == "3":
            print("Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select 1, 2, or 3.")

    # Main menu
    while True:
        print("\nOptions:")
        print("1. Add Recipe")
        print("2. Edit Recipe")
        print("3. Remove Recipe")
        print("4. Display All Recipes")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            name = input("Enter recipe name: ")
            ingredients = input("Enter ingredients (comma-separated): ").split(',')
            ingredients = [ingredient.strip() for ingredient in ingredients]
            print("Enter steps one by one. Type 'done' when finished:")
            steps = []
            while True:
                step = input(f"Step {len(steps)+1}: ")
                if step.lower() == 'done':
                    break
                steps.append(step)
            app.add_recipe(name, ingredients, steps)

        elif choice == "2":
            old_name = input("Enter the name of the recipe you want to edit: ")
            name = input("Enter new recipe name: ")
            ingredients = input("Enter new ingredients (comma-separated): ").split(',')
            ingredients = [ingredient.strip() for ingredient in ingredients]
            print("Enter new steps one by one. Type 'done' when finished:")
            steps = []
            while True:
                step = input(f"Step {len(steps)+1}: ")
                if step.lower() == 'done':
                    break
                steps.append(step)
            app.edit_recipe(old_name, name, ingredients, steps)

        elif choice == "3":
            name = input("Enter the name of the recipe you want to remove: ")
            app.remove_recipe(name)

        elif choice == "4":
            app.display_all_recipes()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please select from 1 to 5.")