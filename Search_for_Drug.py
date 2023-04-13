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
        keyword = request.args.get("keyword")

        # If keyword is None, retrieve all drugs from the collection
        if keyword is None:
            drugs = db.drug.find({}, {"_id": 0, "name": 1})
        else:
            # Otherwise, retrieve drugs that match the keyword
            drugs = db.drug.find({"name": {"$regex": keyword, "$options": "$i"}}, {"_id": 0, "name": 1})

        
        drug_list = []
        for drug in drugs:
            drug_list.append(drug["name"])

        
        return jsonify({"drugs": drug_list})

api.add_resource(DrugList, "/drugs")