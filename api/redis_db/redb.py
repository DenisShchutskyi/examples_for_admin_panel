import redis
import traceback
import datetime

ttl_phone_in_redis = 300

r = redis.StrictRedis(host='localhost', port=6379, db=2)


def set_user_multi(id_user, session_key):
    r.lpush('user_{}'.format(id_user), session_key)
    # r.expire(session_key, 60 * 60 * 24 * 31)  # если надо ттл


def set_user_not_multi(id_user, session_key):
    r.set('user_{}'.format(id_user), session_key)
    # r.expire(session_key, 60 * 60 * 24 * 31)  # если надо ттл


def set_boss_multi(id_user, session_key):
    r.lpush('boss_{}'.format(id_user), session_key)
    # r.expire(session_key, 60 * 60 * 24 * 31)  # если надо ттл


def set_boss_not_multi(id_user, session_key):
    r.set('boss_{}'.format(id_user), session_key)
    # r.expire(session_key, 60 * 60 * 24 * 31)  # если надо ттл


def check_valid_data_multi(id_user, session_key, role):
    try:
        l = list(r.lrange('{}_{}'.format(role,id_user), 0, -1))
        # print(len(l))
        # print('___')
        for li in l:
            # print(li)
            if li.decode('utf-8') == session_key:
                return True
        return False
    except:
        traceback.print_exc()
    return False


def check_valid_data_not_multi(id_user, session_key, role):
    try:
        sk = r.get('{}_{}'.format(role, id_user))
        if sk.decode('utf-8') == session_key:
            return True
        return False
    except:
        traceback.print_exc()
    return False
