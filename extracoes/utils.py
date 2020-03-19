import os
from datetime import date, datetime, timedelta

from gridfs import GridFS
from pymongo import MongoClient

today = date.today()
str_today = datetime.strftime(today, '%d/%m/%Y')
yesterday = today - timedelta(days=1)
str_yesterday = datetime.strftime(yesterday, '%d/%m/%Y')

MONGODB_URI = os.environ.get('MONGODB_URI')
if MONGODB_URI:
    DATABASE = ''.join(MONGODB_URI.rsplit('/')[-1:])
else:
    DATABASE = 'test'

conn = MongoClient(host=MONGODB_URI)
mongodb = conn[DATABASE]
fs = GridFS(mongodb)


def parse_datas(inicio, fim):
    return datetime.strptime(inicio, '%d/%m/%Y'), \
           datetime.strptime(fim + ' 23:59:59', '%d/%m/%Y %H:%M:%S')
