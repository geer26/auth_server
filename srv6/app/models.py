import json, uuid
from app import db, login, secret
import bcrypt
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(), nullable=False, default=secret.dump('nomail@all'))  # enc, updatable
    password_hash = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    settings = db.Column(db.String(), nullable=False, default='{}')  #updatable
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    last_modified_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    is_superuser = db.Column(db.Boolean, nullable=False, default=False)
    is_enabled = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'<Username: {self.username}> <is superuser:{self.is_superuser}>'

    def set_password(self, password):
        salt = bcrypt.gensalt(14)
        p_bytes = password.encode()
        pw_hash = bcrypt.hashpw(p_bytes, salt)
        self.password_hash = pw_hash.decode()
        self.salt = salt.decode()
        return True

    def check_password(self, password):
        c_password = bcrypt.hashpw(password.encode(), self.salt.encode()).decode()
        if c_password == self.password_hash:
            return True
        else:
            return False

    '''
    def setAPIkey(self, key):
        self.APIkey = key
        return True
    '''

    def get_self(self):
        return json.dumps({'ID': self.id, 'username': self.username, 'APIkey': self.APIkey,
                           'created': self.created.strftime("%m/%d/%Y, %H:%M:%S"), 'is superuser': self.is_superuser})

    def get_self_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'settings': self.settings,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'is_superuser': self.is_superuser,
            'is_enabled': self.is_enabled
        }

    def get_self_json_enc(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': str(secret.load(self.email)),
            'settings': self.settings,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'is_superuser': self.is_superuser,
            'is_enabled': self.is_enabled
        }


class Testbatteries(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    short_name = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)  #upgradable
    description = db.Column(db.String(), nullable=False)  #upgradable
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    last_modified_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    requirements = db.Column(db.String(), nullable=False, default='[]')  #upgradable
    est_time = db.Column(db.String(64))  #upgradable

    def __repr__(self):
        return f'<name: {self.name}> <description: {self.description}>'

    def get_self_json(self):
        return {
            'id': self.id,
            'short_name': self.short_name,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'user_id': self.user_id,
            'requirements': self.requirements,
            'estimated time': self.est_time
        }


class Surveys(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default='Survey title')
    description = db.Column(db.String(4096))
    is_anonymus = db.Column(db.Boolean, default=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_archived = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    last_modified_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    email_body = db.Column(db.String(), nullable=True)  # enc
    testbattery_id = db.Column(db.Integer, db.ForeignKey('testbatteries.id'))

    def __repr__(self):
        return f'<title: {self.title}> <email_body: {self.email_body}>'

    def get_self_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_anonymus': self.is_anonymus,
            'is_active': self.is_active,
            'is_archived': self.is_archived,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'email_body': self.email_body,
            'testbattery_id': self.testbattery_id
        }

    def get_self_json_enc(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_anonymus': self.is_anonymus,
            'is_active': self.is_active,
            'is_archived': self.is_archived,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'email_body': str(secret.load(self.email_body)),
            'testbattery_id': self.testbattery_id
        }


class Results(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    results = db.Column(db.String(), nullable=False, default='{}')
    status = db.Column(db.String(20), nullable=False, default='pending')
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    last_modified_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))

    def __repr__(self):
        return f'<status: {self.status}> <id: {self.id}>'

    def get_self_json(self):
        return {
            'id': self.id,
            'results': self.results,
            'status': self.status,
            'is_archived': self.is_archived,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'survey_id': self.survey_id
        }


class Clients(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(), nullable=False)  # enc
    email = db.Column(db.String(), default=secret.dump('nomail@all'))  # enc
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    last_modified_at = db.Column(db.Date(), default=datetime.now(), nullable=False)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))

    def __repr__(self):
        return f'<id: {self.id}> <name: {self.name}>'

    def get_self_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_archived': self.is_archived,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'result_id': self.result_id,
            'survey_id': self.survey_id
        }

    def get_self_json_enc(self):
        return {
            'id': self.id,
            'name': str(secret.load(self.name)),
            'email': str(secret.load(self.email)),
            'is_archived': self.is_archived,
            'created_at': self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'last_modified_at': self.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
            'result_id': self.result_id,
            'survey_id': self.survey_id
        }


class Tokens(db.Model):

    id = db.Column(db.Integer, index=True, primary_key=True)
    token = db.Column(db.String(36), nullable=False, default=str(uuid.uuid1()))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))

    def __repr__(self):
        return f'<id: {self.id}> <token: {self.token}> <client_id: {self.client_id}>'

    def get_self_json(self):
        return {
            'id': self.id,
            'token': self.token,
            'client_id': self.client_id,
            'survey_id': self.survey_id
        }
