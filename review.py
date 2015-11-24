import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import time
import xlwt
import random

start = time.ctime()

book = xlwt.Workbook(encoding="utf-8")

sheet = book.add_sheet("python sheet")
sheet.write(0, 0, "Asin")
sheet.write(0, 1, "Star")
sheet.write(0, 2, "Title")
sheet.write(0, 3, "Date")
sheet.write(0, 4, "Writer")
sheet.write(0, 5, "Content")
sheet.write(0, 6, "URL")

db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')
cursor = db.cursor()

cursor.execute("SELECT Asin, ReViewUrl, Review FROM `product` WHERE `ReViewUrl` != '' AND asin in (select asin from product_category where isout= 1)")
row = cursor.fetchall()

index = 1

for rows in row:
  asin = rows[0]
  #ASIN
  print asin
  #ASIN
  
  numberofR = None
  protect_timeout = 0
  #keep repeating request until getting the data
  while numberofR is None:
    protect_timeout = protect_timeout + 1
    time.sleep(random.randint(3,8))
    if protect_timeout > 20:
      break
    try:
      r = requests.get(rows[1])
      r_html= r.text.encode('utf8')
      soup = BeautifulSoup(r_html)
      numberofR = soup.find('span',{'class':'a-size-medium a-text-beside-button totalReviewCount'}).string
    except requests.exceptions.ConnectionError:
      r.status_code = "Connection Refused"
  if protect_timeout > 20:
    sheet.write(index,0,asin)
    sheet.write(index,6,rows[1])
    index = index + 1
    continue
  else:
    num = int(numberofR)
    last = num%10
    quotient = num/10
    if quotient is 0:
     	last = 0
  	if last > 0:
    	quotient = quotient + 1
        
        
    #===page 1===
    reviews = soup.findAll('div',{'class':'a-section review'})
    for run in reviews:
      star = <span class="a-icon-alt">
  		title = <a class="a-size-base a-link-normal review-title a-color-base a-text-bold">
  		date = <span class="a-size-base a-color-secondary review-date">
  		writer = <a class="a-size-base a-link-normal author">
  		contents = <span class="a-size-base review-text">
    #============
    
    #===if has page 2
    if quotient is 0:
      pass
    else:
      for page in range(2,quotient+1):
        try:
          r = requests.get(rows[1]+"/ref=cm_cr_pr_btm_link_"+`pages`+"?pageNumber="+`pages`)
        except requests.exceptions.ConnectionError:
          r.status_code = "Connection Refused"
        r_html= r.text.encode('utf8')
        soup = BeautifulSoup(r_html)
        
    