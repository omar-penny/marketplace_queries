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
    query = main_search("pipe")

    # Create aggregation stage list
    for stage, operations in query[0].items():
        aggregation_pipeline.append({stage: operations})

    print(aggregation_pipeline)

    start = datetime.datetime.now()
    aggregation = list(collection.aggregate(aggregation_pipeline))
    end = datetime.datetime.now() - start

    # print(aggregation)
    print(end.total_seconds())

    for i in range(0, len(aggregation)):
        runs.append({
            "number": i,
            "time": end.total_seconds(),
            # "size": len(aggregation[i]["val"]),
            # "ID": aggregation[i]["id"],
            "name[en]": aggregation[i]["name"]["en"],
            "sku": aggregation[i]["details"]["sku"],
            # "description": aggregation[i]["details"]["description"],
            # "brand": aggregation[i]["details"]["brand"],
            # "specs": aggregation[i]["techSpecs"],
            "score": aggregation[i]["score"],
        })

    for i in runs:
        print(i)
