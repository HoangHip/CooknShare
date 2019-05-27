from allrecipes import AllRecipes
from pymongo import MongoClient
from bson.objectid import ObjectId

uri = "mongodb+srv://admin:admin@c4e29-cluster-qtb0x.mongodb.net/test?retryWrites=true"

client = MongoClient(uri)

project_database = client.project_database

food_collection = project_database["food_collection"]

query_options = {
  "wt": "Asian",         # Query keywords
}
query_result = AllRecipes.search(query_options)

food_list = []
i = 0

for item in query_result:
    if i <= len(query_result):
        One_food = {}
        One_food['Name'] = query_result[i]['name']
        One_food['Description'] = query_result[i]['description']
        One_food['Image'] =  query_result[i]['image']
        main_recipe_url = query_result[i]['url']
        detailed_recipe = AllRecipes.get(main_recipe_url)
        One_food['Ingredients'] = detailed_recipe['ingredients']
        One_food['Steps'] = detailed_recipe['steps']
        One_food['Continent'] = 'Asian'
        food_list.append(One_food)
        i += 1
    else:
        break

print(food_list)

# food_collection.insert_many(food_list)
