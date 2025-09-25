import requests
import json
from convert_data import ConvertData
from bs4 import BeautifulSoup
import re
from connector import Connector

class NYTScrapper:
    def __init__(self):
        self.recipe = {}
        self.convert_data = ConvertData()

    def iterate_ingredients(self, ul, title):
        ingredients_list = []
        ingredients = ul.find_all(name="li")
        for ingredient in ingredients:
            items = ingredient.find_all("span")
            quantity = items[0].getText()
            if len(items) > 1:
                item = items[1].getText()
                ingredient_str = f"{quantity} {item}"
            else:
                ingredient_str = f"{quantity}"
            formated_ingredient = self.convert_data.convert_unicode_ascii(ingredient_str)
            # formated_ingredient = ingredient_str
            ingredients_list.append(formated_ingredient)
        if title:
            ingredient_group = {
                "Section": title,
                "Ingredients": ingredients_list
            }
        else:
            ingredient_group = ingredients_list

        return ingredient_group


    def scrapper(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

    # ========= Title ==================
        recipe_title = soup.select_one(selector='header h1').getText()
    # ========= Author =================
        recipe_author = soup.select_one(selector='h2 a').getText()
    # ========= Introduction ===========
        recipe_intro_paragraphs = soup.find(name="div", attrs={"class": re.compile("topnote_*")}).find_all(name="p")
        intro_list = []
        for intro in recipe_intro_paragraphs:
            intro_list.append(intro.getText())
    # ========= Ingredients ===========
        ingredients = soup.find(name="div", attrs={"class": re.compile("ingredients_ingredients*")})
        # if one set of ingredients, there will be one ul vs a nested h3 and ul for multiple
        ingredient_group_titles = ingredients.find_all(name="h3")
        ingredient_uls = ingredients.find(name="ul")
        if ingredient_group_titles:
            ingredient_uls = ingredients.select('ul ul')
            ingredient_list = []
            for index in range(0, len(ingredient_group_titles)):
                title = ingredient_group_titles[index].getText()
                ingredient_list.append(self.iterate_ingredients(ingredient_uls[index], title))
        else:
            ingredient_list = self.iterate_ingredients(ingredient_uls, None)
        print(ingredient_list)
    # ========= Steps =========
        steps = soup.find(name="ol", attrs={"class": re.compile("preparation_stepList*")})
        step_list = steps.select('li p')
        preparation = []
        for step in step_list:
            preparation.append(step.getText())

        tips_select = soup.find(name="ul", attrs={"class": re.compile("tips_tipsList*")})
        if tips_select:
            tips_list = tips_select.select('li')
            tips = []
            for tip in tips_list:
                tips.append(tip.getText())
        else:
            tips = None

    # ========= Nutrition Information =========
        nutrition = soup.find(name="div", attrs={"class": re.compile("-nutritional-information*")})
        nutrition_servings = self.convert_data.convert_unicode_ascii(nutrition.find(name="h5").getText())
        nutrition_info = self.convert_data.convert_unicode_ascii(nutrition.find(name="p", attrs={"class": "pantry--ui"}).getText())
        nutrition_group = {
            "Servings": nutrition_servings,
            "Info": nutrition_info
        }

    # ========= Recipe Dictionary
        self.recipe = [
            str(recipe_title),
            str(recipe_author),
            str(intro_list),
            str(ingredient_list),
            str(preparation),
            str(tips),
            str(nutrition_group)
        ]

        post = Connector()
        post.post_nyt_recipe(self.recipe)

        return self.recipe
