from pymongo import MongoClient
from dotenv import load_dotenv
from queries import autocomplete, main_search, techSpecOptions, techSpecOptionsThroughIds
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


def aggregate_query(query: str, x=False):
    aggregation_pipeline = []

    # for stage, operations in query[0].items():
    #     print(stage)
    #     if not x:
    #         if stage != "$skip" and stage != "$limit":
    #             aggregation_pipeline.append({stage: operations})

    if not x:
        for stage, operations in query[0].items():
            print(stage)
            if stage != "$skip" and stage != "$limit":
                aggregation_pipeline.append({stage: operations})

    if x:
        for stage, operations in query[0].items():
            print(stage)
            aggregation_pipeline.append({stage: operations})

    start = datetime.datetime.now()
    aggregation = list(collection.aggregate(aggregation_pipeline))
    end = datetime.datetime.now() - start

    return aggregation, end


if __name__ == "__main__":
    aggregation_pipeline = []
    runs = []
    query = main_search("pipe")
    aggregation, run_time = aggregate_query(query)

    product_ids = [doc["id"] for doc in aggregation]
    query = techSpecOptionsThroughIds(product_ids[:1001])
    aggregation, run_time = aggregate_query(query, True)

    print(len(product_ids))
    for i in range(0, len(aggregation)):
        runs.append({
            "number": i,
            "time": run_time.total_seconds(),
            "size": len(aggregation[i]["val"]),
            # "ID": aggregation[i]["id"],
            "val": aggregation[i]["val"],
            # "name[en]": aggregation[i]["name"]["en"],
            # "sku": aggregation[i]["details"]["sku"],
            # "description": aggregation[i]["details"]["description"],
            # "brand": aggregation[i]["details"]["brand"],
            # "specs": aggregation[i]["techSpecs"],
            # "score": aggregation[i]["score"],
        })

    for i in runs:
        print(i)
#
