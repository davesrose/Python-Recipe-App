import os
import dotenv
import mysql.connector
from enums import NYT_Scrapper

dotenv.load_dotenv()
mysql_user = os.getenv("MYSQL_USER")
mysql_pass = os.getenv("MYSQL_PASS")

class Connector:
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user=mysql_user,
                password=mysql_pass,
                database="Recipes"
            )
            self.mycursor = self.mydb.cursor()
            print("Connection successful!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def post_nyt_recipe(self, recipe):
        sql = "INSERT INTO NYT_Scrapper (title, author, introduction, ingredients, steps, tips, nutrition) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (
            recipe[NYT_Scrapper.TITLE.value],
            recipe[NYT_Scrapper.AUTHOR.value],
            recipe[NYT_Scrapper.INTRODUCTION.value],
            recipe[NYT_Scrapper.INGREDIENTS.value],
            recipe[NYT_Scrapper.STEPS.value],
            recipe[NYT_Scrapper.TIPS.value],
            recipe[NYT_Scrapper.NUTRITION.value]
        )
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        self.mycursor.close()