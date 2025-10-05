import os
import dotenv
import mysql.connector
import json

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
        recipe_json = json.dumps(recipe)
        title = recipe["Title"]
        sql_query = "SELECT * FROM NYT_Scrapper WHERE JSON_EXTRACT(recipe_data, '$.Title') = %s"
        value_to_search = title
        self.mycursor.execute(sql_query, (value_to_search,))
        results = self.mycursor.fetchall()
        if not results:
            print("no duplicates")
            sql = "INSERT INTO NYT_Scrapper (recipe_data) VALUES (%s)"
            val = (recipe_json,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()

            print(self.mycursor.rowcount, "record inserted.")
            self.mydb.close()
        else:
            print("Not inserted, duplicate")

    def get_recipes(self, start_row, end_row):