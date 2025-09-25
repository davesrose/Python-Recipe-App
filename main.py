from ny_times_scrapper import NYTScrapper
import json

# https://cooking.nytimes.com/robot.txt usual page for terms of use (can scrape for personal use if subscribed)

nyt_scrapper = NYTScrapper().scrapper()

print(json.dumps(nyt_scrapper))
