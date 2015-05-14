"""Program that help you to decide what to eat for the week
   You should start adding some Recipies and ingredience you need
   for the Recipie. If you have at least 7 of them they will be
   used to tell you what you could cook and give you a grocery list

   Keywords are add_recipe and get_meals
"""
import sys
import getopt
import json
import glob
import random


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    """Takes the Keywords add_recipe and get_meals and
    calles the underlying functions.
    """
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hamg", ["help", "add"
                                                          "get"])

        except getopt.error as msg:
            raise Usage(msg)

        for o, args in opts:
            print(args)
            if o in ("-h", "--help"):
                print('''Valid options ase -a to add a recipe and -m
                      to get meals and -g to get meals and grocerielist
                      ''')
                return 1
            elif o in ("-a"):
                save_recipe(add_recipe())
            elif o in ("-m"):
                recipes = get_recipes()
                weekly_meals = return_shuffled_max_seven(recipes)
                print_meals(weekly_meals)
            elif o in ("-g"):
                recipes = get_recipes()
                weekly_meals = return_shuffled_max_seven(recipes)
                print_meals(weekly_meals)
                print_grocerylist(weekly_meals)
            else:
                raise Usage("No valid option")

    except Usage as err:
        print(sys.stderr, err.msg)
        print(sys.stderr, "for help use --help")
        return 2


def add_recipe():
    """ Asks the user interactivly to input a recipe name
    and the ingredience

    Returns
    -------
        A dictionary with the recipe name and the list of ingedience

        Example
        -------
            {'Applepie':['Apple','Pie']}
    """
    print("Name of the recipe\n")
    name = input("> ")
    recipe = []
    while True:
        print("Add an ingredience or finalize the recipe with 'q'")
        ingredience = input("> ")
        if ingredience == 'q':
            break
        else:
            recipe.append(ingredience)
    return {name: recipe}


def save_recipe(recipe):
    """Saves the recipe to a json file"""

    # Get the first key from the dictionary: Name of the recipe
    name = next(iter(recipe.keys()))
    with open(name+'.recipe', 'w') as f:
        json.dump(recipe, f, indent=1)


def get_recipes():
    """Gets all recipes and returns them as one list"""
    grand_list_of_recipes = []
    for recipe in glob.glob("*.recipe"):
        with open(recipe, 'r') as f:
            grand_list_of_recipes.append(json.load(f))
    return grand_list_of_recipes


def return_shuffled_max_seven(a_list):
    """ Returns 7 items from a list"""
    b_list = list(a_list)
    random.shuffle(b_list)
    return b_list[:7]


def print_meals(weekly_meals):
    """Prints a weekplan for meals"""
    week = []
    for meal in weekly_meals:
        name = next(iter(meal.keys()))
        week.append(name)
    if len(week) < 7:
        print("You only have "+str(len(week))+" recipes")
        for i in range(7-len(week)):
            week.append('')

    days = ['Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
            ]

    for days, meal in zip(days, week):
        print('{0}:\n    {1}'.format(days, meal))


def print_grocerylist(weekly_meals):
    """Prints the grocersylist"""
    meals = []
    for meal in weekly_meals:
        name = next(iter(meal.keys()))
        meals.append(name)

    recipe_list = []
    for idx, meal in enumerate(meals):
        recipe_list.append(weekly_meals[idx][meal])

    grocery_list = []
    for sublists in recipe_list:
        grocery_list += sublists

    print("Grocery List:\n")
    grocery_list = list(set(grocery_list))
    for item in grocery_list:
        print("    * "+item+"\n")


if __name__ == '__main__':
    sys.exit(main())
