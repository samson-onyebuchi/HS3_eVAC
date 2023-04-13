from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
api = Api(app)

try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["Test_mod"]
except Exception as e:
    db = None

class DrugList(Resource):
    def get(self):
        try:
            # Get the value of the name query parameter from the URL
            name = request.args.get("name")

            # If name is None, retrieve all drugs from the collection
            if name is None:
                drugs = db.drug.find({}, {"_id": 0, "name": 1})
            else:
                # Otherwise, retrieve only drugs with a matching name
                drugs = db.drug.find({"name": name}, {"_id": 0, "name": 1})

            # Convert the drugs to a list
            drug_list = []
            for drug in drugs:
                drug_list.append(drug["name"])

            # Return the drug list as a Python list
            return drug_list

        except Exception as e:
            error_msg = {"error": "An error occurred while retrieving data from the database."}
            return jsonify(error_msg)

api.add_resource(DrugList, "/drugs")
