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
sheet.write(0, 1, "Question")
sheet.write(0, 2, "Answer")
sheet.write(0, 3, "AnswerDate")
sheet.write(0, 4, "Votes")
sheet.write(0, 5, "AnswerWriter")
sheet.write(0, 6, "QuesAsker")
sheet.write(0, 7, "QuesAskDate")
sheet.write(0, 8, "Each UrL")


db = MySQLdb.connect(host='localhost', user='root',passwd='',db='toy_union')
cursor = db.cursor()

cursor.execute("SELECT Asin, QAUrl FROM product where QAUrl !=''")
row = cursor.fetchall()

index = 1

for rows in row:
  #time.sleep(random.randint(3,8))
  asin = rows[0]
  #ASIN
  print asin
  #ASIN
  try:
    r = requests.get(rows[1])
  except requests.exceptions.ConnectionError:
    r.status_code = "Connection Refused"

  r_html= r.text.encode('utf8')
  soup = BeautifulSoup(r_html)

  numberofQ = None
  
  protect_timeout = 0
  #keep repeating request until getting the data
  while numberofQ is None:
    protect_timeout = protect_timeout + 1
    time.sleep(random.randint(3,8))
    if protect_timeout > 20:
      break
    try:
      r = requests.get(rows[1])
      r_html= r.text.encode('utf8')
      soup = BeautifulSoup(r_html)
      numberofQ = soup.find('div',{'class':'a-fixed-left-grid-col askPaginationHeaderMessage a-col-left'},{'style':'width:250px;margin-left:-250px;_margin-left:-125px;float:left;'}).text.encode('utf8').split('of ')[1].split(' q')[0]
    except:
      pass
  #=============================================
  
  if protect_timeout > 20:
    index = index + 1
    continue
  else:
    print "test2"
    #sub soup circle
    questions = soup.findAll('div',{'class':'a-fixed-left-grid-col a-col-right'},{'style':'padding-left:0%;*width:99.6%;float:left;'})
    
    num = int(numberofQ)
    #convert questions to int, calculate the pages of questions
    last = num%10
    quotient = num/10
    if quotient is 0:
      last = 0
    if last > 0:
      quotient = quotient + 1
    print quotient
    #================================================
    
    
    
    mylist=[]
    for run in questions:  
      nestedQ = run.find('a',{'class':'a-link-normal'})
      if nestedQ is not None:
        if not nestedQ['href'] in mylist:
          if '/help' not in nestedQ['href']:
            mylist.append(nestedQ['href'])
    
    r.close()    
    
    #l2=[]
    #[l2.append(i) for i in mylist if not i in l2]
    #http://blog.csdn.net/jiedushi/article/details/6769673
    
    for i in range(0,len(mylist)):
      time.sleep(random.randint(3,8))
      #===pri===
      asker = ''
      question= ''
      askdate= ''
      #===pri===
      #===sub===
      answerDate=''
      answer=''
      author=''
      vote=''
      #===sub===      
      print "========Each Question======="
      print mylist[i]
      
       
      
      try:
        sub_r = requests.get("http://www.amazon.com"+mylist[i])
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
        sub_r.close()
        for each in answers:
          
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
          sheet.write(index,0,asin)
          sheet.write(index,1,question)
          sheet.write(index,2,answer)
          sheet.write(index,3,answerDate)
          sheet.write(index,4,vote)
          sheet.write(index,5,author)
          sheet.write(index,6,asker)
          sheet.write(index,7,askdate)
          sheet.write(index,8,"http://www.amazon.com"+mylist[i])
          book.save("YOLO.xls")  
          index = index + 1
          print "----------------"
          
       
        
      
        #request the last question pages ...
      #except:
      
      
    if quotient is 0:
      pass
    else:
      for page in range(2,quotient+1):
        time.sleep(random.randint(3,8))
        print `page`
        try:
          r = requests.get("http://www.amazon.com/ask/questions/asin/"+asin+"/"+`page`+"/ref=ask_ql_qlh_hza")
        except requests.exceptions.ConnectionError:
          r.status_code = "Connection Refused"
          
        r_html= r.text.encode('utf8')
        soup = BeautifulSoup(r_html)
    
        numberofQ = soup.find('div',{'class':'a-fixed-left-grid-col askPaginationHeaderMessage a-col-left'})
        questions = soup.findAll('div',{'class':'a-fixed-left-grid-col a-col-right'},{'style':'padding-left:0%;*width:99.6%;float:left;'})
        reslist=[]
        for run in questions:  
          nestedQ = run.find('a',{'class':'a-link-normal'})
          if nestedQ is not None:
            if not nestedQ['href'] in reslist:
              if '/help' not in nestedQ['href']:
                reslist.append(nestedQ['href'])
        r.close()
        #close r
        for i in range(0,len(reslist)):
          time.sleep(random.randint(3,8))
          #===pri===
          asker = ''
          question= ''
          askdate= ''
          #===pri===
          #===sub===
          answerDate=''
          answer=''
          author=''
          vote=''
          #===sub===      
          print "========Each Question======="
          print reslist[i]
          try:
            sub_r = requests.get("http://www.amazon.com"+reslist[i])
          except:
            pass
          subr_html= sub_r.text.encode('utf8')
          sub_soup = BeautifulSoup(subr_html)
                #get each quesion & answer info.
          question = sub_soup.find('meta',{'name':'title'})['content'].split('Answers: ')[1]
          askerData = sub_soup.find('div',{'class':'cdAuthorInfoBlock'}).text.encode('utf8').split('asked by')[1].split('on ')
          asker = askerData[len(askerData)-2]
          askdate = askerData[len(askerData)-1]
              
          answers = sub_soup.findAll('div',{'class':'cdMessageInfo'})
          sub_r.close()
          #close the sub_r
          for each in answers:
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
            sheet.write(index,0,asin)
            sheet.write(index,1,question)
            sheet.write(index,2,answer)
            sheet.write(index,3,answerDate)
            sheet.write(index,4,vote)
            sheet.write(index,5,author)
            sheet.write(index,6,asker)
            sheet.write(index,7,askdate)
            sheet.write(index,8,"http://www.amazon.com"+reslist[i])
            book.save("YOLO.xls")
            index = index + 1
            print "----------------"
                        
            
          
          
      
        
    
print "Start : %s" % start      
print "End : %s" % time.ctime()        
    
    
    
     
           
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
        
        
          
        
  #=============================================
  
  
  