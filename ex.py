import requests
import json
import ast
# from fpdf2 import FPDF

# filters data
cuisine_type = [
    {'group': 'Asian',
     'type': ['Asian', 'Chinese', 'Indian', 'Japanese', 'Middle Eastern', 'South East Asian']},
    {'group': 'American',
     'type': ['American', 'Mexican', 'South American']},
    {'group': 'European',
     'type': ['British', 'Central European', 'Eastern European', 'French', 'Italian', 'Mediterranean', 'Nordic']},
    {'group': 'Other',
     'type': ['Kosher', 'Caribbean']}]

meal_type = [
    'Breakfast', 'Lunch', 'Dinner', 'Snack', 'Teatime']

diet_type = [
    'dairy-free', 'gluten-free', 'keto-friendly', 'low-sugar', 'paleo', 'peanut-free',
    'pescatarian', 'vegan', 'vegetarian']


def search(ingredient):
    # api connection data
    app_id = '30a1cf92'
    app_key = '001a381e6201c9fbf86f0b3035b6d2cc'

    search_url = f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}'
    response = requests.get(search_url)
    search_results = response.json()
 
    recipes = search_results['hits']
    print(recipes[0])

    return recipes



def show_results():
    # take data from the form
    ingredient = "spinach"

    # run search()
    results = search(ingredient)
    list_of_recipes = []

# collect data from every recipe in search results
    for result in results:
        recipe = result['recipe']
        label = recipe['label']
        url = recipe['url']
        img = recipe['image']
        shopping_list = recipe['ingredientLines']
        servings = recipe['yield']
        nutrients = {
            "cal":
                round(recipe['calories'] / servings),
            "fat":
                round(recipe['totalNutrients']['FAT']['quantity'] / servings, 1),
            "carbohydrates":
                round(recipe['totalNutrients']['CHOCDF']['quantity'] / servings,
                      1),
            "sugar":
                round(recipe['totalNutrients']['SUGAR']['quantity'] / servings, 1),
            "protein":
                round(recipe['totalNutrients']['PROCNT']['quantity'] / servings, 1)
        }
        ingredients = []

        # create list of ingredients
        j = 0  # int for counting no. of ingredients in a recipe
        for ingr in recipe['ingredients']:
            ingredients.append(ingr['food'].lower())
            j += 1

        # join ingredients into one string - ingredients separated with commas
        ingredients_str = ', '.join(ingredients)

        # create one list of elements needed to be shown in search results
        list_of_recipes.append({
            'label': label.capitalize(),
            'url': url,
            'image': img,
            'servings': servings,
            'ingredients': ingredients,
            'ingredients_str': ingredients_str,
            'no_of_ingredients': j,
            'nutrients': nutrients,
            'shopping_list': shopping_list
        })

    # sort recipes by no. of ingredients and by recipe label
    list_of_recipes = sorted(list_of_recipes,
                             key=lambda e:
                             (e['no_of_ingredients'], e['label']))

    i = 0
    for recipe in list_of_recipes:
        recipe['index'] = i
        i += 1

    return list_of_recipes


def saveRecipes(list_of_recipes):
    text = ""
    labels = ('label','url','shopping_list')
    with open("shoppinglist.txt","w+") as all_recipies:
        for recipe in list_of_recipes:
            recipe = {key:value for (key,value) in recipe.items() if key in labels}
            string = json.dumps(recipe)
            text += string + "\n"
        all_recipies.write(text)

def createShoppingList(*args):
    m = open("shoppinglist2.txt","w+")
    with open("shoppinglist.txt","r+") as source:
        all_lines = source.readlines()
        text = ""
        indexes = args[0]
        for index in indexes:
            print(index)
            chosen_recipe = all_lines[index]
            dictionary = ast.literal_eval(chosen_recipe)
            text += f"{dictionary['label']}\n{dictionary['url']}\n\nShopping List:\n"
            for item in dictionary['shopping_list']:
                text += f"\t{item}\n"
            text += "\n\n"
        m.write(text)
    m.close()

global_var = []
def index(name):
    # players = request.form.getlist('check')
    if 'search-button' == name:
        global_var = show_results()
        saveRecipes(global_var)
        return global_var
    elif 'save-button' == name:
        indexes_str = ["2","5","7","12"]
        indexes_int = [int(x) for x in indexes_str]
        createShoppingList(indexes_int)
        # indexes = request.form.getlist('save')
        # pdf = FPDF()
        # pdf.add_page()
        # pdf.set_font("Arial", size = 12)
        # pdf.cell(200, 10, txt = recipe_show,
        #          ln = 1, align = 'C')
        # pdf.output("GFG.pdf")
        return ("ok")
#             for x in f:
# pdf.cell(200, 10, txt = x, ln = 1, align = 'C')

        # path = 'samplefile.pdf'
            # return send_file(path,download_name='shoppinglist.pdf', as_attachment=True)
    else:
        return ("buuu")

results = index('search-button')
for i in results:
    print(i['label'])

results2 = (index('save-button'))
# print(results2)