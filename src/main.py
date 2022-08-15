"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, UserFavourite, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_all_people():
    peoples = Character.query.all()
    people_json = []
    for people in peoples:
        people_json.append(people.serialize())
    return jsonify(people_json), 200

@app.route('/people/<id>', methods=['GET'])
def get_people(id):
    peoples = Character.query.get(id)
    return jsonify(peoples.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planet():
    planets = Planet.query.all()
    planet_json = []
    for planet in planets:
        planet_json.append(planet.serialize())
    return jsonify(planet_json), 200

@app.route('/planets/<id>', methods=['GET'])
def get_planet(id):
    planets = Planet.query.get(id)
    return jsonify(planets.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    user_json = []
    for user in users:
        user_json.append(user.serialize())
    return jsonify(user_json), 200

@app.route('/users/favourites', methods=['GET'])
def get_all_favourite():
    favourites = UserFavourite.query.all()
    favourite_json = []
    for favourite in favourites:
        favourite_json.append(favourite.serialize())
    return jsonify(favourite_json), 200

@app.route('/favourite/planet/<id>', methods=['POST'])
def post_favourite_planet():
    body = request.get_json()
    favourite_planet = Planet(name=body['name'], id=body['id'])
    db.session.add(favourite_planet)
    db.session.commit()
    return jsonify(favourite_planet.serialize()), 201

@app.route('/favourite/people/<id>', methods=['POST'])
def post_favourite_people():
    body = request.get_json()
    favourite_people = Character(name=body['name'], id=body['id'])
    db.session.add(favourite_people)
    db.session.commit()
    return jsonify(favourite_people.serialize()), 201

@app.route('/favourite/planet/<id_planet>', methods=['DELETE'])
def delete_planet(id_planet):
    favourite_planet = UserFavourite.query.get(id_planet)
    db.session.delete(favourite_planet)
    db.session.commit()
    return jsonify(favourite_planet.serialize()), 200

@app.route('/favourite/peoples/<id_character>', methods=['DELETE'])
def delete_people(id_character):
    favourite_people = UserFavourite.query.get(id_character)
    db.session.delete(favourite_people)
    db.session.commit()
    return jsonify(favourite_people.serialize()), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
