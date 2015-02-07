<?php
require_once "dropbox-sdk-php-1.1.4/lib/Dropbox/autoload.php";
use \Dropbox as dbx;
session_start();

$appInfo = dbx\AppInfo::loadFromJsonFile('credentials.json');
$clientIdentifier = "Droplet/1.0";
$redirectUri = "https://localhost/oauth2_pt2.php";
// $csrfTokenStore = 'randomdigits';
$csrfTokenStore = new dbx\ArrayEntryStore($_SESSION, 'dropbox-auth-csrf-token');

// echo $redirectUri;
$webAuth = new dbx\WebAuthNoRedirect($appInfo, $clientIdentifier);

$_SESSION['webAuth'] = $webAuth;

// $webAuth = new dbx\WebAuth($appInfo, $clientIdentifier, $redirectUri, $csrfTokenStore);

$authorizeUrl = $webAuth->start();

echo "go to " . $authorizeUrl;

echo "
	<form method='POST' action='oauth2_pt2.php'>
		Code: <input type='text' name='code'></input>
		Number: <input type='text' name='phoneNumber'></input>
		<input type='submit'>
	</form>";
	

// echo $authorizeUrl;
//header("Location: " . $authorizeUrl);





?>
