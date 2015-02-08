<?php

require "twilio-php-master/Services/Twilio.php";
//require_once "Logger.php";
     
// Set our AccountSid and AuthToken from twilio.com/user/account
$AccountSid = "AC56a6ba75f572373427231aeb66e0bc21";
$AuthToken = "d2d16fa8f34b9b6db9fb2394b9de7901";

// Instantiate a new Twilio Rest Client
$client = new Services_Twilio($AccountSid, $AuthToken);

foreach ($client->account->messages as $sms) {
	$sms_final = $sms;
	$body = $sms->body;
    $media = $sms->media;
    $phone_num = $sms->from;
    break;
}

if(strcmp($sms_final->num_media,"1") === 0) {
	$media = $media->uri;
	$media = 'https://api.twilio.com' . $media;

	// Gets url contents with username and password
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $media);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_USERPWD, "{$AccountSid}:{$AuthToken}");
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_BASIC);
	$outpt = curl_exec($ch);
	$info = curl_getinfo($ch);
	curl_close($ch);

	$xml = simplexml_load_string($outpt);

	// Parse XML to get Uri
	$uri = "https://api.twilio.com" . $xml->MediaList->Media->Uri;

	$path = "img/";
	$fn = "image.jpg";

	$full_path = $path . $fn;

	// Copy file into server
	copy($uri, $full_path);


	$command = '/usr/bin/python2.7 parser.py "image" ' . $phone_num . ' ' . $full_path;

	exec($command, $output, $ret_code);

	echo '<Response><Message>Successfully added file!</Message></Response>';
}
else {
	$command = '/usr/bin/python2.7 parser.py "' . $body . '" ' . $phone_num;

	exec($command, $output, $ret_code);

	if (strlen($output[0]) > 50) {
    	echo '<Response> <Message><Body>' . 'Success!'. '</Body><Media>' . $output[0] . '</Media></Message></Response>';
	}
	else {
		echo '<Response> <Message>' . 'Success!' . ' ' . $output[0] . '</Message></Response>';
	}
}

?>
