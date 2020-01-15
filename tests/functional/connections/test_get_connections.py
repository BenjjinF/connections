from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'from_person',
    'to_person',
    'connection_type',
]


def test_can_get_connetions(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    db.session.commit()

    ConnectionFactory.create_batch(5, to_person_id=instance.id, from_person_id=None)
    ConnectionFactory.create_batch(5, to_person_id=target.id, from_person_id=None)

    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
