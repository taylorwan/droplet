<?php


require_once "twilio-php-master/Services/Twilio.php";
//require_once "Logger.php";
 
// Set our AccountSid and AuthToken from twilio.com/user/account
$AccountSid = "AC56a6ba75f572373427231aeb66e0bc21";
$AuthToken = "d2d16fa8f34b9b6db9fb2394b9de7901";
 
// Instantiate a new Twilio Rest Client
$client = new Services_Twilio($AccountSid, $AuthToken);
 
foreach ($client->account->messages as $sms) {
    $body = $sms->body;
    $media = $sms->media->uri;
    $phone_num = $sms->from;
    break;
}


$media = 'https://api.twilio.com' . $media;
 
// Gets url contents with username and password
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $media);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_USERPWD, "{$AccountSid}:{$AuthToken}");
curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
$output = curl_exec($ch);
$info = curl_getinfo($ch);
curl_close($ch);
 
$xml = simplexml_load_string($output);
//var_dump($output); 
// Parse XML to get Uri
$uri = "https://api.twilio.com" . $xml->MediaList->Media->Uri;

$path = "img/";
$fn = "hello.jpeg";
 
// Copy file into server
copy($uri, $path . $fn);

$f = fopen('logs.txt', 'a+');

$testVar = "\nnew run";
fwrite($f, $testVar);

$phone_num = "3017933261";
$path = "img/";
$command = '/usr/bin/python2.7 parser.py x ' . $phone_num . ' ' . $path . $fn;


fwrite($f, " ** executing command " . $command);

exec($command, $output, $ret_code);

fwrite($f, "** output: $output[0]");
fclose($f);

echo '<Response><Message>Success!</Message></Response>';

?>
