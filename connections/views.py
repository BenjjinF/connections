from http import HTTPStatus

from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.schemas import ConnectionSchema, PersonSchema
from connections.validators import options_validator

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
@use_args({
    'sort': fields.Str(validate=options_validator(['created_at', 'first_name', 'last_name'])),
    'direction': fields.Str(validate=options_validator(['ascending', 'descending']))
    }, locations=('query',))
def get_people(args):
    sort = args.get('sort', 'created_at')
    direction_map = {'ascending': 'asc', 'descending': 'desc'}
    direction = direction_map[args.get('direction', 'ascending')]

    order_by = getattr(Person, sort)
    order_by = getattr(order_by, direction)()

    people = Person.query.order_by(order_by).all()
    people_schema = PersonSchema(many=True)
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED
