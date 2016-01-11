import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import time
import xlwt
import random
import os

start = time.ctime()

# book = xlwt.Workbook(encoding="utf-8")

# sheet = book.add_sheet("python sheet")
# sheet.write(0, 0, "FailedAsin")
# # sheet.write(0, 1, "Star")
# # sheet.write(0, 2, "Title")
# # sheet.write(0, 3, "Date")
# # sheet.write(0, 4, "Writer")
# # sheet.write(0, 5, "Content")
# sheet.write(0, 6, "URL")

#db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')#localhost
db = MySQLdb.connect(host='localhost', user='james',passwd='james123!',db='crawlerdb')#server
cursor = db.cursor()

cursor.execute("SELECT Asin, ReViewUrl, Review FROM `product` WHERE `ReViewUrl` != '' AND asin in (select asin from product_category where isout= 1)")
row = cursor.fetchall()

index = 1

for rows in row:
  asin = ''
  

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
      numberofR = soup.find('span',{'class':'a-size-medium a-text-beside-button totalReviewCount'})
      if numberofR:
        numberofR = numberofR.text.encode('utf8').replace(",","")
    except requests.exceptions.ConnectionError:
      r.status_code = "Connection Refused"
  if protect_timeout > 20:
    # sheet.write(index,0,asin)
    # sheet.write(index,6,rows[1])
    # index = index + 1
    cursor.execute("INSERT IGNORE INTO debug_review(asin, url) VALUES (%s, %s)",(asin, rows[1]))
    db.commit()
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
      str_star = ''
      str_title = ''
      str_date = ''
      str_writer = ''
      str_contents = ''
      star = run.find('span',{'class':'a-icon-alt'})
      #<span class="a-icon-alt">
      title = run.find('a',{'class':'a-size-base a-link-normal review-title a-color-base a-text-bold'})
      #<a class="a-size-base a-link-normal review-title a-color-base a-text-bold">
      date = run.find('span',{'class':'a-size-base a-color-secondary review-date'})
      #<span class="a-size-base a-color-secondary review-date">
      writer = run.find('a',{'class':'a-size-base a-link-normal author'})
      #<a class="a-size-base a-link-normal author">
      contents = run.find('span',{'class':'a-size-base review-text'})
      #<span class="a-size-base review-text">
      if star:
        str_star = star.string#.__str__('utf8')
        print "STAR:"+ str_star
      if title:
        str_title = title.string#.__str__('utf8') 
        print "TITLE:"+ str_title
      if date:
        str_date = date.string.split('on ')[1]#__str__('utf8')
        print "DATE:"+ str_date
      if writer:
        str_writer = writer.text.encode('utf8')#__str__('utf8')
        print "WRITER:"+str_writer
      if contents:
        str_contents = contents.text.encode('utf8')#__str__('utf8')
        print "CONTENTS:"
        print str_contents

      # sheet.write(index, 0, asin)
      # sheet.write(index, 1, str_star)
      # sheet.write(index, 2, str_title)
      # sheet.write(index, 3, str_date)
      # sheet.write(index, 4, str_writer)
      # sheet.write(index, 5, str_contents)
      # sheet.write(index, 6, row[1])
      # book.save("reviews.xls")
      cursor.execute("INSERT IGNORE INTO raw2_review(Asin, Star, Title, Date, writer, Content) VALUES (%s, %s, %s, %s, %s, %s )",( asin, str_star, str_title, str_date, str_writer, str_contents))
      db.commit()


      index = index + 1
      print "=================="
    #============
    
    #===if has page 2
    if quotient is 0:
      pass
    else:
      for pages in range(2,quotient+1):
        time.sleep(random.randint(3,5))
        try:
          urlR = rows[1]+"/ref=cm_cr_pr_btm_link_"+`pages`+"?pageNumber="+`pages`
          r = requests.get(urlR)
        except requests.exceptions.ConnectionError:
          r.status_code = "Connection Refused"
        r_html= r.text.encode('utf8')
        soup = BeautifulSoup(r_html)
        reviews = soup.findAll('div',{'class':'a-section review'})
        for run in reviews:
          str_star = ''
          str_title = ''
          str_date = ''
          str_writer = ''
          str_contents = ''

          star = run.find('span',{'class':'a-icon-alt'})
          #<span class="a-icon-alt">
          title = run.find('a',{'class':'a-size-base a-link-normal review-title a-color-base a-text-bold'})
          #<a class="a-size-base a-link-normal review-title a-color-base a-text-bold">
          date = run.find('span',{'class':'a-size-base a-color-secondary review-date'})
          #<span class="a-size-base a-color-secondary review-date">
          writer = run.find('a',{'class':'a-size-base a-link-normal author'})
          #<a class="a-size-base a-link-normal author">
          contents = run.find('span',{'class':'a-size-base review-text'})
          #<span class="a-size-base review-text">
          if star:
            str_star = star.string#.__str__('utf8')
            print "STAR:"+ str_star
          if title:
            str_title = title.string.encode('ascii', 'ignore')
            print "TITLE:"+ str_title
          if date:
            str_date = date.string.split('on ')[1]#__str__('utf8')
            print "DATE:"+ str_date
          if writer:
            str_writer = writer.text.encode('utf8')#__str__('utf8')
            print "WRITER:"+str_writer
          if contents:
            str_contents = contents.text.encode('utf8')#__str__('utf8')
            print "CONTENTS:"
            print str_contents

          # sheet.write(index, 0, asin)
          # sheet.write(index, 1, str_star)
          # sheet.write(index, 2, str_title)
          # sheet.write(index, 3, str_date)
          # sheet.write(index, 4, str_writer)
          # sheet.write(index, 5, str_contents)
          # sheet.write(index, 6, urlR)
          # book.save("reviews.xls")
          cursor.execute("INSERT IGNORE INTO raw2_review(Asin, Star, Title, Date, writer, Content) VALUES (%s, %s, %s, %s, %s, %s )",( asin, str_star, str_title, str_date, str_writer, str_contents))
          db.commit() 
          index = index + 1
          print "=================="

os.system("debug_review.py 1")#start debug python program
    