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
    query = category_products()

    # Create aggregation stage list
    for stage, operations in query[0].items():
        aggregation_pipeline.append({stage: operations})

    start = datetime.datetime.now()
    aggregation = list(collection.aggregate(aggregation_pipeline))
    end = datetime.datetime.now() - start

    print(len(aggregation))
    print(end.total_seconds())
    #
    # print(aggregation[0]["totalCount"])
    # print(aggregation[0]["paginatedResults"])

    # aggregation = aggregation[0]["paginatedResults"]

    # pipeline = filter_options_aggregation()
    #
    # aggregation_pipeline = []
    #
    # for stage, operations in pipeline[0].items():
    #     aggregation_pipeline.append({stage: operations})
    #
    # aggregation_pipeline.insert(2, {"$unwind": {
    #     "path": "$vendors",
    #     "preserveNullAndEmptyArrays": False
    # }})
    # print(aggregation_pipeline)
    #
    # start = datetime.datetime.now()
    # aggregation = list(collection.aggregate(aggregation_pipeline))
    # end = datetime.datetime.now() - start
    #
    # print(end.total_seconds())

    # query = main_search("pipe")
    #
    # # Create aggregation stage list
    # for stage, operations in query[0].items():
    #     aggregation_pipeline.append({stage: operations})
    #
    # print(aggregation_pipeline)
    #
    # start = datetime.datetime.now()
    # aggregation = list(collection.aggregate(aggregation_pipeline))
    # end = datetime.datetime.now() - start
    #
    # print(end.total_seconds())

    for i in range(0, len(aggregation)):
        runs.append({
            "run": i,
            "time": end.total_seconds(),
            # "number": aggregation[i]["fieldN"],
            # "name": aggregation[i]["_id"]
            # "size": len(aggregation[i]["val"]),
            # "ID": aggregation[i]["id"],
            "name[en]": aggregation[i]["name"]["en"],
            # "sku": aggregation[i]["details"]["sku"],
            # "description": aggregation[i]["details"]["description"],
            # "brand": aggregation[i]["details"]["brand"],
            # "specs": aggregation[i]["techSpecs"],
            # "score": aggregation[i]["score"],
        })

    for i in runs:
        print(i)
    #
    # print(runs)