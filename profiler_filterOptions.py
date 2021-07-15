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
    # query = filter_options_search("pipe")
    #
    # start = datetime.datetime.now()
    # results_1 = list(collection.distinct("details.brand", filter=query[0]))
    # end = datetime.datetime.now() - start
    #
    # print("Brands only", end.total_seconds())
    # print(results_1)

    # query, select, distinct = filter_options(False)
    #
    # start = datetime.datetime.now()
    # results_2 = list(collection.distinct(distinct, filter=query))
    # end = datetime.datetime.now() - start
    #
    # print("Suppliers only", end.total_seconds())
    # print(results_2)

    pipeline = filter_options_search("hammer")
    aggregation_pipeline = []

    for stage, operations in pipeline[0].items():
        aggregation_pipeline.append({stage: operations})

    aggregation_pipeline.insert(3, {"$unwind": {
        "path": "$vendors",
        "preserveNullAndEmptyArrays": False
    }})

    # for stage in aggregation_pipeline:
    #     print(stage)

    start = datetime.datetime.now()
    aggregation = list(collection.aggregate(aggregation_pipeline))
    end = datetime.datetime.now() - start

    print(aggregation)

    print(end.total_seconds())
    print(len(aggregation[0]["uniqueBrands"]), aggregation[0]['uniqueBrands'])
    print(len(aggregation[0]["uniqueVendors"]), aggregation[0]['uniqueVendors'])

