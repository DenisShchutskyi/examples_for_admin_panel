from flask import Flask


from celery import Celery
from config import path_celery

app = Flask(__name__)

from celery_.example_celery import example_celery

app.config['CELERY_BROKER_URL'] = path_celery
app.config['CELERY_RESULT_BACKEND'] = path_celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# example use celery
# example_celery.delay(arg)


def register_blueprints(app):
    from api.entry.api_entry import entry
    app.register_blueprint(entry)
    from api.city.api_city import city
    app.register_blueprint(city)
register_blueprints(app)


