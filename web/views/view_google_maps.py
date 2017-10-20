from web.__init__ import app
from flask import render_template

from web.config_urls import url_map_by_address,\
    url_map_by_click


def google_map_by_address():
    return render_template('boss/google_maps.html')


def google_map_by_lat_lan():
    return render_template('boss/google_maps_2.html')


app.add_url_rule(url_map_by_address, 'google_map', google_map_by_address)
app.add_url_rule(url_map_by_click, 'google_map_lat_lan', google_map_by_lat_lan)
