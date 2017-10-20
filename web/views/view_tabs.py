from web.__init__ import app
from flask import render_template

from web.config_urls import url_tabs


def tabs():
    return render_template('boss/tabs.html')


app.add_url_rule(url_tabs, 'tabs', tabs)
