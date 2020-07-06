import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


# uncomment next line to drop all records and start db from scratch
# db_drop_and_create_all()

# Get all drinks
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    if len(drinks) == 0:
        abort(404)
    drinks_short = [drink.short() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_short
    })

# Get detailed record of all drinks
# Requires 'get:drinks-detail' permission


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    drinks = Drink.query.all()
    if len(drinks) == 0:
        abort(404)
    drinks_long = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': drinks_long
    })

# Add new drink
# Requires 'post:drinks' permission


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    body = request.get_json()
    title = body.get('title') or None
    recipe = body.get('recipe')
    if (title is None):
        abort(400)
    drink = Drink(title=title, recipe=json.dumps(recipe))
    try:
        drink.insert()
    except Exception as e:
        abort(422)
    return jsonify({
        "success": True,
        "drinks": drink.long()
    })


# Edit existing drink record
# Requires 'patch:drinks' permission
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink_by_id(*args, **kwargs):
    id = kwargs['id']
    drink = Drink.query.filter_by(id=id).one_or_none()
    if drink is None:
        abort(404)
    body = request.get_json()
    title = body.get('title') or None
    if (title is None):
        abort(400)
    if 'title' in body:
        drink.title = body['title']
    if 'recipe' in body:
        drink.recipe = json.dumps(body['recipe'])
    try:
        drink.insert()
    except Exception as e:
        abort(400)
    drink = [drink.long()]
    return jsonify({
        'success': True,
        'drinks': drink
    })


# Deleting drink record
# Requires 'delete:drinks' permission
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(*args, **kwargs):
    id = kwargs['id']
    drink = Drink.query.filter_by(id=id).one_or_none()
    if drink is None:
        abort(404)
    try:
        drink.delete()
    except Exception as e:
        abort(500)
    return jsonify({
        'success': True,
        'delete': id
    })


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
