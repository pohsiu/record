import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import time
import xlwt

#print "Start : %s" % time.ctime()
book = xlwt.Workbook(encoding="utf-8")

sheet = book.add_sheet("python sheet")
sheet.write(0, 0, "Asin")
sheet.write(0, 1, "Title")
sheet.write(0, 2, "ListPrice")
sheet.write(0, 3, "Price")
sheet.write(0, 4, "OtherSourcePrice")
sheet.write(0, 5, "Star")
sheet.write(0, 6, "Review")
sheet.write(0, 7, "ReviewURL")
sheet.write(0, 8, "Q&A")
sheet.write(0, 9, "Q&A URL")
sheet.write(0, 10, "Availability")
sheet.write(0, 11, "ImgUrl")

db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')
cursor = db.cursor()

cursor.execute("SELECT Asin From product_category where isout='1'")
row = cursor.fetchall()

index = 1
#try:
#	dosomething()
#except:
#	pass
for rows in row:
  asin = rows[0]
  #ASIN
  print asin
  sheet.write(index,0,asin)
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
  sheet.write(index,1,de_title.string)
  #title

  #==== price ====
  price = soup.find('span',{'id':'priceblock_ourprice'},{'class':'a-size-medium a-color-price'})
  if price is None:
    price = soup.find('span',{'id':'priceblock_saleprice'},{'class':'a-size-medium a-color-price'})
    #=== pharse 1: normal price ===
  #if price is not None would have list price
  if price is not None:
    listprice = soup.find('td',{'class':'a-span12 a-color-secondary a-size-base a-text-strike'})
    if listprice is not None:
      print "List Price:"+listprice.string
      sheet.write(index,2,listprice.string)
    print "Price:"+price.string    
    sheet.write(index,3,price.string)
  else: 
    #check other price source
    otherprice = soup.find('div',{'class':'a-section a-spacing-small a-spacing-top-small'})
	  if otherprice is not None:  
	    otherprice_new = otherprice.find('span',{'class':'a-color-price'})
	    #in usual [0]:new, [1]:collectible
	    if otherprice_new is None:
	      print "No price"
	      sheet.write(index,4,"No price")
	    else:
	      print "OtherSourcePrice:"+otherprice_new.string
	      sheet.write(index,4,otherprice_new.string)
		else:
			print "No price"
	   	

  #==== price ====


  #=== Star ===
  star = soup.find('span',{'id':'acrPopover'},{'class':'reviewCountTextLinkedHistogram noUnderline'})
  if star is None:
    print "No Star"
  else:
    sheet.write(index,5,star['title'])
    print star['title'] 
  #=== Star ===


  #review
  review = soup.find('span',{'id':'acrCustomerReviewText'},{'class':'a-size-base'})
  reviewURL = soup.find('a',{'class':'a-link-emphasis a-text-bold'},{'href':True})
  if review is not None:
    sheet.write(index,6,review.string)
    print review.string
    if reviewURL is not None:
    print reviewURL['href']
    	sheet.write(index,7,reviewURL['href'])
    else:
    	shhet.write(index,7,"www.amazon.com/dp/"+asin+"#customerReviews")
  else:
    print "No Review"
  #review

  #Q&A data
  qa = soup.find('a',{'class':'a-link-normal askATFLink'})
  qaURL = "http://www.amazon.com/ask/questions/asin/"+asin+"/ref=ask_ql_qlh_hza"
  if qa is not None:
    #level2 find
    qa2 = qa.find('span')
    print qa2.text.encode('utf8')
    print qaURL
    sheet.write(index,8,qa2.text.encode('utf8'))
    sheet.write(index,9,qaURL)
  else:
    print "No Q&A"
  #=== Q&A ===


  

  #===availability===
  avail = soup.find('div',{'id':'availability'},{'class':'a-section a-spacing-none'})
    #level2 find
  if avail is None:
    avail = soup.find('div',{'id':'availability-brief'},{'class':'a-section a-spacing-none'})
  avail2 = avail.find('span')
  if avail2 is None:
    print "Not Available"
  else:
    print avail2.text.encode('utf8')
    sheet.write(index,10,avail2.text.encode('utf8'))

  #===availability===
  
  

  #=== ImgUrl ===
  imgUrl = soup.find('img',{'data-old-hires':True})
  if imgUrl is None:
    print "NoImgUrl"
  elif imgUrl['data-old-hires']:
  	# if imgUrl['data-old-hires'] not null
    print imgUrl['data-old-hires']
    sheet.write(index,11,imgUrl['data-old-hires'])
  else:
  	# if imgUrl['data-old-hires'] is null, take reserve method to fix that
    reserve = imgUrl['data-a-dynamic-image'].split('"')
    reserve_imgUrl = reserve[1]
		print reserve_imgUrl
	  sheet.write(index,11,reserve_imgUrl)
  #=== ImgUrl ===

  index = index + 1
  time.sleep(3)
  
  
  
book.save("output.xls")
#print "End : %s" % time.ctime()
    
