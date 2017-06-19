from pymongo import MongoClient

#Conectarse a BD Mongo
db = MongoClient("mongodb://localhost:27017").bip

bipCenters = db.bipCenters.find()

for bipCenter in bipCenters:
    db.bipCenters.update({
        "_id": bipCenter["_id"]
    }, {
        "$set": {
            "point": {
                "type": "Point",
                "coordinates": [float(bipCenter["LATITUD"]), float(bipCenter["LONGITUD"])]
            }
        }
    })
