from flask import Blueprint,\
    request, \
    jsonify
import datetime
import hashlib
import binascii
import os
import traceback
from api.list_api import api_sign_in,\
    api_check_valid_data_user
from api._models.user import User
from api._api_answers import error_arguments,\
    error_server,\
    error_select,\
    error_connect,\
    not_valid_data_entry,\
    good_sign_in
from api.config_api import create_connection
from api.redis_db.redb import set_boss_multi,\
    set_boss_not_multi,\
    set_user_multi,\
    set_user_not_multi,\
    check_valid_data_not_multi,\
    check_valid_data_multi


entry = Blueprint('entry',
                  __name__,
                  template_folder='templates')


@entry.route(api_sign_in, methods=['POST'])
def sign_in_():
    try:
        login = request.json['login']
        password = request.json['password']
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                user = User(login=login, password_hash=password)
                ans = user.check_user(cur)
                if ans < 0:
                    return jsonify(not_valid_data_entry)
                else:
                    if user.role == 'user':
                        set_user_not_multi(user.id, user.session_key)
                    else:
                        set_boss_not_multi(user.id, user.session_key)
                    answer = jsonify(good_sign_in)
                    answer.headers.extend({
                        'id_user': str(user.id),
                        'session_key': str(user.session_key),
                        'role': str(user.role)
                    })
                    return answer
            except:
                conn.close()
                return jsonify(error_select)
        return jsonify(error_connect)

    except KeyError:
        return jsonify(error_arguments)
    except:
        traceback.print_exc()
        return jsonify(error_server)


@entry.route(api_check_valid_data_user, methods=['GET'])
def check_valid_data_user():
    try:
        role = request.headers['role']
        id_user = request.headers['id_user']
        session_key = request.headers['session_key']
        return jsonify(
            {
                'answer': str(check_valid_data_not_multi(id_user, session_key, role))
            })
    except KeyError:
        return jsonify({
                'answer': str(False)
            })
    except:
        traceback.print_exc()
        return jsonify({
                'answer': str(False)
            })