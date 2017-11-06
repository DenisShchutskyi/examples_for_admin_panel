from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit, rooms
import redis
import random

app = Flask(__name__)
socketio = SocketIO(app)

redis_server_socet_room = redis.StrictRedis('localhost', db=8)   

@socketio.on('connected')
def connected():
    print (request)
    print(request.sid)
    
    redis_server_socet_room.set(str(request.cookies['id']), request.sid)
    print('connect')

    
@socketio.on('disconnect')
def disconnect():
    print('disconect')
    print (request)
    redis_server_socet_room.delete(request.cookies['id'])

@app.route('/run')
def mes_to_client():
    #import pdb
    #pdb.set_trace()
    data = {"header": "переход №1", 
            "text": "перейти к табкам", 
            "group": "tabs",
            "url": '/tabs'}
    for key in redis_server_socet_room.scan_iter():
        socet_room_key = redis_server_socet_room.get(key).decode('utf-8')
        print("send data to client " + socet_room_key)
        res = socketio.emit(
        				    'message', 
        				    data,
        				    room=socet_room_key)
    data = {"header": "запрос на отправку письма", 
            "text": "отправиьт письмо ...", 
            "group": "mail",
            "url": '/send/mail'}
    for key in redis_server_socet_room.scan_iter():
        socet_room_key = redis_server_socet_room.get(key).decode('utf-8')
        print("send data to client " + socet_room_key)
        res = socketio.emit(
                            'message', 
                            data,
                            room=socet_room_key)
    return "ok"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')