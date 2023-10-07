from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Fan, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/fans', methods = ['POST'])
@token_required
def create_fan(current_user_token):
    name = request.json['name']
    email = request.json['email']
    state = request.json['state']
    team = request.json['team']
    sport = request.json['sport']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    fan = Fan(name, email, state, team, sport, user_token = user_token )

    db.session.add(fan)
    db.session.commit()

    response = contact_schema.dump(fan)
    return jsonify(response)

@api.route('/fans', methods = ['GET'])
@token_required
def get_fan(current_user_token):
    a_user = current_user_token.token
    fans = Fan.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(fans)
    return jsonify(response)

@api.route('/fans/<id>', methods = ['GET'])
@token_required
def get_single_fan(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        fan = fan.query.get(id)
        response = contact_schema.dump(fan)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/fans/<id>', methods = ['POST','PUT'])
@token_required
def update_fan(current_user_token,id):
    fan = Fan.query.get(id) 
    fan.name = request.json['name']
    fan.email = request.json['email']
    fan.state = request.json['state']
    fan.team = request.json['team']
    fan.sport = request.json['sport']
    fan.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(fan)
    return jsonify(response)


@api.route('/fans/<id>', methods = ['DELETE'])
@token_required
def delete_fan(current_user_token, id):
    fan = Fan.query.get(id)
    db.session.delete(fan)
    db.session.commit()
    response = contact_schema.dump(fan)
    return jsonify(response)
