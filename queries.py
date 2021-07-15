"""
Optimized: main_search, autocomplete, filter_options
@TODO: tech_spec_options, sub_categories, getProductsByQuery
"""
catalog_id = "penny-cat-1038"


def generate_random_inputs() -> (str, str):
    """
    Generating a random sort and name inputs
    """
    from random import randrange

    sort_options = [{"score": 1}, {"score": -1},
                    {"price.value": 1}, {"price.value": -1}]
    name_options = ["tools", "demolition", "grinder", "welding",
                    "rotary", "electric", "JW", "JW-00002", "impact"]

    sort = sort_options[randrange(len(sort_options))]
    name = name_options[randrange(len(name_options))]

    return sort, name


def main_search_count(name: str):
    return [
        {
            "$search": {
                "compound": {
                    "should": [
                        {
                            "phrase": {
                                "query": name,
                                "path": ["name.en", "details.brand", "details.sku", "details.description"],
                                "score": {"boost": {"value": 3}},
                            },
                        },

                        {
                            "text": {
                                "query": name,
                                "path": ["name.en", "details.brand"],
                                "score": {"boost": {"value": 2}},
                                "fuzzy": {"maxEdits": 2, "prefixLength": 0, "maxExpansions": 10},
                            },
                        },

                        {
                            "text": {
                                "query": name,
                                "path": ["details.description"],
                                "fuzzy": {"maxEdits": 2, "prefixLength": 0, "maxExpansions": 10},
                            }
                        },

                        {
                            "text": {
                                "query": name,
                                "path": ["details.sku"],
                                "fuzzy": {"maxEdits": 2, "prefixLength": 0, "maxExpansions": 10},
                                "score": {"boost": {"value": 3}},
                            }
                        },
                    ],
                }
            },

            "$match": {
                "status": "ACTIVE",
                "catalogs.id": catalog_id,
                "details.isAvailable": True,
            },

            "$count": "count"
        }
    ]


def tech_spec_options(name: str):
    query = [
        {
            "$search": {
                "compound": {
                    "should": [
                        {
                            "text": {
                                "query": name,
                                "path": ["name.en", "details.brand"],
                                "score": {"boost": {"value": 2}},
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 256},
                            },
                        },
                        {
                            "text": {
                                "query": name,
                                "path": ["details.description"],
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 256},
                            },
                        },
                        {
                            "text": {
                                "query": name,
                                "path": ["details.sku"],
                                "score": {"boost": {"value": 3}},
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 10},
                            },
                        },
                    ],
                },
            },

            "$match": {
                "techSpecs": {"$ne": None},
                "status": "ACTIVE",
                "catalogs.id": catalog_id,
                "details.isAvailable": True,
            },
            # "$limit": 1000,

            "$project": {
                "techSpecs": {
                    "$objectToArray": "$techSpecs",
                },
            },

            "$unwind": {
                "path": "$techSpecs",
            },

            "$group": {
                "_id": {
                    "spec": "$techSpecs.k",
                },
                "total": {
                    "$sum": 1,
                },
                "val": {
                    "$addToSet": "$techSpecs.v",
                },
            },

            "$sort": {
                "total": -1,
            },

            "$limit": 5
        },
    ]

    return query


def sub_categories(name: str):
    """
    Test runs:
    1. ,penny-ctg-4182,: 2.707999
    2. ,penny-ctg-1357,: 2.5ish
    3. ,penny-ctg-3330,: 2.635998
    4. ,penny-ctg-1969,: 2.60199598
    """
    match_query = [
        {
            "$match": {
                "catalogs.id": catalog_id,
                "status": "ACTIVE",
                "details.isAvailable": True,
                "categories.path": {
                    "$regex": ",penny-ctg-1357,"
                }
            },

            "$unwind": "$categories",

            "$group": {
                "_id": "$categories.id",
            },
        }
    ]

    select_query = [
        {
            "id": {"$in": []}
        },
        {
            "select": {"name": 1, "id": 1, "image": 1}
        }
    ]

    return match_query, select_query


def wildcard_search():
    return \
        [
            {
                "$search": {
                    "index": "test",
                    "wildcard": {
                        "query": "*penny-ctg-9505*",
                        "path":
                            "categories.path"
                    }
                }
            }
        ]


def category_products():
    category = "penny-ctg-9505"

    pipeline = [
        {
            "$match": {
                "status": "ACTIVE",
                "catalogs.id": catalog_id,
                "$or": [
                    {
                        "categories.path": {
                            "$regex": f",{category},"
                        }
                    },
                    {"categories.id": category}
                ],
            },

            "$limit": 25,

            "$skip": 0 * 25,

            "$project": {
                "id": 1,
                "name": 1,
                "categories": 1,
                "catalogs": 1,
                "details.description": 1,
                "details.isAvailable": 1,
                "details.brand": 1,
                "details.sku": 1,
                "details.soldBy": 1,
                "mediaList": 1,
                "price": 1,
                "vendors": 1,
            }

            # "$facet": {
            #     "paginatedResults": [
            #         {
            #             "$project": {
            #                 "id": 1,
            #                 "name": 1,
            #                 "categories": 1,
            #                 "catalogs": 1,
            #                 "details.description": 1,
            #                 "details.isAvailable": 1,
            #                 "details.brand": 1,
            #                 "details.sku": 1,
            #                 "details.soldBy": 1,
            #                 "mediaList": 1,
            #                 "price": 1,
            #                 "score": {"$meta": "searchScore"}
            #             }
            #         },
            #         {"$sort": {"score": -1}},
            #         {"$skip": 0*25},
            #         {"$limit": 25}
            #     ],
            #     "totalCount": [
            #         {
            #             "$count": 'count'
            #         }
            #     ]
            # }
        }
    ]

    return pipeline
