<?php
require_once "dropbox-sdk-php-1.1.4/lib/Dropbox/autoload.php";
require_once "DBHandler.php";
use \Dropbox as dbx;
session_start();


$code = $_POST['code'];
$phoneNumber = filter_var($_POST['phoneNumber'], FILTER_SANITIZE_NUMBER_INT);

$webAuth = $_SESSION['webAuth'];

try {
  list($accessToken, $userId) = $webAuth->finish($code);
	$dbxClient = new dbx\Client($accessToken, "Droplet/1.0");
	$accountInfo = $dbxClient->getAccountInfo();
}
catch (dbx\Exception $ex) {
   print("Error communicating with Dropbox API: " . $ex->getMessage() . "\n");
}

echo "<br><br>";
print_r($accountInfo);

$numsTokensFileName = "/var/www/html/droplet/numbersToTokens.txt";
$fileContents = file_get_contents($numsTokensFileName);

if (!is_writeable($numsTokensFileName)){
	echo "is not  writeable<br>";
}

if (strpos($fileContents, $phoneNumber) != FALSE  ){
	echo "already in file";
}else{
	$newRecord = "{$phoneNumber}|{$accessToken}\n";
	echo "putting $newRecord into $numsTokensFileName";
	echo "res: " . file_put_contents($numsTokensFileName, $newRecord, FILE_APPEND | LOCK_EX); 
}

echo "Success! You can now text 443-364-3176 to use Droplet!";

?>




