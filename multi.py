import multiprocessing
import multiprocessing.pool
from multiprocessing import Pool,Process
import time
import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import xlwt
import random

global quotient
#===pri===
global asker
global question
global askdate
#===pri===
#===sub===
global answerDate
global answer
global author
global vote
#===sub===

start = time.ctime()

class NoDaemonProcess(multiprocessing.Process):
	def _get_daemon(self):
		return False
	def _set_daemon(self,value):
		pass
	daemon = property(_get_daemon, _set_daemon)

class MyPool(multiprocessing.pool.Pool):
	Process = NoDaemonProcess

def http_get(urls):
	#print "test"
	numberofQ = None  
  	protect_timeout = 0
  	#keep repeating request until getting the data
  	while numberofQ is None:
		protect_timeout = protect_timeout + 1
		time.sleep(random.randint(3,8))
		if protect_timeout > 20:
			break
		try:
			r = requests.get(urls)
			r_html= r.text.encode('utf8')
			soup = BeautifulSoup(r_html)
			numberofQ = soup.find('div',{'class':'a-fixed-left-grid-col askPaginationHeaderMessage a-col-left'},{'style':'width:250px;margin-left:-250px;_margin-left:-125px;float:left;'}).text.encode('utf8').split('of ')[1].split(' q')[0]
		except:
			pass
		r.close()
	if soup:
		find(soup)

def find(soup):
	#print "test2"
	numberofQ = soup.find('div',{'class':'a-fixed-left-grid-col askPaginationHeaderMessage a-col-left'},{'style':'width:250px;margin-left:-250px;_margin-left:-125px;float:left;'}).text.encode('utf8').split('of ')[1].split(' q')[0]
	num = int(numberofQ)
	#convert questions to int, calculate the pages of questions
	last = num%10
	global quotient
	quotient = num/10
	if quotient is 0:
		last = 0
	if last > 0:
		quotient = quotient + 1
	mylist=[]
	questions = soup.findAll('div',{'class':'a-fixed-left-grid-col a-col-right'},{'style':'padding-left:0%;*width:99.6%;float:left;'})
	for run in questions:  
		nestedQ = run.find('a',{'class':'a-link-normal'})
		if nestedQ is not None:
			if not nestedQ['href'] in mylist:
				if '/help' not in nestedQ['href']:
					mylist.append(nestedQ['href'])
	
	listURL = mylist
	sub_pool = MyPool(5)
	sub_pool.map(eachQuestion,listURL)


def eachAnswer(each):
	print "test4"
	#===pri===
	global asker
	global question
	global askdate
	#===pri===
	#===sub===
	global answerDate
	global answer
	global author
	global vote
	#===sub===
	subAnswer = each.find('span',{'style':'display:block'})
	if subAnswer.text.encode('utf8') is '':
		xcode = subAnswer['id'].split('_')[1]
		subAnswer = each.find('span',{'id':'long_'+xcode})
		answer = subAnswer.text.encode('utf8')
	else: 
		answer = subAnswer.text.encode('utf8')
	Authordata = each.find('div',{'class':'answerAuthor'})
	if Authordata is not None:
		Authordata = Authordata.text.encode('utf8').split('answered on ')
		author = Authordata[0]
		answerDate = Authordata[1].split('&')[0]
	voteinfo = each.find('span',{'class':'votingInfo'})
	if voteinfo is not None:
		vote = voteinfo.text.encode('utf8')[0]#.split('.')[0]
	if vote is 'D':
		vote = '0'
	print "----------------"
	print "Question:"+question
	print "Answer:"+answer
	print vote
	print "Writer:"+author
	print "AnswerDate:"+answerDate
	print "Asker:"+asker
	print "AskDate:"+askdate
	print askerData


def eachQuestion(listURL):
	#print "test3"
	#===pri===
	global asker
	global question
	global askdate
	#===pri===
	
	#===pri===
	asker = ''
	question= ''
	askdate= ''
	#===pri===
	
	#print listURL
	try:
		sub_r = requests.get("http://www.amazon.com"+listURL)
	except requests.exceptions.ConnectionError:
		sub_r.status_code = "Connection Refused"

	subr_html= sub_r.text.encode('utf8')
	sub_soup = BeautifulSoup(subr_html)
	#get each quesion & answer info.
	question = sub_soup.find('meta',{'name':'title'})
	if question is not None:
		question = question['content'].split('Answers: ')[1].encode('utf8')

		askerData = sub_soup.find('div',{'class':'cdAuthorInfoBlock'}).text.encode('utf8').split('asked by')[1].split('on ')
		asker = askerData[len(askerData)-2]
		askdate = askerData[len(askerData)-1]

		answers = sub_soup.findAll('div',{'class':'cdMessageInfo'})
		try:
			print "Question:"+question
		except:
			pass
		sub_r.close()
		#sub_pool = Pool(processes=1)
		#sub_pool.map(eachAnswer,answers)
		

			




if __name__ == '__main__':

	db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')
	cursor = db.cursor()

	cursor.execute("SELECT Asin, QAUrl FROM product where QAUrl !=''")
	row = cursor.fetchall()

	asins = []
	urls = []
	for rows in row:
		asins.append(rows[0])
		urls.append(rows[1])
	#print urls
	pool = MyPool(3)
	pool.map(http_get,urls)
	print "Start : %s" % start      
	print "End : %s" % time.ctime() 
	    

	




