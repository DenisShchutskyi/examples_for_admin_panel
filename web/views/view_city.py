from web.__init__ import app
from flask import render_template,\
    jsonify

from web.config_urls import url_cites,\
    url_page_city,\
    url_find_in_select,\
    url_find_in_select_multi
from web.config_api import api_get_all_city,\
    api_get_city_by_page
import requests


def to_city():
    return render_template('boss/city_infinity.html', url_page=url_page_city)


def city_page(page):
    res = requests.get(api_get_city_by_page.format(page)).json()['result']
    return jsonify({'data': res})


def find_city():
    res = requests.get(api_get_all_city).json()['result']
    return render_template('boss/find_in_select.html', cites=res)


def multi_select_with_find():
    res0 = requests.get(api_get_city_by_page.format(0)).json()['result']
    res1 = requests.get(api_get_city_by_page.format(1)).json()['result']
    res_p = res0 + res1
    return render_template('boss/multi_select.html',
                           cites=res_p)


app.add_url_rule(url_cites, 'cites_inf', to_city)
app.add_url_rule(url_page_city + '/<page>',
                 'city_page',
                 city_page,
                 methods=['GET'])
app.add_url_rule(url_find_in_select, 'find_city', find_city)
app.add_url_rule(url_find_in_select_multi, 'multi_find', multi_select_with_find)
