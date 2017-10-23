from api import celery


message_news_admin = {
    'title': 'Новость',
    'body': 'news',
    'code_': 3,
    'id_ ': 0,
}


@celery.task
def example_celery(arg):
    pass