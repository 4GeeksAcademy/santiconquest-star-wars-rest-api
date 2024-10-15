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
from models import db, User, Personajes, Planetas, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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
    
    all_users = User.query.all()
    results = list(map(lambda usuario:usuario.serialize(),all_users))
    
    return jsonify(results), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    
    all_favorites = Favorites.query.filter_by(user_id=user_id).all()
    results4 = list(map(lambda favorite:favorite.serialize(),all_favorites))
    
    return jsonify(results4), 200

@app.route('/people', methods=['GET'])
def get_characters():
    
    all_characters = Personajes.query.all()
    result2 = list(map(lambda character:character.serialize(),all_characters))

    return jsonify(result2), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    
    all_planets = Planetas.query.all()
    result3 = list(map(lambda planet:planet.serialize(),all_planets))

    return jsonify(result3), 200


@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['POST'])
def add_favorite_character(user_id,people_id):
    if not user_id or not people_id or user_id=="" or people_id=="":
        return jsonify({"error": "user_id and people_id are required"}),400
    new_favorite = Favorites(user_id=user_id, personaje_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body={
        "msg": "Se creo el nuevo favorito"
    }

    return jsonify(response_body), 200

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id,planet_id):
    if not user_id or not planet_id or user_id=="" or planet_id=="":
        return jsonify({"error": "user_id and planet_id are required"}),400
    new_favorite = Favorites(user_id=user_id, planetas_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_body={
        "msg": "Se creo el nuevo favorito"
    }

    return jsonify(response_body), 200



 
@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    
    personaje=Personajes.query.get(people_id)

    return jsonify(personaje.serialize()), 200

@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(user_id,people_id):
    #Quiero filtrar el user de mi tabla con el que recibo de postman(linea 119)
    favorite=Favorites.query.filter_by(user_id=user_id,personaje_id=people_id).first()
    if not favorite:
        return jsonify({"error": "favorite not found"}),404
    db.session.delete(favorite)
    db.session.commit()

    response_body={
        "msg": "Se elimino el personaje favorito"
    }

    return jsonify(response_body), 200

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id,planet_id):
    
    favorite=Favorites.query.filter_by(user_id=user_id,planetas_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "favorite not found"}),404
    db.session.delete(favorite)
    db.session.commit()

    response_body={
        "msg": "Se elimino el planeta favorito"
    }

    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    
    planeta=Planetas.query.get(planet_id)

    return jsonify(planeta.serialize()), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
