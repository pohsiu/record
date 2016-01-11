import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import time

db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')
cursor = db.cursor()

cursor.execute("SELECT Asin From product_category where isout='1' and asin='B00IQ8MTIY'")
row = cursor.fetchall()

#test2
lpriceStr =''
priceStr=''
for rows in row:
  asin = rows[0]
  #ASIN
  print asin
  #ASIN
  r = requests.get("http://www.amazon.com/dp/"+asin)
  r_html= r.text.encode('utf8')
  soup = BeautifulSoup(r_html)

  de_title = soup.find('span',{'id':'productTitle'},{'class':'a-size-large'})
  
  #keep repeating request until getting the data
  while de_title is None:
    r = requests.get("http://www.amazon.com/dp/"+asin)
    r_html= r.text.encode('utf8')
    soup = BeautifulSoup(r_html)
    de_title = soup.find('span',{'id':'productTitle'},{'class':'a-size-large'})
    time.sleep(2)
  #=============================================
  

  #title
  print de_title.string
  #title

  #=== Product Description ===
  
  desc = soup.find('div',{'id':'productDescription'})
  #spec = soup.find('div',{'class':'text-block a-spacing-small'})
  #if spec is None:
  if desc is not None:
    description = desc.find('p')
    if description is not None:
      if description.string:
        descStr = description.string
        print descStr
      else:
        #====method 2====
        li = soup.findAll('li')
        descStr =''
        if li is not None:
          for lis in li:
            liDetail=lis.findAll('span',{'class':'a-list-item'})
            for details in liDetail:
              if details.string:
                descStr = descStr+"\n"+(details.string)
        print descStr
        #sheet.write(index,12,descStr)
  else:
    print "No description"
  #else:
  #  descStr = spec.text.encode('utf8')
  #  print descStr
    #sheet.write(index,12,descStr)
  
  #=== Product Description ===
  #=== Product Description Reserve===
  """
  print "==========="
  li = soup.findAll('li')
  detail =''
  if li is not None:
    for lis in li:
      liDetail=lis.findAll('span',{'class':'a-list-item'})
      for details in liDetail:
        if details.string:
          detail = detail+"\n"+(details.string)
  print detail
  """
  #=== Product Description Reserve===  
  
  
