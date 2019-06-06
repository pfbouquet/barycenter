from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(256))
    address_1 = db.Column(db.String(100))
    address_2 = db.Column(db.String(100))

    __tablename__ = "user"
    __table_args__ = {"schema": "coding_night"}

    def __repr__(self):
        return f'<User {self.id}: {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Group(db.Model):

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    creator = db.Column(db.String(50))

    __tablename__ = "group"
    __table_args__ = {"schema": "coding_night"}

    def __repr__(self):
        return f'<Group "{self.name}" from user {self.creator}>'

    def __init__(self, name, creator):
        self.id = generate_password_hash(f'{creator}{datetime.now()}')[-50:]
        self.name = name
        self.creator = creator


class Member(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    group_id = db.Column(db.String(50), db.ForeignKey(Group.id))

    __tablename__ = "member"
    __table_args__ = {"schema": "coding_night"}

    def __repr__(self):
        return f'<Member {self.user_id} from group {self.group_id}>'
