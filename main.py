from ny_times_scrapper import NYTScrapper
import json
import os
import dotenv
import mysql.connector

dotenv.load_dotenv()
single_group_ingredients = os.getenv("NYT_SINGLE_INGREDIENTS")
multiple_group_ingredients = os.getenv("NYT_MULTIPLE_INGREDIENTS")



# https://cooking.nytimes.com/robot.txt usual page for terms of use (can scrape for personal use if subscribed)

nyt_scrapper = NYTScrapper().scrapper(multiple_group_ingredients)

print(nyt_scrapper)
