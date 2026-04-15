from flask import Blueprint, jsonify
from models import db, Character, Location, User
from sqlalchemy import select

api = Blueprint("api", __name__)

@api.route('/characters', methods=['GET'])
def get_characters():
    characters = db.session.scalars(select(Character)).all()
    response = [character.serialize() for character in characters]
    return jsonify(response), 200

@api.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = db.session.get(Character, character_id)
    if not character:
        return jsonify({"error": "not found"}), 404
    return jsonify(character.serialize()), 200

@api.route('/locations', methods=['GET'])
def get_locations():
    locations = db.session.scalars(select(Location)).all()
    response = [location.serialize() for location in locations]
    return jsonify(response), 200

@api.route('/locations/<int:location_id>', methods=['GET'])
def get_location(location_id):
    location = db.session.get(Location, location_id)
    if not location:
        return jsonify({"error": "not found"}), 404
    return jsonify(location.serialize()), 200

@api.route('/users', methods=['GET'])
def get_users():
    users = db.session.scalars(select(User)).all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "not found"}), 404
    
    favorites_characters = [character.serialize() for character in user.favorites_characters]
    favorites_locations = [location.serialize() for location in user.favorites_locations]

    return jsonify({
        "characters": favorites_characters,
        "locations": favorites_locations
    }), 200

@api.route('/users/<int:user_id>/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
        return jsonify({'error': 'user or character not found'}), 404
    if character in user.favorites_characters:
        return jsonify({"msg": "this character is already a favorite."}), 400

    user.favorites_characters.append(character)
    db.session.commit()

    return jsonify(user.serialize()), 200


@api.route('/users/<int:user_id>/characters/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    user = db.session.get(User, user_id)
    character = db.session.get(Character, character_id)

    if not user or not character:
        return jsonify({'error': 'user or character not found'}), 404
    if character in user.favorites_characters:
        user.favorites_characters.remove(character)

    db.session.commit()
    return jsonify({"msg": "character deleted succesfully"}), 200

@api.route('/users/<int:user_id>/locations/<int:location_id>', methods=['POST'])
def add_favorite_location(user_id, location_id):
    user = db.session.get(User, user_id)
    location = db.session.get(Location, location_id)

    if not user or not location:
        return jsonify({'error': 'user or location not found'}), 404
    if location in user.favorites_locations:
        return jsonify({"msg": "this location is already a favorite"}), 400

    user.favorites_locations.append(location)
    db.session.commit()

    return jsonify(user.serialize()), 200


@api.route('/users/<int:user_id>/locations/<int:location_id>', methods=['DELETE'])
def remove_favorite_location(user_id, location_id):
    user = db.session.get(User, user_id)
    location = db.session.get(Location, location_id)

    if not user or not location:
        return jsonify({'error': 'user or location not found'}), 404
    if location in user.favorites_locations:
        user.favorites_locations.remove(location)

    db.session.commit()
    return jsonify({"msg": "location deleted succesfully"}), 200