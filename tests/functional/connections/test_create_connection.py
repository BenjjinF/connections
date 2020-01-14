from http import HTTPStatus

import pytest
from tests.factories import PersonFactory

from connections.models.connection import Connection


@pytest.fixture
def connection_payload(db):
    person_from = PersonFactory(first_name='Diana')
    person_to = PersonFactory(first_name='Harry')
    db.session.commit()
    return {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'mother',
    }


def test_can_create_connection(db, testapp, connection_payload):

    res = testapp.post('/connections', json=connection_payload)

    assert res.status_code == HTTPStatus.CREATED

    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == connection_payload['from_person_id']
    assert connection.to_person_id == connection_payload['to_person_id']
    assert connection.connection_type.value == 'mother'


@pytest.mark.parametrize('field, value, error_message', [
    pytest.param('from_person_id', None, 'Field may not be null.', id='missing from person'),
    pytest.param('to_person_id', 'Diane', 'Not a valid integer.', id='incorrect from person'),
    pytest.param('to_person_id', None, 'Field may not be null.', id='missing to person'),
    pytest.param('to_person_id', 'Harry', 'Not a valid integer.', id='incorrect to person'),
    pytest.param('connection_type', None, 'Field may not be null.', id='missing type'),
    pytest.param('connection_type', 'friendz', 'Invalid enum member friendz', id='incorrect type'),
])
def test_create_connection_validations(
        db, testapp, connection_payload, field, value, error_message):
    connection_payload[field] = value

    res = testapp.post('/connections', json=connection_payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors[field]
