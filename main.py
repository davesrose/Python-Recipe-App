from ny_times_scrapper import NYTScrapper
import json

# https://cooking.nytimes.com/robot.txt usual page for terms of use (can scrape for personal use if subscribed)

nyt_scrapper = NYTScrapper().scrapper("https://cooking.nytimes.com/recipes/1022317-jalapeno-grilled-pork-chops")
# nyt_scrapper = NYTScrapper().scrapper("https://cooking.nytimes.com/recipes/1027143-corn-and-parmesan-pasta")
print(json.dumps(nyt_scrapper))
