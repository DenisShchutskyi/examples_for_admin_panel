from __future__ import absolute_import, unicode_literals, print_function

from kombu import Connection
import pprint
import json
import smtplib
import traceback

from config import mail as m ,\
    password

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(to, subject, text):
    try:
        # me == my email address
        # you == recipient's email address
        me = m
        you = to  # куда

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you

        # Create the body of the message (a plain-text and an HTML version).


        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        # part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        # msg.attach(part2)
        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        mail.login(m, password)
        mail.sendmail(me, you, msg.as_string())
        mail.quit()
        mail.close()
    except:
        traceback.print_exc()