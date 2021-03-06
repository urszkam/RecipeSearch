from flask import Flask, flash, redirect, render_template, request, send_file, url_for
import requests
# from fpdf import FPDF
import json
import ast

app = Flask(__name__, template_folder='templates', static_url_path='/static')

# secret key
app.secret_key = "abcdefgh"

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


def search(ingredient, add_filters):
    # api connection data
    app_id = '30a1cf92'
    app_key = '001a381e6201c9fbf86f0b3035b6d2cc'

    search_url = f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}{add_filters}'
    response = requests.get(search_url)
    search_results = response.json()
 
    recipes = search_results['hits']

    return recipes



def show_results():
    # take data from the form
    ingredient = request.form.get('ingredient')  # main filter
    c_type = request.form.get('c_type')  # additional filters
    m_type = request.form.get('m_type')
    d_type = request.form.get('d_type')

    # concatenate the additional filters
    add_filters = ''
    if c_type != '':
        add_filters = f'&cuisineType={c_type}'
    if m_type != '':
        add_filters += f'&mealType={m_type}'
    if d_type != '':
        add_filters += f'&health={d_type}'
    add_filters = add_filters.replace(' ', '%20')

    # run search()
    results = search(ingredient, add_filters)
    global list_of_recipes
    list_of_recipes = []

# collect data from every recipe in search results
    for result in results:
        recipe = result['recipe']
        label = recipe['label']
        url = recipe['url']
        img = recipe['image']
        servings = recipe['yield']
        shopping_list = recipe['ingredientLines']
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
    with open("recipes.txt","w+") as all_recipies:
        for recipe in list_of_recipes:
            recipe = {key:value for (key,value) in recipe.items() if key in labels}
            string = json.dumps(recipe)
            text += string + "\n"
        all_recipies.write(text)


def createShoppingList(*args):
    m = open("shoppinglist.txt","w+")
    with open("recipes.txt","r+") as source:
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'search-button' in request.form:
            recipe_show = show_results()
            saveRecipes(recipe_show)
            return render_template(
                'index.html',
                list_of_recipes=recipe_show,
                cuisine=cuisine_type,
                diet=diet_type,
                meal=meal_type,
                )
        elif 'save-button' in request.form:
            indexes_str = request.form.getlist('save')
            indexes_int = [int(x) for x in indexes_str]
            createShoppingList(indexes_int)
            # pdf = FPDF()
            # pdf.add_page()
            # pdf.set_font("Arial", size = 12)
            # pdf.cell(200, 10, txt = recipe_show,
            #         ln = 1, align = 'C')
            # pdf.output("GFG.pdf")
            # return render_template('index.html')
            path = 'shoppinglist.txt'
            return send_file(path,download_name='shoppinglist.txt', as_attachment=True)
    else:
        return render_template(
            'index.html',
            cuisine=cuisine_type,
            diet=diet_type,
            meal=meal_type,
        )


if __name__ == '__main__':
    app.run(debug=True)
