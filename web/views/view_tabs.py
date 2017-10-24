from web.__init__ import app
from flask import render_template

from web.config_urls import url_tabs,\
    url_popup,\
    url_open_box


def tabs():
    return render_template('boss/tabs.html')


def popup():
    return render_template('boss/popup.html')


def open_box():
    return render_template('boss/opened_box.html')


app.add_url_rule(url_tabs, 'tabs', tabs)
app.add_url_rule(url_popup, 'popup', popup)
app.add_url_rule(url_open_box, 'box', open_box)
