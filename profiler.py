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


def run_aggregation(pipeline: list) -> list:
    products_list = []
    for agg in collection.aggregate(pipeline, allowDiskUse=True):
        products_list.append(agg)

    return products_list


if __name__ == "__main__":
    aggregation_pipeline = []
    runs = []
    query = Query().main_search()

    for stage, operations in query[0].items():
        aggregation_pipeline.append({stage: operations})

    start = datetime.datetime.now()
    aggregation = run_aggregation(aggregation_pipeline)
    runs.append({"totalCount": aggregation[0]["totalCount"]})
    aggregation = aggregation[0]["paginatedResults"]
    end = datetime.datetime.now() - start

    for i in range(0, 15):
        runs.append({
            "number": i,
            "time": end.total_seconds(),
            "score": aggregation[i]["score"],
        })

    print(runs)
