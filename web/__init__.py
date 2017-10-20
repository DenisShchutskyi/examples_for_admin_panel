from flask import Flask,\
    request,\
    render_template,\
    redirect,\
    url_for,\
    make_response
import requests
import hashlib
import traceback
from web.config_urls import url_index,\
    url_sign_in
from web.config_api import api_sign_in,\
    api_check_valid_data_user

app = Flask(__name__)


import web.views.view_google_maps
import web.views.view_tabs
import web.views.view_statistic
import web.views.view_city


def index():
    try:
        sk = request.cookies.get('session_key')
        id_user = request.cookies.get('id_user')
        role = request.cookies.get('role')
        if sk and id_user and role:
            headers = {
                'role': role,
                'id_user': id_user,
                'session_key': sk
            }
            res = requests.get(api_check_valid_data_user, headers=headers).json()
            if res['answer'] == 'True':
                if role == 'boss':
                    resp = make_response(redirect(url_for('google_map')))

                else:
                    resp = make_response(render_template('user/firs_user.html'))
                return resp
    except:
        pass
    return redirect(url_for('sign_in'))


def sign_in():
    def create_hash_password(password):
        return hashlib.sha256(bytes(str(password), 'utf-8')).hexdigest()

    message = ''
    if request.method == 'POST':
        di = dict(request.form)
        login = di['login'][0]
        password = di['password'][0]
        data = {
            'login': login,
            'password': create_hash_password(password)
        }
        res = requests.post(api_sign_in, json=data)
        if res.json()['code'] == 1:
            head = res.headers
            if head['role'] == 'boss':
                resp = make_response(redirect(url_for('google_map')))
                resp.set_cookie('role', 'boss')
            else:
                resp = make_response(render_template('user/firs_user.html'))
                resp.set_cookie('role', 'user')
            resp.set_cookie('id_user', head['id_user'])
            resp.set_cookie('session_key', head['session_key'])
            return resp
        else:
            message = res.json()['message']
    return render_template('sign_in.html',
                           message=message)


app.add_url_rule(url_index, 'index', index)
app.add_url_rule(url_sign_in, 'sign_in', sign_in, methods=['POST', 'GET'])