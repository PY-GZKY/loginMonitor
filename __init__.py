'''
celery -A tasks beat -l INFO
celery -A tasks worker -l INFO -c 2
'''