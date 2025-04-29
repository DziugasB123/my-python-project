1. Introduction
    This programs purpose is to allow users to create various recipes, which you can then view, edit or delete anytime. It also has an account system, meaning multiple people can have their own recipe "books".

    To run the program, you will need some sort of coding software, like VS Code or Google Colab to run the code, as it does not have it's own launcher.

    Once launched, the program first let's the user choose from three options: create an account, login or exit. You may only login if there is at least one existing account. All you need is to input 1, 2 or 3 for the corresponding choice.
    When logging or creating an account and prompted to enter the password, it will not be visible - the field will appear empty no matter what you input. So it is best to enter the password carefully, especially since the program will close itself if login is failed three times.
    Once logged in, the program now provides five choices: add a recipe, edit a recipe, remove a recipe, display all recipes in account or exit. Again, all you need to do is input the corresponding number from 1 to 5 to make a choice.
    When creating a recipe, you will first be promted to give a name, then input the ingredient list, and lastly input the cooking steps one by one.
    Editing a recipe is the same as creating a new recipe, but it replaces the chosen recipe to edit.

    The program stores all data in Users/"username"/Documents/RecipeApp.
    There you can find all account info and saved recipes. It is best not to edit, delete or add any external files, or the program may break. To delete all data, simply delete the "RecipeApp" folder.
    
2. Examples of requirements

    Example of Polymorphism, Abstraction and Inherritance

        There is an abstract class called "Recipe", in which there is an abstract method "display":

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
        
        The class "RegularRecipe" inherits from the abstract "Recipe class, and in this class the "display" method is overriden by a method of the same name.

            class RegularRecipe(Recipe):
                def display(self):
                    steps_formatted = "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(self.steps)])
                    return f"\nRecipe: {self.name}\nIngredients: {', '.join(self.ingredients)}\nSteps:\n{steps_formatted}"
         

    Examples of Encapsulation

        In the abstract class "Recipe", the attributes are marked as "protected" by using a single underscore before the name:

            class Recipe(ABC):
                def __init__(self, name, ingredients, steps):
                    self._name = name
                    self._ingredients = ingredients
                    self._steps = steps
        
        In the class "RecipeBook", there is a recipes list, which even though is not protected or private, it is only accessed through the class methods:

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

                ...

        The class "Account" has the "username" and "password" attributes as "protected", same as in the "Recipe" class:

            def __init__(self, username, password):
                self._username = username
                self._password = password
                self.recipe_book = RecipeBook()
                self.base_path = Path.home() / "Documents" / "RecipeApp" / self._username
                self.account_file = self.base_path / "account.txt"
                self.recipes_file = self.base_path / "recipes.txt"


    Example of Composition

        The "Account" class, instead of inheriting from, has an instance of "RecipeBook" class:
            
            class Account:
                def __init__(self, username, password):
                    self._username = username
                    self._password = password
                    self.recipe_book = RecipeBook()
                    self.base_path = Path.home() / "Documents" / "RecipeApp" / self._username
                    self.account_file = self.base_path / "account.txt"
                    self.recipes_file = self.base_path / "recipes.txt"


    Example of a Design Pattern

        The "action_logger" method "wraps around" other method in "RecipeApp" class to log what actions were made:

            def action_logger(func):
                def wrapper(*args, **kwargs):
                    print(f"Action logged: {func.__name__}")
                    return func(*args, **kwargs)
                return wrapper

            class RecipeApp:
                @action_logger
                def add_recipe(self, name, ingredients, steps):
                ...

                @action_logger
                def remove_recipe(self, recipe_name):
                ...

                @action_logger
                def edit_recipe(self, old_recipe_name, name, ingredients, steps):
                ...

3. Implementation

    First, there is the abstract class "Recipe", which defines the blueprint of a recipe and from which "RegularRecipe" class inherits for the "display" method, which formats and displays recipe from read file.

    The "RecipeBook" class manages a list of recipes, has methods for actions with recipes, as well as for saving to and loading from file. The recipes are saved to file with "|" as a seperator in the format RecipeName|Ingreient1,Ingredient2,...|Setp1//Step2//Step3... The recipes are loaded once a file is opened with valid lines.
    It also encapsulates the recipe management functions.

    The "Account" class is there to manage account creation and logging in, stores the users username, password and "recipe book". The "create_account" method creates an account with the user inputs, also checking if it's not a duplicate account. "login" method checks the user inputs and comapres them to other account information. Once a match is found, it opens the account "recipe book" and prepares it for actions.

    The "action_logger" decorator logs the actions that happen (such as adding or removing recipes).

    "if __name__ == "__main__":" provides a console menu for the user inputs.


4. Results and Summary

    Results:
        1. User account creation and login;
        2. Recipe management;
        3. Persistent storage;
        4. Action logging;
        5. There were a few times, when the program wouldn't work because of tiny mistakes that were hard to catch.
    
    Conclusion:
        This program successfully manages recipe creation, deletion or editing, user accounts. It records data in .txt files to preserve information. This was the largest programming project I have ever done, which was interesting to work on, but I do not believe I will be in any way improving or adding to this program, nor in any way sharing it with other people - it was solely a project for the course work assignment.