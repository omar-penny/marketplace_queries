catalog_id = "penny-cat-1038"


def filter_options_aggregation():
    """
    Changes: Initial match query is the same, but two unwind stages and a group stage were added
    Some categories return null in the list of brands/suppliers -> preserveNullAndEmptyArrays: False
    """
    category = "penny-ctg-9505"

    pipeline = [{
        "$match": {
            "catalogs.id": catalog_id,
            "$or": [
                {
                    "categories.path": {
                        "$regex": f",{category},"
                    },
                },
                {
                    "categories.id": category,
                },
            ],
            "status": "ACTIVE",
        },

        "$unwind": {
            "path": "$vendors",
            "preserveNullAndEmptyArrays": False
        },

        "$group": {
            "_id": None,
            "uniqueBrands": {"$addToSet": "$details.brand"},
            "uniqueVendors": {"$addToSet": "$vendors.connection.name"}
        }
    }]

    return pipeline


def autocomplete(name: str):
    """
    Changes: searching for term in description was removed
    Special characters to be replaced with whitespace: "@", ":" and "-"
    """
    return [
        {
            "$search": {
                "compound": {
                    "should": [
                        {
                            "autocomplete": {
                                "path": 'name.en',
                                "query": name,
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 3},
                                "score": {"boost": {"value": 2}},
                            }
                        },
                        {
                            "autocomplete": {
                                "path": 'details.sku',
                                "query": name,
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 3},
                                "score": {"boost": {"value": 3}},
                            }
                        },
                        {
                            "autocomplete": {
                                "path": 'details.brand',
                                "query": name,
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 3},
                                "score": {"boost": {"value": 2}},
                            }
                        },
                    ],
                },
            },

            "$match": {
                "status": "ACTIVE",
                "catalogs.id": catalog_id,
                "details.isAvailable": True,
            },

            "$project": {
                "id": 1,
                "name": 1,
                "details.sku": 1,
                "mediaList": 1,
            },

            "$limit": 5
        }
    ]


def main_search(name: str):
    """
    Changes: sad violin music
    """
    page = 0
    limit = 20

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

            "$skip": page * limit,

            "$limit": limit,

            "$match": {
                "status": "ACTIVE",
                "catalogs.id": catalog_id,
                "details.isAvailable": True,
            },

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
                "score": {"$meta": "searchScore"},
            },
        }
    ]


def filter_options_search(name: str):
    pipeline = [{
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

        "$unwind": {
            "path": "$details.brand",
            "preserveNullAndEmptyArrays": False
        },

        # "$unwind": {
        #     "path": "$vendors",
        #     "preserveNullAndEmptyArrays": False
        # },

        "$group": {
            "_id": None,
            "uniqueBrands": {"$addToSet": "$details.brand"},
            "uniqueVendors": {"$addToSet": "$vendors.connection.name"}
        }
    }]

    return pipeline
