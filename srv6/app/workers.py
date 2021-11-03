import json
import uuid
#from random import SystemRandom
from app import db, logger, secret
from app.models import Users, Testbatteries, Surveys, Results, Clients, Tokens


def addsu(username, password):
    for user in Users.query.all():
        if user.is_superuser:
            return False
    user = Users(username=str(username))
    user.is_superuser = True
    user.set_password(str(password))
    db.session.add(user)
    db.session.commit()
    return True


def del_user(id):

    try:
        user = Users.query.get(int(id))
        for tb in Testbatteries.query.filter_by(user_id=user.id).all():
            del_battery({'tbid':tb.id})
    except:
        return False

    db.session.delete(user)
    db.session.commit()
    return True


def add_superuser(username,password):
    user = Users(username=username)
    user.is_superuser=True
    user.set_password(str(password))
    #user.setAPIkey(generate_API(64))
    db.session.add(user)
    db.session.commit()
    return True


def add_user(data):
    try:
        user = Users(username=data['username'])
        user.is_superuser=data['is_superuser']
        user.is_enabled=data['is_enabled']
        user.set_password(str(data['password']))
        user.email = secret.dump(data['email'])
        db.session.add(user)
    except:
        return False
    db.session.commit()
    return True


def get_admindata():
    data = {}

    data['users'] = []
    for user in Users.query.all():
        #print(user.get_self_json_enc())
        data['users'].append(user.get_self_json_enc())

    data['testbatteries'] = []
    for testbattery in Testbatteries.query.all():
        data['testbatteries'].append(testbattery.get_self_json())

    data['surveys'] = []
    for survey in Surveys.query.all():
        data['surveys'].append(survey.get_self_json_enc())

    data['results'] = []
    for result in Results.query.all():
        data['results'].append(result.get_self_json())

    data['clients'] = []
    for client in Clients.query.all():
        data['clients'].append(client.get_self_json_enc())

    data['tokens'] = []
    for token in Tokens.query.all():
        data['tokens'].append(token.get_self_json())

    return json.dumps(data)


def change_key(username, request):
    new = secret.generate_key()

    for user in Users.query.all():
        user.email = secret.temp_fernet.encrypt(secret.load(user.email))

    for client in Clients.query.all():
        client.name = secret.temp_fernet.encrypt(secret.load(client.name).decode('utf-8'))
        client.email = secret.temp_fernet.encrypt(secret.load(client.email).decode('utf-8'))

    db.session.commit();

    logger.upd_log('Secret key changed!', request=request, type=9, user=username)

    secret.fernet = secret.temp_fernet
    secret.set_env(secret=new)

    return True


def add_battery(data):
    try:
        battery = Testbatteries()
        battery.short_name = str(data['short_name'])
        battery.name = str(data['name'])
        battery.description = str(data['description'])
        battery.user_id = int(data['user_id'])
        db.session.add(battery)
        db.session.commit()
    except:
        return False
    return True


def del_battery(data):
    try:
        battery = Testbatteries.query.get( int(data['tbid']) )
        for survey in Surveys.query.filter_by(testbattery_id=battery.id).all():
            data = {'sid': int(survey.id)}
            del_survey(data)
        db.session.delete(battery)
        db.session.commit()
    except:
        return False
    return True


def add_survey(data):
    try:
        survey = Surveys()
        survey.title = data['title']
        survey.is_anonymus = data['is_anonymus']
        survey.is_active = data['is_active']
        survey.email_body = secret.dump(data['email_body'])
        survey.testbattery_id = int(data['tbid'])
        db.session.add(survey)
        db.session.commit()
        print(f'Survey is anonymus: {survey.is_anonymus}')
        if survey.is_anonymus:
            token = Tokens()
            print(f'Survey id: {survey.id}')
            token.survey_id = survey.id
            token.client_id = 0
            print(f'TOKEN: {token.get_self_json()}')
            db.session.add(token)
            print('token added')
            db.session.commit()
            print('token comitted')
            result = Results()
            result.survey_id = survey.id
            print(f'RESULT: {result.get_self_json()}')
            db.session.add(token)
            db.session.commit()
        #db.session.add(survey)
        #db.session.commit()
    except:
        return False
    return True


def del_survey(data):
    try:
        survey = Surveys.query.get(int(data['sid']))
        if not survey.is_anonymus:
            for client in Clients.query.filter_by(survey_id=survey.id).all():
                del_client({'cid':client.id})
        else:
            for token in Tokens.query.filter_by(survey_id=survey.id).all():
                db.session.delete(token)
            for result in Results.query.filter_by(survey_id=survey.id).all():
                db.session.delete(result)
        db.session.delete(survey)
        db.session.commit()
    except:
        return False
    return True


def add_client(data):
    survey = Surveys.query.get(int(data['survey_id']))
    if survey.is_anonymus:
        return False
    try:
        result = Results()

        token = Tokens()
        token.survey_id = int(data['survey_id'])

        client = Clients()
        db.session.add(result)
        db.session.add(token)
        db.session.add(client)
        client.name = secret.dump(data['name'])
        client.email = secret.dump(data['email'])
        client.is_archived = data['is_archived']
        client.survey_id = int(data['survey_id'])

        db.session.commit()

        token.client_id = client.id
        client.result_id = result.id
        #result.client_id = client.id
        result.survey_id = survey.id

        db.session.commit()

    except:
        return False
    return True


def del_client(data):
    try:
        client = Clients.query.get(int(data['cid']))
        for token in Tokens.query.filter_by(client_id=client.id).all():
            del_token({'tid':token.id})
        for result in Results.query.filter_by(client_id=client.id).all():
            del_result({'rid':result.id})

        db.session.delete(client)
        db.session.commit()
    except:
        return False
    return True


def del_token(data):
    try:
        token = Tokens.query.get(data['tid'])
        db.session.delete(token)
        db.session.commit()
    except:
        return False
    return True


def del_result(data):
    try:
        token = Tokens.query.get(int(data['rid']))
        db.session.delete(token)
        db.session.commit()
    except:
        return False
    return True


def clean_database():

    return True