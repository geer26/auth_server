from datetime import datetime, timedelta
import json

class Sess():

    def __init__(self, app, timeout=3600):
        self.app = app
        self.sessionlist = []
        self.timeout = timeout


    def remove_from_list(self, session):
        self.sessionlist.remove(session)
        return True


    def add_to_list(self, session):
        session['expiration'] = datetime.now() + timedelta(seconds=self.timeout)
        self.sessionlist.append(str(session['_id']))
        return True


    def check_on_list(self, session):
        if session in self.sessionlist:
            return True
        return False


    def check_expired(self, session):
        if 'expiration' not in session.keys():
            return False
        if datetime.now() > session['expiration']:
            return False
        else:
            return True


    def update_expiration(self, session):
        session['expiration'] = datetime.now() + timedelta(seconds=self.timeout)
        return True


    def get_users(self):
        pass


    def renew_timeout(self, session):
        pass


    def return_all(self):
        return json.dumps(self.sessionlist)


