from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from model.abstract_everyday_product import AbstractEverydayProduct

import os
import json
import copy

with open('secret.json') as f:
    SECRET = json.load(f)

DB_URI = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db}".format(
    user=SECRET["user"],
    password=SECRET["password"],
    host=SECRET["host"],
    port=SECRET["port"],
    db=SECRET["db"])
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)


class Switchblade(AbstractEverydayProduct, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_of_product = db.Column(db.String(64))
    price_in_uah = db.Column(db.Float)
    mass_in_grams = db.Column(db.Integer)
    producing_country = db.Column(db.String(64))
    composition_of_product = db.Column(db.String(64))
    side_effects = db.Column(db.String(64))
    quantity_in_one_package = db.Column(db.Integer)

    def __init__(self, name_of_product="Default name", price_in_uah=0.0, mass_in_grams=0,
                 producing_country="country", composition_of_product="default", side_effects="no",
                 quantity_in_one_package=0, material="default"):
        super().__init__(name_of_product, price_in_uah, mass_in_grams, producing_country,
                         composition_of_product, side_effects, quantity_in_one_package)


class SwitchbladeSchema(marshmallow.Schema):
    class Meta:
        fields = ('name_of_product', 'price_in_uahgi', 'mass_in_grams', 'producing_country',
                  'composition_of_product', 'side_effects', 'quantity_in_one_package')


switchblade_schema = SwitchbladeSchema( )
switchblades_schema = SwitchbladeSchema(many=True)


@app.route("/switchblade", methods=["POST"])
def add_switchblade():
    name_of_product = request.json['name_of_product']
    price_in_uah = request.json['price_in_uah']
    mass_in_grams = request.json['mass_in_grams']
    producing_country = request.json['producing_country']
    composition_of_product = request.json['composition_of_product']
    side_effects = request.json['side_effects']
    quantity_in_one_package = request.json['quantity_in_one_package']
    switchblade = Switchblade(name_of_product, price_in_uah, mass_in_grams, producing_country,
                              composition_of_product, side_effects, quantity_in_one_package)
    db.session.add(switchblade)
    db.session.commit()
    return switchblade_schema.jsonify(switchblade)


@app.route("/switchblade/<id>", methods=["GET"])
def get_wanted_switchblade(id):
    switchblade = Switchblade.query.get(id)
    if not switchblade:
        abort(404)
    return switchblade_schema.jsonify(switchblade)


@app.route("/switchblade", methods=["GET"])
def get_switchblades():
    all_switchblades = Switchblade.query.all( )
    result = switchblades_schema.dump(all_switchblades)
    return jsonify({'switchblades': result})


@app.route("/switchblade/<id>", methods=["PUT"])
def update_switchblade(id):
    switchblade = Switchblade.query.get(id)
    if not switchblade:
        abort(404)
    old_switchblade = copy.deepcopy(switchblade)
    switchblade.name_of_product = request.json['name_of_product']
    switchblade.price_in_uah = request.json['price_in_uah']
    switchblade.mass_in_grams = request.json['mass_in_grams']
    switchblade.producing_country = request.json['producing_country']
    switchblade.composition_of_product = request.json['composition_of_product']
    switchblade.side_effects = request.json['side_effects']
    switchblade.quantity_in_one_package = request.json['quantity_in_one_package']
    db.session.commit()
    return switchblade_schema.jsonify(old_switchblade)


@app.route("/switchblade/<id>", methods=["DELETE"])
def delete_switchblade(id):
    switchblade = Switchblade.query.get(id)
    if not switchblade:
        abort(404)
    db.session.delete(switchblade)
    db.session.commit()
    return switchblade_schema.jsonify(switchblade)


@app.route("/")
def hello():
    return "<h1 style='color:black'>Hello There!</h1>"


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='0.0.0.0')

