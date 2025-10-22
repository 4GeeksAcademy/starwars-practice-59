"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, People
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import requests

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200



@api.route("/people/population", methods=["GET"])
def people_population():
    url_people = "https://www.swapi.tech/api/people?page=1&limit=10"

    response  = requests.get(url_people)
    data = response.json()

    for person in data["results"]:
        person_details = requests.get(person["url"])
        person_details = person_details.json()
        name = person_details["result"]["properties"]["name"]
        height = person_details["result"]["properties"]["height"]
        mass = person_details["result"]["properties"]["mass"]
        gender = person_details["result"]["properties"]["gender"]
        birth_year = person_details["result"]["properties"]["birth_year"]

        new_person = People(
            name=name,
            height=height,
            mass=mass,
            gender=gender,
            birth_year=birth_year
        )

        db.session.add(new_person)
        
    try:
        db.session.commit()
        return jsonify("People succesfully"), 200
    except Exception as error:
        db.session.rollback()
        return jsonify({"message": f"Error: {error}"}), 500


