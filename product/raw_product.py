import MySQLdb
import requests
from BeautifulSoup import BeautifulSoup
import time
import xlwt
import random
from datetime import date
from datetime import timedelta

today = date.today()
offset = (12 - today.weekday()) % 7
lastSaturday = today + timedelta(days=offset)

str_lastSaturday =lastSaturday.strftime('%Y-%m-%d')
str_today = today.strftime('%Y-%m-%d')


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
sheet.write(0, 12, "Product Description")
sheet.write(0, 13, "Function Description")

db = MySQLdb.connect(host='localhost', user='james',passwd='james123!',db='toy_union')
cursor = db.cursor()



cursor.execute("SELECT Asin From product_category where isout='1'")
row = cursor.fetchall()

index = 1



start = time.ctime()
for rows in row:
  asin =''
  title = ''
  priceStr = ''
  lpriceStr = ''
  opriceStr = ''
  starStr = ''
  reviewStr = ''
  reviewURLStr = ''
  qaStr=''
  qaURLStr=''
  availStr=''
  imgURLStr=''
  descStr = ''
  f_descStr = ''
  
  print "===" + `index` + "==="
  asin = rows[0]
  #ASIN
  print asin
  asinURL = "http://www.amazon.com/dp/"+asin
  sheet.write(index,0,asin)
  #ASIN
  try:
    r = requests.get("http://www.amazon.com/dp/"+asin)
    r_html= r.text.encode('utf8')
    soup = BeautifulSoup(r_html)
  
    de_title = soup.find('span',{'id':'productTitle'},{'class':'a-size-large'})
  except:
    pass
  protect_timeout = 0
  #keep repeating request until getting the data
  while de_title is None:
    try:
      r = requests.get("http://www.amazon.com/dp/"+asin)
      r_html= r.text.encode('utf8')
      soup = BeautifulSoup(r_html)
      de_title = soup.find('span',{'id':'productTitle'},{'class':'a-size-large'})
      protect_timeout = protect_timeout + 1
      if protect_timeout > 20:
        break
      time.sleep(random.randint(3,8))
    except:
      pass
  #=============================================
  
  
  if protect_timeout > 20:
    index = index + 1
    continue
  else:  
    #title
    title = de_title.string
    print title
    sheet.write(index,1,title)
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
        lpriceStr = listprice.string 
        print "List Price:"+lpriceStr
        sheet.write(index,2,lpriceStr)
      priceStr = price.string
      print "Price:"+priceStr    
      sheet.write(index,3,priceStr)
    #else: 
    #check other price source
    otherprice = soup.find('div',{'class':'a-section a-spacing-small a-spacing-top-small'})
    if otherprice is not None:
      otherprice_new = otherprice.find('span',{'class':'a-color-price'})
      #in usual [0]:new, [1]:collectible
      if otherprice_new is None:
        print "No price"
        sheet.write(index,4,"No price")
      else:
        opriceStr = otherprice_new.string
        
        print "OtherSourcePrice:"+opriceStr
        sheet.write(index,4,opriceStr)
    else:
      print "No Other Price"
    if price is None:
      priceStr = opriceStr
      sheet.write(index,3,priceStr)
  
    #==== price ====
  
  
    #=== Star ===
    star = soup.find('span',{'id':'acrPopover'},{'class':'reviewCountTextLinkedHistogram noUnderline'})
    if star is None:
      print "No Star"
    else:
      starStr = star['title']
      sheet.write(index,5,starStr)
      print starStr 
    #=== Star ===
  
  
    #review
    review = soup.find('span',{'id':'acrCustomerReviewText'},{'class':'a-size-base'})
    reviewURL = soup.find('a',{'class':'a-link-emphasis a-text-bold'},{'href':True})
    if review is not None:
      reviewStr = review.string
      sheet.write(index,6,reviewStr)
      print reviewStr
      if reviewURL is not None:
        reviewURLStr = reviewURL['href']
        print reviewURLStr
        sheet.write(index,7, reviewURLStr)
      else:
        reviewURLStr = "http://www.amazon.com/dp/"+asin+"#customerReviews"
        sheet.write(index,7, reviewURLStr)
    else:
      print "No Review"
    
    
    #review
  
    #Q&A data
    qa = soup.find('a',{'class':'a-link-normal askATFLink'})
    qaURL = "http://www.amazon.com/ask/questions/asin/"+asin+"/ref=ask_ql_qlh_hza"
    qaURLStr = qaURL
    if qa is not None:
      #level2 find
      qa2 = qa.find('span')
      qaStr = qa2.text.encode('utf8')
      
      print qaStr
      print qaURLStr
      sheet.write(index,8,qaStr)
      sheet.write(index,9,qaURLStr)
    else:
      print "No Q&A"
    #=== Q&A ===
  
  
    
  
    #===availability===
    avail = soup.find('div',{'id':'availability'},{'class':'a-section a-spacing-none'})
      #level2 find
    if avail is None:
      avail = soup.find('div',{'id':'availability-brief'},{'class':'a-section a-spacing-none'})
    if avail is not None:
      avail2 = avail.find('span')
      if avail2 is None:
        print "Not Available"
      else:
        availStr = avail2.text.encode('utf8')
        print availStr
        sheet.write(index,10,availStr)
    else:
      print "Not Available"
  
    #===availability===
    
    
  
    #=== ImgUrl ===
    imgUrl = soup.find('img',{'data-old-hires':True})
    if imgUrl is None:
      reserve1 = soup.find('script',{'type':'text/javascript'})
      if reserve1 is None:
        print "NoImgUrl"
      else:
        reserve1URL = reserve1.string.split('"')[1]
        imgURLStr = reserve1URL
        print imgURLStr
        sheet.write(index,11,imgURLStr)
    elif imgUrl['data-old-hires']:
      imgURLStr = imgUrl['data-old-hires']
      print imgURLStr
      sheet.write(index,11,imgURLStr)
    else:
      reserve = imgUrl['data-a-dynamic-image'].split('"')
      imgURLStr = reserve[1]
      print imgURLStr
      sheet.write(index,11,imgURLStr)
    #=== ImgUrl ===
  
    #=== Product Description ===
    desc = soup.find('div',{'id':'productDescription'})
    spec = soup.find('div',{'class':'text-block a-spacing-small'})
    if spec is None:
      if desc is not None:
        description = desc.find('p')
        if description is not None:
          descStr = description.text.encode('utf8')
          print descStr
          sheet.write(index,12,descStr)
      else:
        print "No description"
    else:
      descStr = spec.text.encode('utf8')
      print descStr
      sheet.write(index,12,descStr)
    #=== Product Description ===
    
    #=== Function Desc ====
    li = soup.findAll('li')
    if li is not None:
      for lis in li:
        liDetail=lis.findAll('span',{'class':'a-list-item'})
        for details in liDetail:
          if details.string:
            f_descStr = f_descStr+"\n"+(details.string.__str__('utf8'))
      print f_descStr
      sheet.write(index,13,f_descStr)
    else:
      print "No function description"
      sheet.write(index,13,"No function description")
    #=== Function Desc ====
    
    
    index = index + 1
    time.sleep(random.randint(5,10))
    book.save("verTest3.xls")
    cursor.execute("INSERT INTO raw_product(Asin, Title, ListPrice, Price, Star, Status, New, Collectible, Used, ReView, ReViewUrl, QA, QAUrl, DType, DateData, Enddate, Url, ImageUrl, content,  type, availability,function_content) VALUES (%s, %s, %s, %s, %s, %s,%s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",(asin,title,lpriceStr, priceStr, starStr,'','',opriceStr,'',reviewStr,reviewURLStr, qaStr, qaURLStr, 'US' ,str_today, str_lastSaturday,'', imgURLStr, descStr, '',availStr,f_descStr))
    db.commit()
"""
index = 1

start = time.ctime()
mylist=[]
for rows in row:
  mylist.append([rows[0],0])

mylist[0][1] = 1
print mylist[0][1]
print mylist[5]

for lists in mylist:
  if lists[1] is 1:
    print lists[0]
    
    
print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
"""   