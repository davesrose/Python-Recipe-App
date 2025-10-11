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

    def get_record_length(self):
        query = f"SELECT COUNT(*) FROM NYT_Scrapper"
        self.mycursor.execute(query)
        return self.mycursor.fetchone()[0]

    def post_nyt_recipe(self, recipe):
        recipe_json = json.dumps(recipe)

        # ===== Check for duplicates =====
        title = recipe["Title"]
        sql_query = "SELECT * FROM NYT_Scrapper WHERE JSON_EXTRACT(recipe_data, '$.Title') = %s"
        value_to_search = title
        self.mycursor.execute(sql_query, (value_to_search,))
        results = self.mycursor.fetchall()
        if not results:
            sql = "INSERT INTO NYT_Scrapper (recipe_data) VALUES (%s)"
            val = (recipe_json,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            self.mydb.close()
            return "1 record inserted"
        else:
            return "not inserted"



    def get_recipes(self, offset, per_page):
        sql_query = "SELECT * FROM NYT_Scrapper LIMIT %s OFFSET %s"
        self.mycursor.execute(sql_query, (per_page, int(offset)))
        results = self.mycursor.fetchall()
        return results

    def get_recipe(self, title):
        print("query a recipe")
        sql_query = "SELECT * FROM NYT_Scrapper WHERE JSON_EXTRACT(recipe_data, '$.Title') = %s"
        value_to_search = title
        self.mycursor.execute(sql_query, (value_to_search,))
        return self.mycursor.fetchall()