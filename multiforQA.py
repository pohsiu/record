import multiprocessing
import sys
import os
import Queue

import MySQLdb
import xlwt
from BeautifulSoup import BeautifulSoup
import time
import requests


DEBUG = False

MAX_ALL_RATINGS = 1000
N_PROCESS = 20


def _get_link_page(linkurl):
	if not linkurl:
		return u''
	try:
		r = requests.get(linkurl)
		r_html= r.text.encode('utf8')
		soup = BeautifulSoup(r_html)

		return soup
	except Exception, e:
		return u''


class ScopeLock(object):
	def __init__(self, lock):
		self._lock = lock

	def __enter__(self):
		self._lock.acquire()

	def __exit__(self, type, value, traceback):
		self._lock.release()


def _do_parse_url(lock, queue, s_all_ratings, s_active_workers, has_increased_active_workers):
	while True:
		msg = ('pid=%d: queue.get() (#=%df), all_ratings=%d\n'
				'' % (os.getpid(), queue.qsize(), len(s_all_ratings)))
		sys.stderr.write(msg)
		url = queue.get()
		msg = 'pid=%d: url=%s\n' % (os.getpid(), url)
		sys.stderr.write(msg)
		if url is None:
			break

		with ScopLock(lock):
			s_active_workers.value += 1
			has_increased_active_workers = True

		rootsoup = _get_link_page(url)
		


def _parse_url(lock, queue, s_all_ratings, s_active_workers):
	has_increased_active_workers = False
	try:
		_do_parse_url(lock, queue, s_all_ratings, s_active_workers, has_increased_active_workers)
	except Exception, e:
		pass
	if has_increased_active_workers:
		# Must reset the state or the main process won't stop.
		with ScopLock(lock):
			s_active_workers.value -= 1


def _put_links(queue, links):
	for link in links:
		msg = 'pid=%d: put link=%s\n' % (os.getpid(), link)
		sys.stderr.write(msg)
		queue.put(link)

def get_in_parallel(links):
	manager = multiprocessing.Manager()
	lock = manager.Lock()
	all_ratings = manager.dict()
	active_workers = manager.Value('i', 0)
	queue = manager.Queue()

	init_producer = multiprocessing.Process(targer=_put_links,args=(queue, links))
	init_producer.start()

	#start workers
	process = []
	for i in xrange(N_PROCESS):
		args = (lock, queue, all_ratings, active_workers)
		p = multiprocessing.Process(target=_parse_url, args=args)
		p.start
		processes.append(p)






if __name__ == '__main__':
	seed_urls = [
	'https://play.google.com/store/apps/details?id=com.cloudmosa.puffinFree&hl=en'
	]

	all_ratings = get_in_parallel(seed_urls)
	for url, value in all_ratings.items():
		app_name, ratings = value
		ss = [app_name, url] + map(str, ratings)
		print (u'\t'.join(ss)).encode('utf8')