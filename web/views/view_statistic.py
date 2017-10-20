from web.__init__ import app
from flask import render_template,\
    jsonify

from web.config_urls import url_statistic,\
    url_get_statistic


def statistic():
    return render_template('boss/statistic.html')


def get_statistic():

    series = [
        {
            'name': 'test1',
            'data': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        },
        {
            'name': 'test2',
            'data': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        }]
    categories = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return jsonify({
        'code': 1,
        'series': series,
        'categories': categories
    })

app.add_url_rule(url_statistic, 'statistic', statistic)
app.add_url_rule(url_get_statistic, 'get_stat', get_statistic, methods=['POST'])
