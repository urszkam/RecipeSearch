# import packages
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
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


def search():
    global recipes
    global add_filters

    # api connection data
    app_id = '30a1cf92'
    app_key = '001a381e6201c9fbf86f0b3035b6d2cc'

    # take chosen filters from the form
    ingredient = request.form.get('ingredient')  # main filter
    c_type = request.form.get('c_type')  # additional filters
    m_type = request.form.get('m_type')
    d_type = request.form.get('d_type')

    # concatenate the additional filters
    add_filters = ''
    if c_type != '':
        add_filters = '&cuisineType={}'.format(c_type)
    if m_type != '':
        add_filters += '&mealType={}'.format(m_type)
    if d_type != '':
        add_filters += '&health={}'.format(d_type)
    add_filters = add_filters.replace(' ', '%20')

    search_url = 'https://api.edamam.com/api/recipes/v2?type=public' \
                 '&q={}&app_id={}&app_key={}{}'.format(ingredient, app_id, app_key, add_filters)
    response = requests.get(search_url)
    search_results = response.json()
    recipes = search_results['hits']

    return recipes


def show_results():

    search()

    global list_of_recipes
    list_of_recipes = []

    i = 0
    for recipe in recipes:
        rec = recipe['recipe']

        label = rec['label']
        url = rec['url']
        cal = rec['calories']
        img = rec['image']
        ingredients = rec['ingredients']
        servings = rec['yield']
        nutrients = {"cal_per_serving": rec['calories'] / servings,
                "fat": rec['totalNutrients']['FAT']['quantity'] / servings,
                "carbohydrates": rec['totalNutrients']['CHOCDF']['quantity'] / servings,
                "sugar": rec['totalNutrients']['SUGAR']['quantity'] / servings,
                "protein": rec['totalNutrients']['PROCNT']['quantity'] / servings}

        i += 1
        list_of_recipes.append({
            'index': i,
            'label': label.capitalize(),
            'url': url,
            'cal': round(cal),
            'image': img,
            'ingredients': ingredients,
            'nutrients': nutrients})

    return list_of_recipes


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        show_results()
        return render_template('index.html',
                               list_of_recipes=list_of_recipes,
                               cuisine=cuisine_type,
                               diet=diet_type,
                               meal=meal_type)
        # return redirect(url_for('index'))
    else:
        return render_template(
            'index.html',
            cuisine=cuisine_type,
            diet=diet_type,
            meal=meal_type,
            #list_of_recipes=list_of_recipes
        )


if __name__ == '__main__':
    app.run(debug=True)
