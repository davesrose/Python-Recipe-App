import datetime
from flask import Flask, render_template, request, session
from flask_paginate import Pagination
from nyt_scrapper import NYTScrapper
from connector import Connector
import json

PORT="5003"
DOMAIN=f"http://127.0.0.1:{PORT}"

app = Flask(__name__)
app.secret_key = 'super_secret_key'

year = datetime.datetime.now().year

recipes_per_page = 30

@app.route('/')
def index():
    page = session.get('page')
    return render_template("index.html", year=year, page=page)

@app.route('/post_recipe', methods=['GET', 'POST'])
def post_recipe():
    page = session.get('page')
    if request.method == 'POST':
        recipe_url = request.form.get('recipe_url')
        recipe_list = request.form.get('recipe_list')
        if not recipe_list:
            nyt_scrapper = NYTScrapper().get_recipe(recipe_url)
            message = False
            if "1 record inserted" in nyt_scrapper:
                print("modal should print 1 record inserted")
                message = "Recipe successfully recorded."
            elif "not inserted" in nyt_scrapper:
                print("modal should say no record inserted")
                message = "The recipe appears to be a duplicate.  It won't be recorded."
            return render_template("submit_url.html", message=message, year=year, page=page)
        elif recipe_list:
            recipe_list = json.loads(recipe_list)
            for item in recipe_list:
                nyt_scrapper = NYTScrapper().get_recipe(item)
            message = "Recipes recorded."
            return render_template("submit_url.html", message=message, page=page)
    return render_template("submit_url.html", message=False, year=year, page=page)

recipes = []
def get_items(offset=0, per_page=40):
    return recipes[offset: offset + per_page]

@app.route('/nyt_recipes')
def nyt_recipes():
    per_page = request.args.get('per_page', 40, type=int)
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * per_page
    response = Connector().get_recipes(offset, per_page)
    session['page'] = page
    recipes = []
    for item in response:
        recipes.append({
            "id": item[0],
            "recipe": json.loads(item[1])
        })
    table_length = Connector().get_record_length()
    pagination_recipes = get_items(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=table_length, css_framework='bootstrap5')
    return render_template("nyt_recipes.html", recipes=recipes, offset=offset, domain=DOMAIN, items=pagination_recipes, page=page, per_page=per_page, pagination=pagination)

@app.route('/nyt_recipe/<title>')
def nyt_recipe(title):
    page = session['page']
    results = Connector().get_recipe(title) # includes recipe id
    result = json.loads(results[0][1])
    ingredients = result["Ingredients"]
    is_ingredient_list = isinstance(ingredients, list)
    return render_template("recipe.html", results=result, page=page, ingredients=ingredients, is_list=is_ingredient_list, domain=DOMAIN)

@app.route('/input_custom_recipe', methods=["GET", "POST"])
def input_custom_recipe():
    if request.method == 'POST':
        title = request.form.get("title")
        author = request.form.get("author")
        url = request.form.get("recipe_url")
        ingredients = request.form.get("ingredients").splitlines()
        steps = request.form.get("steps").splitlines()
        recipe_data = {
            "Title": title,
            "Recipe ID": url,
            "Author": author,
            "Ingredients": ingredients,
            "Instructions": steps,
        }
        post = Connector().post_recipe(recipe_data, 'Custom_Recipes')
        return render_template("input_custom_recipe.html")
    return render_template("input_custom_recipe.html")

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
    # app.run(host='0.0.0.0', port=5000) # for running on network (IE access IP:5000)