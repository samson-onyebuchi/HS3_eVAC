from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser
from bson import ObjectId
from app.schemas import Facility, PRecords, Referrals, Hmo, HmoAthu, QueryFac, QueryHom, RefRec, RefFac
from app.schemas import ReferralSec, Diagnose, Serivces, Drugs, EncounterImage
#from utils import current_date, create_code
from app.utils import current_date, create_code
#from model import get_enrid, get_depenrid
#from file_upload import uploadfile, add_enconters
from dotenv import load_dotenv
#from mongo_url import mongo_url
import os

load_dotenv()

app = Flask(__name__)
#client = MongoClient((mongo_url()))
client = MongoClient(os.getenv("MONGO_URI"))
db = client["Test_mod"]



# def check_sub(exp_date,duration):
#     today = datetime.today()
#     if exp_date == False:
#         return "active"

#     diff = relativedelta(exp_date, today)
#     if diff.months == (duration % 12) and (duration % 12) < 6:
#         return "expired"
#     else:
#         return "active"
    
def check_sub(expiry_date, total_duration):
    """
    Checks subscription status based on expiry date and total duration
    """
    today = date.today()
    expiry_date = parser.parse(expiry_date).date()
    duration = relativedelta(expiry_date, today).months + 1
    if duration < total_duration:
        return "active"
    elif today <= expiry_date:
        return "active"
    else:
        return "expired"

@app.route("/patient/records/<enrollment_id>", methods=["GET"])
def patient_records(enrollment_id):
    try:
        en_result = db.enrollments.find_one({"enrollment_id": enrollment_id}, {
            "passport": 1,
            "name": 1,
            "date_of_birth": 1,
            "phone_number": 1,
            "address": 1,
            "enrollment_id": 1,
            "facility": 1,
            "hmo": 1,
            "subcategoryitem": 1,
            "_id": 0,
        })

        if not en_result:
            return {"message": "Invalid enrollment ID", "status": False}

        dates = current_date - relativedelta(months=3)
        encounters = db.encounters.find(
            {"enrollment_id": enrollment_id, "submission_time": {"$gte": request.args.get("date", dates)}},
            {"_id": 0})
        if not encounters:
            return {"message": "No encounter records found", "status": False}

        primary = []
        secondary = []
        for enc in encounters:
            if enc["type"] == "encounter":
                del enc["facility"]
                primary.append(enc)
            else:
                secondary.append(enc)
            del enc["type"]

        en_result["Nominal roll"] = [
            {"Passport": en_result.get("passport")},
            {"Name": en_result.get("name")},
            {"DOB": en_result.get("date_of_birth")},
            {"Phone Number": en_result.get("phone_number")},
            {"Address": en_result.get("address")},
            {"Enrid": en_result.get("enrollment_id")},
            {"Facility": en_result.get("facility")},
            {"HMO": en_result.get("hmo")},
            {"subcategoryItem": en_result.get("subcategoryitem")},
        ]

        en_result["primary_encounters"] = primary
        en_result["secondary_referrals"] = secondary
    except Exception as e:
        return jsonify(message=f"An exception occurred: {e}", status=False)
    else:
        return {"data": en_result, "message": f"showing patient records from {request.args.get('date', dates)} till date",
            "status": True}

@app.route("/verify/", methods=["POST"])
def verify():
    try:
        data = request.json
        payload = Facility().load(data)
        result = db.subscriptions.find_one({"enrollment_id": payload["enrollment_id"]})
        if not result:
            return jsonify(message="Invalid Enrollment Id", status=False), 401

        payload["facility_no"] = (result["facility"]["id"]) if int(payload["facility_no"]) == 34000 else payload[
            "facility_no"]

        staff_result = db.facilities.find_one(
            {"$or": [{"oic_number": payload["facility_no"]}, {"name.id": payload["facility_no"]}]})

        if not staff_result:
            return jsonify(message="Number not authorized", status=False), 401

        if result["facility"]["id"] != staff_result["name"]["id"]:
            return jsonify(message="You can't generate code for someone not assigned to your facility", status=False),

        enc = db.encounters.find_one({"enrollment_id": payload["enrollment_id"], "archive": False,
                                          "type": "encounter"}, {"_id": 0})
        if enc:
            #return jsonify(message=f"Enrollee has an active encounter {enc['code']}", status=False)
            return jsonify(message=f"Enrollee has an active encounter code", status=False)

        if check_sub(result["expiry_date"], result["total_duration"]) == "expired":
            return jsonify(message=f"Enrollee has no active subscription please top-up to receive services", status=False)

        code = create_code(8)
        existing_code = db.encounters.find_one({"code": code, "archive": False})
        while existing_code:
            code = create_code(8)
            existing_code = db.encounters.find_one({"code": code, "archive": False})

        db.encounters.insert_one(
            {"enrollment_id": payload["enrollment_id"], "hmo": result['hmo'], "code": code,
             "submission_time": parser.parse(str(current_date)),
             "facility": result["facility"], "services": [], "drugs": [], "diagnosis": [], "type": "encounter",
             "images": [], "archive": False})
    except Exception as e:
        return jsonify(message=f"An exception occurred: {e}", status=False)
    else:
        #return {"message": f"Encounter Code For {payload['enrollment_id']} is {code}", "status": True}
        return {"message": f"Encounter Code For {payload['enrollment_id']} is created successfully","code":code, "status": True}

