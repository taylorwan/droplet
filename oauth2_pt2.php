<?php
require_once "dropbox-sdk-php-1.1.4/lib/Dropbox/autoload.php";
require_once "DBHandler.php";
use \Dropbox as dbx;
session_start();


$code = $_POST['code'];
$phoneNumber = $_POST['phoneNumber'];

$webAuth = $_SESSION['webAuth'];

echo $code;

$dbHandler = new DBHandler();

$dbHandler->insertAccessToken($phoneNumber, $code);

try {
   list($accessToken, $userId) = $webAuth->finish($code);
}
catch (dbx\Exception $ex) {
   print("Error communicating with Dropbox API: " . $ex->getMessage() . "\n");
}

$dbxClient = new dbx\Client($accessToken, "Droplet/1.0");
$accountInfo = $dbxClient->getAccountInfo();
print_r($accountInfo);




?>