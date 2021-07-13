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
    query, select, distinct = filter_options(True)

    start = datetime.datetime.now()
    results_1 = list(collection.distinct(distinct, filter=query))
    end = datetime.datetime.now() - start

    print("Brands only", end.total_seconds())
    # print(results_1)

    query, select, distinct = filter_options(False)

    start = datetime.datetime.now()
    results_2 = list(collection.distinct(distinct, filter=query))
    end = datetime.datetime.now() - start

    print("Suppliers only", end.total_seconds())
    # print(results_2)

    pipeline = filter_options_aggregation(True)
    aggregation_pipeline = []

    for stage, operations in pipeline[0].items():
        aggregation_pipeline.append({stage: operations})

    aggregation_pipeline.insert(2, {"$unwind": {
        "path": "$vendors",
        "preserveNullAndEmptyArrays": False
    }})

    for stage in aggregation_pipeline:
        print(stage)

    start = datetime.datetime.now()
    aggregation = list(collection.aggregate(aggregation_pipeline))
    end = datetime.datetime.now() - start
    print(aggregation)
    print("Both", end.total_seconds())
    print(aggregation[0]['uniqueBrands'])
    print(aggregation[0]['uniqueVendors'])
    # results_1 = [r for r in results_1 if r is not None]
    # results_2 = [r for r in results_2 if r is not None]
    # print(aggregation[0]["uniqueBrands"].sort() == results_1.sort())
    # print(aggregation[0]["uniqueVendors"].sort() == results_2.sort())

