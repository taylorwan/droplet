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

//$output = system('/usr/bin/python2.7 alextesting.py', $retval);
//$image = "https://pbs.twimg.com/profile_images/378800000320815801/cbe630c29a62e283cef31afc5c4471da_normal.png";

// $json_decoded = json_decode($json);
// $message = $json_decoded->{'body'};

//echo '<Response> <Message><Body>' . $body . '</Body><Media>' . $output[0] . '</Media></Message></Response>';
//echo '<Response> <Message><Body>' . $message . '</Body><Media>' . 'https://www.dropbox.com/s/toyzur6e0m34t7v/dropbox-logos_dropbox-glyph-blue.png?raw=1' . '</Media></Message></Response>';
echo '<Response><Message>' . $output[0] . '</Message></Response>';


?>
