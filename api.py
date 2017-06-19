# -*- coding: utf-8 -*-

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["MONGO_DBNAME"] = "bip"
mongo = PyMongo(app, config_prefix='MONGO')
APP_URL = "http://127.0.0.1:9000"


class Student(Resource):
    def get(self, registration=None, department=None):
        data = []

        #Indice para poder ocupar la función near
        mongo.db.bipCenters.create_index([("point", "2dsphere")])
        
        #Obtener los parametros ingresados
        latitud = float(request.args.get("latitud"))
        longitud = float(request.args.get("longitud"))
        radio = int(request.args.get("radio"))
        
        #Encontrar todos los puntos bip cerca de la ubicacion ingresada
        closeBipCenters = mongo.db.bipCenters.find({
        "point":
            {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [latitud, longitud]
                    },
                    "$maxDistance": radio
                }
            }
        })

        for closeBipCenter in closeBipCenters:
            data.append(closeBipCenter)
        return jsonify(data)


class Index(Resource):
    def get(self):
        return redirect(url_for("bipcenters"))


api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(Student, "/bipcenters", endpoint="bipcenters")

if __name__ == "__main__":

    app.run(debug=True, port= 9000)

