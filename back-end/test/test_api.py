from flask import url_for, jsonify
from mockito import mock
from api import db, api
import requests
from fuzzywuzzy import process
import json
import requests_cache


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def test_popular_searches(when, client):

    when(db).get_popular_searches().thenReturn([["test1"], ["test2"]])

    res = client.get(url_for("popular_searches"))
    assert res.json == [["test1"], ["test2"]]


def test_search_drugs(when, client):
    mock_response = MockResponse(
        {"displayTermsList": {"term": ["result1", "result2", "result3"]}}, 200
    )
    when(requests).get(...).thenReturn(mock_response)

    when(process).extract(...).thenReturn([["test3"], ["test4"]])

    res = client.get(url_for("search_drugs") + "?search_text=anything")
    assert res.json == [["test3"], ["test4"]]


def test_similar_drugs(when, client, expect):
    mock_response_1 = MockResponse(
        {
            "drugGroup": {
                "name": "alavert",
                "conceptGroup": [
                    {"tty": "BPCK"},
                    {
                        "tty": "SBD",
                        "conceptProperties": [
                            {
                                "rxcui": "997953",
                                "name": "Loratadine 10 MG Oral Tablet [Alavert]",
                                "synonym": "Alavert 10 MG Oral Tablet",
                                "tty": "SBD",
                                "language": "ENG",
                                "suppress": "N",
                                "umlscui": "C2920298",
                            }
                        ],
                    },
                ],
            }
        },
        200,
    )

    mock_response_2 = MockResponse(
        {
            "relatedGroup": {
                "rxcui": "997953",
                "termType": ["IN"],
                "conceptGroup": [
                    {
                        "tty": "IN",
                        "conceptProperties": [
                            {
                                "rxcui": "28889",
                                "name": "Loratadine",
                                "synonym": "",
                                "tty": "IN",
                                "language": "ENG",
                                "suppress": "N",
                                "umlscui": "C0065180",
                            }
                        ],
                    }
                ],
            }
        },
        200,
    )

    mock_response_3 = MockResponse(
        {
            "relatedGroup": {
                "rxcui": "28889",
                "termType": ["SCD", "SBD"],
                "conceptGroup": [
                    {
                        "tty": "SBD",
                        "conceptProperties": [
                            {
                                "rxcui": "1020126",
                                "name": "Loratadine 10 MG Oral Tablet [Loradamed]",
                                "synonym": "Loradamed 10 MG Oral Tablet",
                                "tty": "SBD",
                                "language": "ENG",
                                "suppress": "N",
                                "umlscui": "C2940265",
                            }
                        ],
                    },
                    {
                        "tty": "SCD",
                        "conceptProperties": [
                            {
                                "rxcui": "1117562",
                                "name": "24 HR Loratadine 10 MG / Pseudoephedrine sulfate 240 MG Extended Release Oral Tablet",
                                "synonym": "loratadine 10 MG / pseudoephedrine sulfate 240 MG 24 HR Extended Release Oral Tablet",
                                "tty": "SCD",
                                "language": "ENG",
                                "suppress": "N",
                                "umlscui": "C3194903",
                            }
                        ],
                    },
                ],
            }
        },
        200,
    )

    when(requests).get(api.DRUGS_NAME_URL, {"name": "alavert"}).thenReturn(
        mock_response_1
    )
    when(requests).get(api.SIMILAR_URL.format("997953"), {"tty": "IN"}).thenReturn(
        mock_response_2
    )
    when(requests).get(api.SIMILAR_URL.format("28889"), "tty=SBD+SCD").thenReturn(
        mock_response_3
    )

    expect(db).update_popular_searches("alavert")

    requests_cache.core.clear()

    res = client.get(url_for("similar_drugs") + "?name=alavert")
    assert res.json == [
        {
            "name": "24 HR Loratadine 10 MG / Pseudoephedrine sulfate 240 MG Extended Release Oral Tablet"
        },
        {"name": "Loratadine 10 MG Oral Tablet [Loradamed]"},
    ]
