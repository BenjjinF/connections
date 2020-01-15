from http import HTTPStatus

import pytest
from tests.factories import ConnectionFactory, PersonFactory


@pytest.fixture
def ids_fixture(db):
    from_person = PersonFactory(first_name='Diana')
    to_person = PersonFactory(first_name='Harry')
    db.session.commit()

    connection = ConnectionFactory(
        to_person_id=to_person.id,
        from_person_id=from_person.id,
    )
    db.session.commit()

    return {
        'from_person': from_person.id,
        'to_person': to_person.id,
        'connection': connection.id,
    }


def test_can_patch_connection(db, testapp, ids_fixture):
    payload = {
        'connection_type': 'mother',
    }
    connection_id = ids_fixture['connection']
    res = testapp.patch(f'/connections/{connection_id}', json=payload)
    assert res.status_code == HTTPStatus.OK

    patched_connection = res.json
    assert patched_connection is not None

    assert patched_connection['from_person_id'] == ids_fixture['from_person']
    assert patched_connection['to_person_id'] == ids_fixture['to_person']
    assert patched_connection['connection_type'] == 'mother'


@pytest.mark.parametrize('field, value, error_message', [
    pytest.param(
        'connection_type',
        'friendz',
        'The value `friendz` is not a valid option.',
        id='invalid type'
    ),
    pytest.param('connection_type', None, 'Field may not be null.', id='missing type'),
])
def test_patch_connection_validations(db, testapp, ids_fixture, field, value, error_message):
    payload = {
        'connection_type': 'mother'
    }
    payload[field] = value

    connection_id = ids_fixture['connection']
    res = testapp.patch(f'/connections/{connection_id}', json=payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors[field]
