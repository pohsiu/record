<?php
$serverName = "adminID\SQLEXPRESS"; //serverName\instanceName
// Since UID and PWD are not specified in the $connectionInfo array,
// The connection will be attempted using Windows Authentication.
$connectionInfo = array( "Database"=>"db", "UID"=>"root", "PWD"=>"root");
$conn = sqlsrv_connect( $serverName, $connectionInfo);
if( $conn === false ) {
     die( print_r( sqlsrv_errors(), true));
}
echo "AmazonSearch Start</br>";
echo "=====================================</br>";
$asinNA=array("http://www.amazon.com/s/ref=sr_pg_3?rh=n%3A165796011%2Cn%3A%21165797011%2Cn%3A166828011%2Cn%3A166850011%2Cn%3A166851011&page=3&ie=UTF8&qid=1428420272&spIA=B002HTRXUM,B001KZC79G,B005NHRVDE",
"http://www.amazon.co.uk/s/ref=nb_sb_noss/278-3709780-1636104?url=search-alias%3Daps&field-keywords=gemar%20balloon",
"http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=LeapFrog%20Fridge%20Phonics%20Magnetic%20Letter%20Set%20",
"http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Dtoys-and-games&field-keywords=Hexbug%20Scarab%20",
"http://www.amazon.com/s/ref=sr_pg_1?rh=i%3Aaps%2Ck%3Awater+bomb+easy+tie&keywords=water+bomb+easy+tie&ie=UTF8&qid=1437037461&spIA=B0106WXV3O",
"http://www.amazon.com/s/ref=sr_pg_1?rh=i%3Aaps%2Ck%3Amodelling+balloon&keywords=modelling+balloon&ie=UTF8&qid=1437037569&spIA=B00WEE4PHO",
"http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=rocket+balloon");
//echo sizeof($asinNA); 
for($i=0;$i<sizeof($asinNA);$i++){
	$checkNA = "Select Index_id FROM dbo.AmazonSearch WHERE Link ="."'$asinNA[$i]'";
  $query = sqlsrv_query( $conn, $checkNA );
  if(sqlsrv_num_rows($query)==0){
    echo $i.":".$asinNA[$i]."</br></br>";
  }
}
?>
/*
before applied


apache 32bit required
php 5.4 <> php_sqlsrv_54_ts.dll + php_pdo_sqlsrv_54_ts.dl
(註 5.4 則對應 55)
put those two into \ext file
modify php.ini
extension  = php_sqlsrv_54_ts.dll 
extension  = php_pdo_sqlsrv_54_ts.dll
restart apache
*/
