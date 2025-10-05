import requests
import json
import re
from bs4 import BeautifulSoup
from convert_data import ConvertData
from connector import Connector

class NYTScrapper:
    def __init__(self):
        self.convert_data = ConvertData()

    def iterate_ingredients(self, ul):
        # function for creating lists of ingredients when there's groups
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
            ingredients_list.append(formated_ingredient)
        return ingredients_list

    def get_recipe(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # ==== first grab recipe data from script json in head of recipe
        head_tag = soup.find('head')
        json_script_tag = head_tag.find('script', type='application/ld+json').string
        recipe = json.loads(json_script_tag)

        title = recipe["mainEntityOfPage"]["name"]
        recipe_id = recipe["mainEntityOfPage"]["@id"]
        author = recipe["author"]["name"]
        nutrition = recipe["nutrition"]

        json_ingredients = recipe["recipeIngredient"]
        # ==== check if there's different groups of ingredients

        ingredient_scrape = soup.find(name="div", attrs={"class": re.compile("ingredients_ingredients*")})

        # if one set of ingredients, there will be one ul vs a nested h3 and ul for multiple
        ingredient_group_titles = ingredient_scrape.find_all(name="h3")
        if ingredient_group_titles:
            ingredients = {}
            ingredient_uls = ingredient_scrape.select('ul ul')
            for index in range(0, len(ingredient_group_titles)):
                ingredients[ingredient_group_titles[index].getText()] = self.iterate_ingredients(ingredient_uls[index])

        else:
            ingredients = json_ingredients

        get_instructions = recipe["recipeInstructions"]
        instructions = []
        for instruction in get_instructions:
            instructions.append(instruction["text"])

        # ====== look in page for tips =====
        tips_select = soup.find(name="ul", attrs={"class": re.compile("tips_tipsList*")})
        if tips_select:
            tips_list = tips_select.select('li')
            tips = {}
            for index in range(0,len(tips_list)):
                tips[index] = tips_list[index].getText()
        else:
            tips = None

        year = recipe["copyrightYear"]

        formatted_recipe = {
            "Title": title,
            "Recipe ID": recipe_id,
            "Author": author,
            "Ingredients": ingredients,
            "Instructions": instructions,
            "Tips": tips,
            "Nutrition": nutrition,
            "Year": year
        }

        post = Connector()
        post.post_nyt_recipe(formatted_recipe)

        return formatted_recipe
