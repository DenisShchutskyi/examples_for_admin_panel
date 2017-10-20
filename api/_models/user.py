import datetime
import hashlib


class User:
    login = None
    password_hash = None
    full_name = None
    mail = None
    id = None
    role = None
    session_key = None

    def __init__(self,
                 login=None,
                 password_hash=None,
                 full_name=None,
                 mail=None,
                 id_user=None):
        if login:
            self.login = login
        if password_hash:
            self.password_hash = password_hash
        if full_name:
            self.full_name = full_name
        if mail:
            self.mail = mail
        if id_user:
            self.id = id_user

    def check_user(self,
                   cur,
                   login=None,
                   password=None):
        def create_session_key(pass_word):
            return hashlib.sha256(
                bytes(str(pass_word)
                      + str(datetime.datetime.now()),
                      'utf-8')) \
                .hexdigest()

        select = ''
        if login and password:
            self.password_hash = password
            self.login = login
            select = '''
                SELECT check_boss('{}', '{}'), check_user('{}', '{}')
            '''.format(login,
                       password,
                       login,
                       password)
        elif self.login and self.password_hash:
            select = '''
                SELECT check_boss('{}', '{}'), check_user('{}', '{}')
            '''.format(self.login,
                       self.password_hash,
                       self.login,
                       self.password_hash)
        else:
            assert AttributeError

        cur.execute(select)
        res = cur.fetchone()
        if res[0] > 0:  # boss
            self.id = int(res[0])
            self.role = 'boss'
            self.session_key = create_session_key(self.password_hash)
            code = 1
        elif res[1] > 0:
            self.id = int(res[1])
            self.role = 'user'
            self.session_key = create_session_key(self.password_hash)
            code = 1
        else:
            code = -1
        return code
