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


def main_search():
    page = 0
    limit = 20
    sort, name = generate_random_inputs()
    name = "a"

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
                "catalogs.id": "penny-cat-1154",
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

            "$skip": page * limit,

            "$limit": limit,
        }
    ]


def autocomplete():
    # sort, name = generate_random_inputs()
    name = "black"

    return [
        {
            "$search": {
                "compound": {
                    "should": [
                        {
                            "autocomplete": {
                                "path": 'name.en',
                                "query": name,
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 10},
                                "score": {"boost": {"value": 2}},
                            }
                        },
                        {
                            "autocomplete": {
                                "path": 'details.sku',
                                "query": name,
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 10},
                                "score": {"boost": {"value": 3}},
                            }
                        },
                        {
                            "autocomplete": {
                                "path": 'details.brand',
                                "query": name,
                                "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 10},
                                "score": {"boost": {"value": 2}},
                            }
                        },
                        # {
                        #     "text": {
                        #         "query": name,
                        #         "path": ['details.description'],
                        #     },
                        # },
                    ],
                },
            },

            "$match": {
                "status": "ACTIVE",
                "catalogs.id": "penny-cat-1154",
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

            "$limit": 5
        }
    ]


def techSpecOptions():
    return [
        {
            "$match": {
                "status": "ACTIVE",
                "catalogs.id": "penny-cat-1154",
                "details.isAvailable": True,
                "techSpecs": {"$ne": None},

            },
        },
        {
            "$project": {
                "techSpecs": {
                    "$objectToArray": '$techSpecs',
                },
            },
        },
        {
            "$unwind": {
                "path": '$techSpecs',
            },
        },
        {
            "$group": {
                "_id": {
                    "spec": '$techSpecs.k',
                },
                "total": {
                    "$sum": 1,
                },
                "val": {
                    "$addToSet": '$techSpecs.v',
                },
            },
        },
        {
            "$sort": {
                "total": -1,
            },
        },
        {
            "$limit": 5,
        },
    ]


# def sub_categories():
#     query = {
#         "categories.path": ",penny-ctg-1191,penny-ctg-2112",
#         "status": "ACTIVE",
#         "catalogs.id": "penny-cat-1154",
#         "details.isAvailable": True,
#     }
#
#     aggregateQuery = [
# 			{ "$match": "query" },
# 			{ "$unwind": '$categories' },
# 			# ...(options?.categoryPath? [
#             query["categories.path"]: [
# 						{
# 							"$project": {
# 								# "categoryIdPath": { "$arrayElemAt": [{ "$split": ['$categories.path', ','] }, options?.categoryPath?.split(',')?.length - 1] },
# 								"categoryIdPrivate": '$categories.id',
# 							},
# 						},
# 						{
# 							"$project": {
# 								"categoryId": {
# 								    "$switch": {
# 										"branches": [
# 											{ "case": { "$eq": ['$categoryIdPath', None] }, "then": '$categoryIdPrivate' },
# 											{ "case": { "$eq": ['$categoryIdPath', ''] }, "then": '$categoryIdPrivate' },
# 											{ "case": '$categoryIdPath', "then": '$categoryIdPath' },
# 										],
# 										"default": '$categoryIdPrivate',
# 									},
# 								},
# 							},
# 						},
# 				  ]
#
# 				# : []),
# 			{
# 				"$group": {
# 					"_id": '$categoryId',
# 					// count: { $sum: 1 }, //Performance issue
# 				},
# 			},
# 		]