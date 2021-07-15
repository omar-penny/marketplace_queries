custom = {
    "analyzer": "categorySplitter",
    "mappings": {
        "dynamic": False,
        "fields": {
            "categories": {
                "fields": {
                    "path": [
                        {"type": "string"}
                    ]
                }
            }
        }
    },

    "analyzers": [
        {
            "name": "categorySplitter",
            "charFilters": [],
            "tokenizer": {
                "type": "regexSplit",
                "pattern": "(?<=,)[^,]+(?=,)"
            },
            "tokenFilters": []
        }
    ]
}

current = {
    "mappings": {
        "dynamic": False,
        "fields": {
            "details": {
                "fields": {
                    "brand": [
                        {
                            "norms": "omit",
                            "type": "string"
                        },
                        {
                            "type": "autocomplete"
                        }
                    ],
                    "description": {
                        "norms": "omit",
                        "store": False,
                        "type": "string"
                    },
                    "sku": [
                        {
                            "analyzer": "lucene.keyword",
                            "norms": "omit",
                            "searchAnalyzer": "lucene.keyword",
                            "type": "string"
                        },
                        {
                            "foldDiacritics": False,
                            "type": "autocomplete"
                        }
                    ]
                },
                "type": "document"
            },
            "name": {
                "fields": {
                    "en": [
                        {
                            "norms": "omit",
                            "type": "string"
                        },
                        {
                            "foldDiacritics": False,
                            "tokenization": "nGram",
                            "type": "autocomplete"
                        }
                    ]
                },
                "type": "document"
            }
        }
    }
}

suggested = {
    "analyzer": "dashAutocomplete",
    "mappings": {
        "dynamic": True
    },
    "analyzers": [
        {
            "charFilters": [],
            "name": "dashAutocomplete",
            "tokenFilters": [
                {
                    "maxGram": 10,
                    "minGram": 1,
                    "type": "nGram"
                }
            ],
            "tokenizer": {
                "type": "keyword"
            }
        }
    ]
}
