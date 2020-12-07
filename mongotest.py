import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Monitor"]
mycol = mydb["emmettcowan"]


mydoc = mycol.find({'App': 'youtube.com'})

for x in mydoc:
    print(x)