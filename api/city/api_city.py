from flask import Blueprint,\
    request, \
    jsonify
import datetime
import hashlib
import binascii
import os
import traceback
from api.list_api import api_get_city_by_page,\
    api_get_all_city
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
    set_user_not_multi
max_city_at_page = 40


city = Blueprint('city',
                 __name__,
                 template_folder='templates')


@city.route(api_get_all_city, methods=['GET'])
def all_city():
    try:
        conn = create_connection()
        if conn:
            try:
                select = '''
                    SELECT id_city, city_ru
                    FROM city_r
                    ORDER BY id_city ASC
                '''
                cur = conn.cursor()
                cur.execute(select)
                answer = [[r[0], r[1]] for r in cur.fetchall()]
                return jsonify({'code': 1,
                                'result': answer})
            except:
                conn.close()
                return jsonify(error_select)
        return jsonify(error_connect)

    except KeyError:
        return jsonify(error_arguments)
    except:
        traceback.print_exc()
        return jsonify(error_server)


@city.route(api_get_city_by_page, methods=['GET'])
def page_city(page):
    try:
        conn = create_connection()
        if conn:
            try:
                select = '''
                    SELECT id_city, city_ru
                    FROM city_r
                    ORDER BY id_city ASC
                    LIMIT {} offset {}
                '''.format(max_city_at_page, max_city_at_page * int(page))
                cur = conn.cursor()
                cur.execute(select)
                answer = [[r[0], r[1]] for r in cur.fetchall()]
                return jsonify({'code': 1,
                                'result': answer})
            except:
                conn.close()
                return jsonify(error_select)
        return jsonify(error_connect)

    except KeyError:
        return jsonify(error_arguments)
    except:
        traceback.print_exc()
        return jsonify(error_server)
