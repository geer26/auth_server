from datetime import datetime, timedelta

class Sess():

    def __init__(self, app, timeout=3600):
        self.app = app
        self.sessionlist = []
        self.timeout = timeout


    def remove_from_list(self, session):
        pass


    def add_to_list(self, session):
        session['expiration'] = datetime.now() + timedelta(seconds=self.timeout)
        self.list.append(session)
        return True


    def check_on_list(self, session):
        if session in self.sessionlist:
            return True
        return False


    def check_expired(self, session):
        if 'expirqtion' not in session.keys():
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


