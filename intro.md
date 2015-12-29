Python Crawler簡要說明

try except主要都應用在防止Max retry 時造成爬蟲停止


raw_product.py << 白名單產品基本資訊寫入raw_product table 並 輸出excel :verTest3.xls book.save("verTest3.xls”)

==========================================


raw_QA.py  輸出成QAyyyy-mm-dd.xls （查看book.save(“QAyyyy-mm-dd.xls”)) 有兩個

一個Asin 對應 一個 QA URL = first page of QA 對應 1~多個pages 
(一個page 對應 1~多個questions
 (一個question 對應 1~多個answers
                    (一個answer 對應多個 answer data)
  )
)


從DB擷取asin, QaUrl
for (each url)
{
  numberofQ : question 總數//每頁可瀏覽10筆
  quotient : QAurl總頁數
  mylist : 將本頁的question對應的URL存放至止(由於label標誌造成可能重複所以用判斷式防止重複url加入list)
  for( each mylist)
  {
   擷取每筆question的資訊
   for (each answer for this question)
   { 
    擷取對應question之所有answer
   }
  }
  for i in 2:總頁數重複上述迴圈 <<從page2開始 
}


==========================================

review.py 直接寫入db
從DB擷取asin與reviewurl, review作為日後更新備用
for(each url)
{
  numberofR : review 總數//每頁可瀏覽10筆
  quotient : review總頁數
  for (all reviews)
  {
   擷取本頁之全review之資料
  }
  for i in 2:總頁數重複上述迴圈 <<從page2開始
}

