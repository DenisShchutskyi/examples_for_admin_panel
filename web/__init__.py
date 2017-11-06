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
    url_sign_in,\
    url_logout,\
    url_language
from web.config_api import api_sign_in,\
    api_check_valid_data_user
from function.json_read import read_json
js = read_json('translate.json')

app = Flask(__name__)


import web.views.view_google_maps
import web.views.view_tabs
import web.views.view_statistic
import web.views.view_city
import web.views.view_mail
import web.views.main_page


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
    resp = make_response(redirect(url_for('sign_in')))
    lan = request.cookies.get('language')
    if lan is None or lan == 'None':
        resp.set_cookie('language', 'ru')
    return resp


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
                resp = make_response(redirect(url_for('main_page')))
                resp.set_cookie('role', 'boss')
                import random
                resp.set_cookie('id', str(random.randint))
            else:
                resp = make_response(render_template('user/firs_user.html'))
                resp.set_cookie('role', 'user')
            resp.set_cookie('id_user', head['id_user'])
            resp.set_cookie('session_key', head['session_key'])
            return resp
        else:
            message = res.json()['message']
    resp = make_response(render_template('sign_in.html',
                                         message=message,
                                         js=js))
    # lan = request.cookies.get('language')
    # if lan is None or lan == 'None':
    #     resp.set_cookie('language', 'ru')
    return resp


def logout():
    resp = make_response(redirect(url_for('sign_in')))
    resp.set_cookie('session_key', '')
    resp.set_cookie('id_user', '')
    resp.set_cookie('role','')
    return resp


def language(lan):
    resp = make_response(redirect(url_for('sign_in')))
    if lan == 'ru' or lan == 'en':
        resp.set_cookie('language', lan)
    else:
        resp.set_cookie('language', 'ru')
    return resp

@app.errorhandler(404)
def page_not_found(e):
    return render_template('boss/404.html'), 404


app.add_url_rule(url_index, 'index', index)
app.add_url_rule(url_sign_in, 'sign_in', sign_in, methods=['POST', 'GET'])
app.add_url_rule(url_logout, 'logout', logout)
app.add_url_rule(url_language+'/<lan>', 'language', language)
