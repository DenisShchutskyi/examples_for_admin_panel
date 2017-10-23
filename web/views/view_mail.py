from web.__init__ import app
from flask import render_template,\
    request
from function.send_mail import send_mail
from web.config_urls import url_send_mail


def s_mail():
    if request.method == 'POST':
        di = dict(request.form)
        mail = di['mail'][0]
        message = di['message'][0]
        send_mail(mail,'example', message)
    return render_template('boss/send_mail.html')

app.add_url_rule(url_send_mail, 'send_mail', s_mail, methods=['POST', 'GET'])


