from web.__init__ import app
from flask import render_template
import requests


def main_page():
    return render_template('boss/layout_boss.html')

app.add_url_rule('/home', 'main_page', main_page)
