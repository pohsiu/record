from multiprocessing import Process, Pool
import time
import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import xlwt
import random


def millis():
  return int(round(time.time() * 1000))

def http_get(url):
  r = requests.get(url)
  r_html= r.text.encode('utf8')
  soup = BeautifulSoup(r_html)
  return soup



db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')
cursor = db.cursor()

cursor.execute("SELECT Asin, QAUrl FROM product where QAUrl !=''")
row = cursor.fetchall()

print row[1]


if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
