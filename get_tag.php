<?php
require_once "twilio_credentials.php";
require "twilio-php-master/Services/Twilio.php";
     

// Instantiate a new Twilio Rest Client
$client = new Services_Twilio($AccountSid, $AuthToken);

foreach ($client->account->messages as $sms) {
    $body = $sms->body;
    $phone_num = $sms->from;
    break;
}

$command = '/usr/bin/python2.7 parser.py "' . $body . '" ' . $phone_num;

exec($command, $output, $ret_code);

echo '<Response> <Message><Body>cat.jpeg</Body><Media>' . $output[0] . '</Media></Message></Response>';

?>
