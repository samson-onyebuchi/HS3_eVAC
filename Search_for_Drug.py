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

class Search(Resource):
    def get(self, keyword):
        try:
            drugs = list()
            services = list()

            # Search for drugs
            drug_record = db.drug.find({"drugName": {"$regex": keyword, "$options": "i"}}, {"_id": 0, "drugName": 1, "price": 1})
            for drug in drug_record:
                drugs.append(drug)

            # Search for services
            service_record = db.service.find({"serviceName": {"$regex": keyword, "$options": "i"}}, {"_id": 0, "serviceName": 1, "price": 1})
            for service in service_record:
                services.append(service)

            results = drugs + services

            # If no results are found, append some default values
            if not results:
                results.append({
                    "generic_name": "No results found",
                    "price": "N/A"
                })
        except Exception as e:
            return jsonify(message=f"An exception occurred: {e}", status=False)
        else:
            return jsonify(data=results, message=f"List of drugs and services similar to '{keyword}' retrieved successfully", status=True)

api.add_resource(Search, "/search/<string:keyword>")
