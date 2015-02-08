<?php

require "twilio-php-master/Services/Twilio.php";
     
// Set our AccountSid and AuthToken from twilio.com/user/account
$AccountSid = "AC56a6ba75f572373427231aeb66e0bc21";
$AuthToken = "d2d16fa8f34b9b6db9fb2394b9de7901";

// Instantiate a new Twilio Rest Client
$client = new Services_Twilio($AccountSid, $AuthToken);

foreach ($client->account->messages as $sms) {
    $body = $sms->body;
    $phone_num = $sms->from;
    break;
}

$command = '/usr/bin/python2.7 parser.py "' . $body . '" ' . $phone_num;

exec($command, $output, $ret_code);

echo '<Response> <Message><Body>' . $body . '</Body><Media>' . $output[0] . '</Media></Message></Response>';

?>
