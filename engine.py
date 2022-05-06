# import packages
import requests

app_id = '30a1cf92'
app_key = '001a381e6201c9fbf86f0b3035b6d2cc'


def search():
    # declare an ingredient
    ingredient = input('Enter the ingredient:\n')
    search_url = 'https://api.edamam.com/api/recipes/v2?type=public' \
                 '&q={}&app_id={}&app_key={}'.format(ingredient, app_id, app_key)
    response = requests.get(search_url)
    search_results = response.json()
    global recipes
    recipes = search_results['hits']


def one_ingredient():
    search()
    i = 1
    for recipe in recipes:
        label = recipe['recipe']['label']
        url = recipe['recipe']['url']
        cal = recipe['recipe']['calories']
        print('{}: {}\n    {}\n    cal: {} kcal per serving\n'.format(i, label.title(), url, round(cal)))
        i += 1


one_ingredient()

# cuisineType American, Asian, British, Caribbean, Central Europe, Chinese, Eastern Europe, French, Indian, Italian, Japanese, Kosher, Mediterranean, Mexican, Middle Eastern, Nordic, South American, South East Asian
