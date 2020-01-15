from http import HTTPStatus

import pytest
from tests.factories import ConnectionFactory, PersonFactory

from connections.models.connection import Connection


@pytest.fixture
def connection_fixture(db):
    to_person_id = PersonFactory()
    connection = ConnectionFactory(
        to_person_id=to_person_id.id,
        from_person_id=None
    )

    db.session.commit()

    return {
        'id': connection.id,
    }


def test_can_delete_connection(db, testapp, connection_fixture):
    connection_id = connection_fixture['id']
    res = testapp.delete(f'/connections/{connection_id}')
    assert res.status_code == HTTPStatus.NO_CONTENT
    connection = Connection.query.get(connection_id)
    assert connection is None


@pytest.mark.parametrize('field, value, error_message', [
    pytest.param('connection_id', None, 'Not a valid integer.', id='invalid connection id'),
])
def test_patch_connection_validations(db, testapp, field, value, error_message):
    res = testapp.patch(f'/connections/{value}')

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors[field]
