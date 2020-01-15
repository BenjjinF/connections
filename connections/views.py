from http import HTTPStatus

from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args

from connections.models.connection import Connection, ConnectionType
from connections.models.person import Person
from connections.schemas import ConnectionSchema, NestedConnectionSchema, PersonSchema
from connections.validators import enum_validator

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connection_schema = NestedConnectionSchema(many=True)
    connections = Connection.query.all()
    return connection_schema.jsonify(connections), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections/<connection_id>', methods=['PATCH'])
@use_args({
    'connection_id': fields.Int(location='view_args', required=True),
    'connection_type': fields.Str(
        location='json',
        required=True,
        validate=enum_validator(ConnectionType)
    )
})
def patch_connection(connection, connection_id):
    existing_connection = Connection.query.get(connection_id)
    if existing_connection:
        existing_connection.connection_type = connection.get('connection_type')
        existing_connection.update()
        return ConnectionSchema().jsonify(existing_connection), HTTPStatus.OK
    else:
        return jsonify({'description': 'Connection does not exist'}), HTTPStatus.NOT_FOUND

