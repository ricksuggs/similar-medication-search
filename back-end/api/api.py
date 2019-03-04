from flask import Flask, request, jsonify
from fuzzywuzzy import process
import requests
import requests_cache
import json
import logging
import urllib.parse
import typing
import itertools
from operator import itemgetter
from . import db

logging.basicConfig(level=logging.DEBUG)
requests_cache.install_cache("rxnorm_api_cache", expire_after=24 * 60 * 60)
# initializes the popular searches sqlite db
conn_init = db.get_connection()  # type: dataset.dataset.Database

app = Flask(__name__)
app.debug = False


DISPLAYNAMES_URL = "https://rxnav.nlm.nih.gov/REST/displaynames.json"
SIMILAR_URL = "https://rxnav.nlm.nih.gov/REST/rxcui/{0}/related.json"
DRUGS_NAME_URL = "https://rxnav.nlm.nih.gov/REST/drugs.json"


@app.route("/api/popular_searches")
def popular_searches() -> str:
    return jsonify(db.get_popular_searches())


@app.route("/api/search_drugs")
def search_drugs() -> str:
    search_text = request.args.get("search_text").lower()

    displaynames_response = requests.get(DISPLAYNAMES_URL)
    candidates = (
        displaynames_response.json().get("displayTermsList", []).get("term", [])
    )  # type: List[str]

    # initially filter the list by matching the first character
    candidates = [
        candidate for candidate in candidates if candidate.startswith(search_text[0])
    ]

    # additionally filter the list with fuzzy string matching to the top 100 results
    fuzzy_matches = process.extract(search_text, candidates, limit=100)
    return jsonify(fuzzy_matches)


@app.route("/api/similar_drugs")
def similar_drugs() -> str:
    name = request.args.get("name")

    db.update_popular_searches(name)

    # send request to the "drugs" endpoint to get the cui
    drugs_name_response = requests.get(DRUGS_NAME_URL, {"name": name})
    concept_group = get_concept_group(drugs_name_response.json(), "drugGroup")
    rxcuis = get_concept_property(concept_group, "rxcui")

    api_response = set()
    # for this prototype limit the requests to 10 for 'IN'
    for rxcui in itertools.islice(rxcuis, 0, 10):

        # initial 'IN' related response
        in_concept_response = requests.get(SIMILAR_URL.format(rxcui), {"tty": "IN"})
        concept_group = get_concept_group(in_concept_response.json(), "relatedGroup")

        # use 'IN' response to get SBD and SCD related responses
        inner_rxcuis = get_concept_property(concept_group, "rxcui")

        # for this prototype limit the requests to 10 for 'SBD+SCD'
        for inner_rxcui in itertools.islice(inner_rxcuis, 0, 10):
            query_params = f'tty={urllib.parse.quote("SBD+SCD", safe=" /+")}'
            sbd_scd_concept_response = requests.get(
                SIMILAR_URL.format(inner_rxcui), query_params
            )
            concept_group = get_concept_group(
                sbd_scd_concept_response.json(), "relatedGroup"
            )
            api_response.update(get_concept_property(concept_group, "name"))

    api_response = sorted(api_response)
    return jsonify([{"name": name} for name in api_response])


def get_concept_group(response_json: dict, parent_key: str) -> list:
    return response_json.get(parent_key, {}).get("conceptGroup", [])


def get_concept_property(concept_group: typing.List[dict], property_name: str) -> set:
    result = set()
    for concept in concept_group:
        for concept_property in concept.get("conceptProperties", []):
            result.add(concept_property.get(property_name))
    return result
