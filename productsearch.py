import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import time

db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')
cursor = db.cursor()

cursor.execute("SELECT Asin From product_category where isout='1' Limit 0,2")
row = cursor.fetchall()

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

  #review
  review = soup.find('span',{'id':'acrCustomerReviewText'},{'class':'a-size-base'})
  reviewURL = "www.amazon.com/dp/"+asin+"#customerReviews"
  if review is not None:
    print review.string
    print reviewURL
  else:
    print "No Review"
  #review

  #Q&A data
  qa = soup.find('a',{'class':'a-link-normal askATFLink'})
  qaURL = "www.amazon.com/ask/questions/asin/"+asin+"/ref=ask_ql_qlh_hza"
  if qa is not None:
    #level2 find
    qa2 = qa.find('span')
    print qa2.text.encode('utf8')
    print qaURL
  else:
    print "No Q&A"
  #=== Q&A ===

  #==== price ====
  price = soup.find('span',{'id':'priceblock_ourprice'},{'class':'a-size-medium a-color-price'})
  if price is None:
    price = soup.find('span',{'id':'priceblock_saleprice'},{'class':'a-size-medium a-color-price'})
    #=== pharse 1: normal price ===
  #if price is not None would have list price
  if price is not None:
    listprice = soup.find('td',{'class':'a-span12 a-color-secondary a-size-base a-text-strike'})
    print "List Price:"+listprice.string
    print "Price:"+price.string
  else: 
    #check other price source
    otherprice = soup.findAll('div',{'class':'a-section a-spacing-small a-spacing-top-small'})
    otherprice_new = otherprice.find('span',{'class':'a-color-price'})
    #in usual [0]:new, [1]:collectible
    if otherprice_new is None:
      print "No price"
    else:
      print "OtherSourcePrice:"+otherprice_new.string

  #==== price ====
  

  #===availability===
  avail = soup.find('div',{'id':'availability'},{'class':'a-section a-spacing-none'})
    #level2 find
  avail2 = avail.find('span')
  if avail2 is None:
    print "Not Available"
  else:
    print avail2.text.encode('utf8')
  #===availability===
  
  #=== Star ===
  star = soup.find('span',{'id':'acrPopover'},{'class':'reviewCountTextLinkedHistogram noUnderline'})
  if star is None:
    print "No Star"
  else:
    print star['title'] 
  #=== Star ===

  #=== ImgUrl ===
  imgUrl = soup.find('img',{'data-old-hires':True})
  if imgUrl is None:
    print "NoImgUrl"
  else:
    print imgUrl['data-old-hires']
  #=== ImgUrl ===
  
  
