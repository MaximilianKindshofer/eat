"""Program that help you to decide what to eat for the week
   You should start adding some Recipies and ingredience you need
   for the Recipie. If you have at least 7 of them they will be
   used to tell you what you could cook and give you a grocery list
   
   Keywords are add_recepie and get_meals
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
    """Takes the Keywords add_recepie and get_meals and
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
                print('''Valid options ase -a to add a recepie and -m
                      to get meals and -g to get meals and grocerielist
                      ''')
                return 1
            elif o in ("-a"):
                save_recepie(add_recepie())
            elif o in ("-m"):
                recepies = get_recepies()
                weekly_meals = return_shuffled_max_seven(recepies)
                print_meals(weekly_meals)
            elif o in ("-g"):
                recepies = get_recepies()
                weekly_meals = return_shuffled_max_seven(recepies)
                print_meals(weekly_meals)
                print_grocerylist(weekly_meals)
            else:
                raise Usage("No valid option")
        
                
    except Usage as err:
        print(sys.stderr, err.msg)
        print(sys.stderr, "for help use --help")
        return 2
        
def add_recepie():
    """ Asks the user interactivly to input a recepie name
    and the ingredience
    
    Returns
    -------
        A dictionary with the recepie name and the list of ingedience
        
        Example
        -------
            {'Applepie':['Apple','Pie']}
    """
    print("Name of the recepie\n")
    name = input("> ")
    recepie = []
    while True:
        print("Add an ingredience or finalize the recepie with 'q'")
        ingredience = input("> ")
        if ingredience in 'q':
            break
        else:
            recepie.append(ingredience)
    return {name: recepie}

def save_recepie(recepie):
    """Saves the recepie to a json file"""
    
    #Get the first key from the dictionary: Name of the recepie
    name = next(iter(recepie.keys()))
    with open(name+'.recepie', 'w') as f:
        json.dump(recepie, f, indent=1)

def get_recepies():
    """Gets all recepies and returns them as one list"""
    grand_list_of_recepies = []
    for recepie in glob.glob("*.recepie"):
        with open(recepie, 'r') as f:
            grand_list_of_recepies.append(json.load(f))
    return grand_list_of_recepies

def return_shuffled_max_seven(a_list):
    """ Returns 7 items from a list"""
    random.shuffle(a_list)
    return a_list[:7]

def print_meals(weekly_meals):
    """Prints a weekplan for meals"""
    week=[]
    for meal in weekly_meals:
        name = next(iter(meal.keys()))
        week.append(name)
    if len(week) < 7:
        print("You only have "+str(len(week))+" recepies")
        for i in range(7-len(week)):
            week.append('')

    print('Mondays:')
    print('    '+str(week[0])+'\n')
    print('Tuesdays:')
    print('    '+str(week[1])+'\n')
    print('Wednesday:')
    print('    '+str(week[2])+'\n')
    print('Thursday:')
    print('    '+str(week[3])+'\n')
    print('Friday:')
    print('    '+str(week[4])+'\n')
    print('Saturday:')
    print('    '+str(week[5])+'\n')
    print('Sunday:')
    print('    '+str(week[6])+'\n')

def print_grocerylist(weekly_meals):
    """Prints the grocersylist"""
    meals=[]
    for meal in weekly_meals:
        name = next(iter(meal.keys()))
        meals.append(name)
    
    recepie_list=[]
    for idx, meal  in enumerate(meals):
        recepie_list.append(weekly_meals[idx][meal])
    
    grocery_list=[]
    for sublists in recepie_list:
        grocery_list += sublists
    
    print("Grocery List:\n")
    grocery_list = list(set(grocery_list))
    print(', '.join(grocery_list))


if __name__ == '__main__':
    sys.exit(main())
