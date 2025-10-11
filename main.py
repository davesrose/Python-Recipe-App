from nyt_scrapper import NYTScrapper
import os
import dotenv

dotenv.load_dotenv()
single_group_ingredients = os.getenv("NYT_SINGLE_INGREDIENTS")
multiple_group_ingredients = os.getenv("NYT_MULTIPLE_INGREDIENTS")

# https://cooking.nytimes.com/robot.txt usual page for terms of use (can scrape for personal use if subscribed)

nyt_scrapper = NYTScrapper().get_recipe(single_group_ingredients)
# print(nyt_scrapper)
