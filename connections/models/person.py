from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)

    connections = db.relationship('Connection', foreign_keys='Connection.from_person_id')

    def mutual_friends(self, target):
        person_friends = [
            friend.to_person_id for friend in self.connections
            if friend.connection_type.name == 'friend'
        ]
        target_friends = [
            friend.to_person_id for friend in target.connections
            if friend.connection_type.name == 'friend'
        ]
        mutual_friends = Person.query.filter(Person.id.in_([*person_friends, *target_friends]))
        return [friend for friend in mutual_friends]
