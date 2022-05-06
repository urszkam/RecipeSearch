# import packages
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
import requests

app = Flask(__name__, template_folder='templates')

# secret key
app.config.update(dict(
    SECRET_KEY='verysecretkey', ))


def search():
    # declare an ingredient
    app_id = '30a1cf92'
    app_key = '001a381e6201c9fbf86f0b3035b6d2cc'

    # variables from user's form
    ingredient = request.form.get('ingredient')
    c_type = request.form.get('c_type')
    search_url = 'https://api.edamam.com/api/recipes/v2?type=public' \
                 '&q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key)
    response = requests.get(search_url)
    search_results = response.json()
    global recipes
    recipes = search_results['hits']
    return recipes


cuisine_type = [
    {'group': 'Asian', type: ['Asian', 'Chinese', 'Indian', 'Japanese', 'Middle Eastern', 'South East Asian']},
    {'group': 'American', type: ['American', 'Mexican', 'South American']},
    {'group': 'European',
     type: ['British', 'Central European', 'Eastern European', 'French', 'Italian', 'Mediterranean', 'Nordic']},
    {'group': 'Other', type: ['Kosher', 'Caribbean']}]


def show_results():
    search()

    i = 0
    global list_of_recipes
    list_of_recipes = []

    for recipe in recipes:
        label = recipe['recipe']['label']
        url = recipe['recipe']['url']
        cal = recipe['recipe']['calories']
        i += 1
        list_of_recipes.append({'index': i, 'label': label, 'url': url, 'cal': round(cal)})

    return list_of_recipes


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        show_results()
        # return redirect(url_for('index'))

    return render_template(
        'index.html',
        cuisine=cuisine_type,
        list_of_recipes=list_of_recipes)


if __name__ == '__main__':
    app.run(debug=True)
