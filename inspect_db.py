from mongoengine import *
from dbs import Planet

connect('planets')
# print("Listing countries:")
# for country in Planet.objects:
#     print(f"country = {country.name}")
#     print(f"\tpopulation = {country.population}")
#     print(f"\tcurrency = {country.currency}")
#     print(f"\tcurrency_code = {country.currency_code}")

# Delete all records.
Planet.drop_collection()

# Count all records.
# print(Planet.objects.count())

# Mongo dbs cml tools
"""

To install mongodb on Mac:
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community

show dbs
show collections
db.name_of_collection.count()
db.name_of_collection.find().pretty()
db.name_of_collection.find({attribute:value}).pretty()
db.name_of_collection.update({attribute_to_match:value_to_match}, {attribute_to_update:value_to_update})
db.name_of_collection.update({attribute_to_match:value_to_match}, {$set:{attribute_to_update:value_to_update}})
db.name_of_collection.update({attribute_to_match:value_to_match}, {$unset:{attribute_to_update:value_to_update}})
db.name_of_collection.remove({attribute_to_match:value_to_match})
"""