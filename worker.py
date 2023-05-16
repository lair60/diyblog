import os

import redis
from rq import Worker, Queue, Connection
import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diyblog.settings')
django.setup()

listen = ['high', 'default', 'low']

redis_url = os.environ.get('REDISTOGO_URL', 'rediss://red-chd69c2k728tp9f132cg:bYKxOYk2q8LI781gB82Onf0rptpgSwsU@frankfurt-redis.render.com:6379')#Modified in Instance2

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):        
        worker = Worker(map(Queue, listen))
        worker.work()