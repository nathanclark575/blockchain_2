"""
    Demonstrates how json files are writen to and read
"""

import json

# make data
book = {}

book["Nathan"] = {
    "name" : "Nathan",
    "adress" : "Home",
    "phone" : "07748828173"
}

book["Grace"] = {
    "name" : "Grace",
    "adress" : "Home",
    "phone" : "999"
}

# converts data in book to a json string
json_string = json.dumps(book)
with open("test.txt", "w") as file:
    file.write(json_string)
file.close()

# reads the data and stores it as a string
with open("test.txt", "r") as file:
    string_2 = file.read()
file.close()

# change to dic to read it
book_2 = json.loads(string_2)
#print the names of people in the book
for person in book_2:
    print(book_2[person]["name"])