from pymongo import MongoClient
from dotenv import load_dotenv
from optimized_queries import *
from queries import *
import datetime
import certifi
import os

load_dotenv()
URI = os.environ.get("uri")
DATABASE = os.environ.get("db")
COLLECTION = os.environ.get("collection")

client = MongoClient(URI, tlsCAFile=certifi.where())
db = client[DATABASE]
collection = db[COLLECTION]

if __name__ == "__main__":
    aggregation_pipeline = []
    runs = []
    match_query, select_query = sub_categories("pipe")

    for stage, operations in match_query[0].items():
        aggregation_pipeline.append({stage: operations})

    start = datetime.datetime.now()
    aggregation = list(collection.aggregate(aggregation_pipeline))
    end = datetime.datetime.now() - start

    print(end.total_seconds())
    print(aggregation)

    for ctg in aggregation:
        select_query[0]["id"]["$in"].append(ctg["_id"])

    print(select_query[0])

    collection = db["categories"]
    start = datetime.datetime.now()
    aggregation = list(collection.find(
          filter=select_query[0], projection=select_query[1]["select"]
    ))
    end2 = datetime.datetime.now() - start

    print(end2.total_seconds())
    print(aggregation)

    print(f"Total: {end.total_seconds() + end2.total_seconds()}")

