import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 78, "name": "Joe", "views": "100000"},
        {"likes": 10000, "name": "How to make REST API", "views": "80000"},
        {"likes": 35, "name": "Tim", "views": "2000"}]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])    # send a get request to the url that has "BASE+helloworld"
    print(response.json())

# input()
# response = requests.delete(BASE + "video/0")
# print(response)                 # this doesn't response with json file since for delete(), we don't return anything
input()
response = requests.get(BASE + "video/6") 
print(response.json())