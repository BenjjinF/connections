from http import HTTPStatus

import pytest
from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


@pytest.mark.xfail
def test_can_get_mutual_friends(db, testapp):
    person = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person_id=person.id, from_person_id=None)
    ConnectionFactory.create_batch(5, to_person_id=target.id, from_person_id=None)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person_id=person.id, to_person_id=f.id, connection_type='friend')
        ConnectionFactory(from_person_id=target.id, to_person_id=f.id, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person_id=person.id, to_person_id=decoy.id, connection_type='coworker')
    ConnectionFactory(from_person_id=target.id, to_person_id=decoy.id, connection_type='coworker')

    db.session.commit()

    person_res = testapp.get(f'/people/{person.id}/mutual_friends?target_id={target.id}')
    assert person_res.status_code == HTTPStatus.OK
    assert len(person_res.json) == 3
    for person in person_res.json:
        for field in EXPECTED_FIELDS:
            assert field in person
    person_mutual_friends = [f.id for f in person_res.json]

    target_res = testapp.get(f'/people/{target.id}/mutual_friends?target_id={person.id}')
    target_mutual_friends = [f.id for f in target_res.json]

    assert person_mutual_friends == target_mutual_friends
