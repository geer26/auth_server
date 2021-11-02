import os
import string
from random import choices
import base64
from os import getenv
from cryptography.fernet import Fernet

class Secret():

    def __init__(self, app):
        self.envfile =  os.path.join(app.config['ENV_FOLDER'], '.env')
        self.fernet = Fernet(base64.urlsafe_b64encode(getenv('FERNET_SECRET').encode('utf-8')))
        self.temp_fernet = None


    def dump(self, plain):
        return self.fernet.encrypt(str(plain).encode())


    def load(self, encoded):
        return self.fernet.decrypt(bytes(encoded, 'UTF-8')).decode(encoding='utf-8')
        #return self.fernet.decrypt(bytes(encoded)).decode(encoding='utf-8')
        #return self.fernet.decrypt(bytes(encoded))


    def new_fernet(self, secret=None, f=None):
        if not secret and f:
            self.fernet = f
        elif not f and secret:
            self.fernet = Fernet(base64.urlsafe_b64encode(secret.encode('utf-8')))
        else:
            return False
        return True


    def set_env(self, secret=None):
        filecontent = []
        with open(self.envfile, 'r') as env:
            for line in env.readlines():
                if line.startswith('FERNET_SECRET='):
                    if not secret:
                        text = f'FERNET_SECRET={self.generate_key()[1]}\n'
                    else:
                        text = f'FERNET_SECRET={secret}\n'
                    filecontent.append(text)
                    continue
                else:
                    filecontent.append(line)
                    continue

        with open(self.envfile, 'w') as env:
            for line in filecontent:
                env.write(line)

        return True


    def generate_key(self):
        new_pw = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 32))
        self.temp_fernet = Fernet(base64.urlsafe_b64encode(new_pw.encode('utf-8')))
        return new_pw