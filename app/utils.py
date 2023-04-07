from random import randint
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
# from insure import mon
from dateutil.relativedelta import relativedelta
import pytz


current_date = datetime.now()


def create_code(length:int):
    num = "0".zfill(length-1)
    num = int(str(length)+num)
    code = randint(1, num)
    code = str(code).zfill(length)

    return code
def check_exp(exp_date):
    today = current_date - exp_date.utcnow()
    if today.days > 14:
        return "expired"
    else:
        return "active"
def check_sub(exp_date,duration):
    if exp_date == False:
        return "active"

    diff = relativedelta(exp_date, current_date)
    if diff.months == (duration % 12) and (duration % 12) < 6:
        return "expired"
    else:
        return "active"
def months_date(mon):
    mon = current_date - relativedelta(months=mon)
    return mon
def days_date(days):
    Enddate = current_date - timedelta(days=days)

    return Enddate
def convert_datetostring(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m")
    formatted_date = date_obj.strftime("%b '%y")
    return formatted_date


# def month_summary(collection, month):
#     """
#     Generate a summary of data from a MongoDB database for a given month.
#
#     Parameters:
#         collection (str): The name of the collection to aggregate data from. Possible values are:
#                           "enrollments", "dependents", "facilities", "category", "hmos",
#                           "subscriptions", "encounters", and "nominal".
#         month (str): The month for which data should be aggregated.
#
#     Returns:
#         list: A list of dictionaries, where each dictionary represents a month and year and contains
#               the keys "x" (a string representation of the month and year) and "y" (the count of
#               documents in the aggregated data for the given month and year). The list is sorted by
#               the "x" values.
#
#     Example:
#         month_summary("enrollments", "Jan 2022")
#         Output: [{'x': 'Jan 2022', 'y': 5}, {'x': 'Feb 2022', 'y': 3}, ...]
#     """
#
#     col = {"enrollments": mon.db.enrollments.aggregate,
#            "dependents": mon.db.dependents.aggregate,
#            "facilities": mon.db.facilities.aggregate,
#            "category": mon.db.enrollment.aggregate,
#            "hmos": mon.db.hmos.aggregate,
#            "subscriptions": mon.db.subscriptions.aggregate,
#            "encounters": mon.db.encounters.aggregate,
#            "nominal": mon.db.nominal.aggregate}
#     data = col[collection]([
#         {"$match": {"submission_time": {"$gte": months_date(month)}}},
#         {
#             "$project": {
#                 "month": {"$month": "$submission_time"},
#                 "year": {"$year": "$submission_time"},
#                 "x": {"$dateToString": {"format": "%Y-%m", "date": "$submission_time"}},
#             }
#         },
#         {"$group": {"_id": {"x": "$x"}, "count": {"$sum": 1}}}
#     ])
#
#     data_list = list(data)
#     data_list = [{'x': convert_datetostring(doc['_id']['x']), 'y': doc['count']} for doc in data_list]
#
#     data_list.sort(key=lambda date: datetime.strptime(date["x"], "%b '%y"))
#
#     return data_list



def create_excel(data_frames: dict):
    out = BytesIO()
    writer = pd.ExcelWriter(out, engine='openpyxl')
    for sheet_name, df in data_frames.items():
        df.to_excel(writer, sheet_name=sheet_name,index=False)

    writer.close()
    return out.getvalue()

