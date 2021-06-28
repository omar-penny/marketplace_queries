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


class Query:
    """
    Contains all queries that need to be profiled
    """

    def __init__(self):
        pass

    def main_search(self):
        page = 0
        limit = 20
        sort, name = generate_random_inputs()

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
                    "catalogs.id": "penny-cat-1038",
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

    def autocomplete(self):

        sort, name = generate_random_inputs()

        return [
                   {"$search": {
                       "compound": {
                           "should": [
                               {"autocomplete": {"path": 'name.en', "query": name,
                                                 "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 256}}},
                               {"autocomplete": {"path": 'details.sku', "query": name,
                                                 "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 256}}},
                               {"autocomplete": {"path": 'details.brand', "query": name,
                                                 "fuzzy": {"maxEdits": 1, "prefixLength": 3, "maxExpansions": 256}}},
                               {
                                   "text": {
                                       "query": name,
                                       "path": ['details.description'],
                                   },
                               },
                           ],
                       },
                   },
                   },
                   {"$match": {
                       "status": "ACTIVE",
                       "catalogs.id": "penny-cat-1038",
                       "details.isAvailable": True,
                   }, },
                   {
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
                   },
                   {
                       "$limit": 5,
                   },
               ],
