# import packages
from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates', static_url_path='/static')

# secret key
app.secret_key = "abc"

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
    global recipes

    # api connection data
    app_id = '30a1cf92'
    app_key = '001a381e6201c9fbf86f0b3035b6d2cc'

    search_url = f'https://api.edamam.com/api/recipes/v2?type=public&q={ingredient}&app_id={app_id}&app_key={app_key}{add_filters}'
    response = requests.get(search_url)
    search_results = response.json()
    recipes = search_results['hits']

    return search_results['hits']



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

    list_of_recipes = []

# collect data from every recipe in search results
    for result in results:
        recipe = result['recipe']
        label = recipe['label']
        url = recipe['url']
        img = recipe['image']
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
        i = 0  # int for counting no. of ingredients in a recipe
        for ingr in recipe['ingredients']:
            ingredients.append(ingr['food'].lower())
            i += 1

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
            'no_of_ingredients': i,
            'nutrients': nutrients
        })

    # sort recipes by no. of ingredients and by recipe label
    list_of_recipes = sorted(list_of_recipes,
                             key=lambda e:
                             (e['no_of_ingredients'], e['label']))

    return list_of_recipes


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        recipe_show = show_results()
        return render_template(
            'index.html',
            list_of_recipes=recipe_show,
            cuisine=cuisine_type,
            diet=diet_type,
            meal=meal_type
            )
    else:
        return render_template(
            'index.html',
            cuisine=cuisine_type,
            diet=diet_type,
            meal=meal_type,
        )


if __name__ == '__main__':
    app.run(debug=True)
