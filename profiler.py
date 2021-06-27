from pymongo import MongoClient
from dotenv import load_dotenv
from queries import Query
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
    query = Query().main_search()

    for stage, operations in query[0].items():
        aggregation_pipeline.append({stage: operations})

    start = datetime.datetime.now()
    aggregation = list(collection.aggregate(aggregation_pipeline))
    end = datetime.datetime.now() - start

    # runs.append({"totalCount": aggregation[0]["totalCount"]})
    # aggregation = aggregation[0]["paginatedResults"]

    for i in range(0, len(aggregation)):
        runs.append({
            "number": i,
            "time": end.total_seconds(),
            "name[en]": aggregation[i]["name"]["en"],
            "sku": aggregation[i]["details"]["sku"],
            "des": aggregation[i]["details"]["description"],
            "brand": aggregation[i]["details"]["brand"],
            "score": aggregation[i]["score"],
        })

    for i in runs:
        print(i)