Python Crawler簡要說明

try except主要都應用在防止Max retry 時造成爬蟲停止


raw_product.py << 白名單產品基本資訊寫入raw_product table 並 輸出excel :verTest3.xls book.save("verTest3.xls”)

==========================================


QA.py  輸出成QAxxxx.xls （查看book.save(“QAxxxx.xls”)) 有兩個
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
  #有改寫成def方式（尚在測試階段） 
}

==========================================

review.py 輸出成 reviewXXXX.xls （查看book.save....）有兩個
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
