<?php
/**
 * Copyright (c) 2013 Awaaz.De 
 * This sample code to call xact api
 * API documentation: http://awaaz.de/console/xact/
 **/


// Setting up 
require_once 'include_all.php';

 // Xact auth info
$user 		= "your username";
$password 	= "your password";
$ws_url		= "https://awaaz.de/console/xact/";

//creating a authdata object
$authdata = new AuthData($user, $password, $ws_url);

//getting call information


echo "<h3>Getting all call information</h3>";

$callMgr = new CallManager($authdata);

//displaying call info
html_show_array($callMgr->getAll());

//getting specific call info
echo "<h3>Getting specific call data</h3>";
html_show_array($callMgr->get('7032'));

//creating new call
echo "<h3>Creating new call</h3>";

//call data
$calldata = array(
    'recipient' => '0123456789',
    'text' => 'You have 99 elephants waiting at awaaz',
    'send_on' => '2014-08-30T13:10:00'
	);
	
html_show_array($callMgr->create($calldata));


//editing call data
echo "<h3>Editing new call</h3>";

//call data
$callId = '7032';
$calldata = array(
    'recipient' => '0123456789',
    'text' => 'You have 33 elephants waiting at awaaz',
    'send_on' => '2014-08-30T13:11:00'
	);
	
html_show_array($callMgr->modify($callId, $calldata));


//deleting call data
echo "<h3>Deleting new call</h3>";

//call data
$callId = '7032';
echo 'deleting call with id' . $callId;
	
html_show_array($callMgr->delete($callId));


// templates related apis

$templateMgr = new TemplateManager($authdata);

//getting all templates
html_show_array($templateMgr->getAll());

//getting template with id
html_show_array($templateMgr->get(31));

//creating new template
$template_data = array (
    "text" => "This is demo",
    "vocabulary" => ["msg1", "msg2"],
    "language" => "eng"
);

html_show_array($templateMgr->create($template_data));


//updating template
$template_id = 50;

$template_data = array (
    "text" => "This is demo22",
    "vocabulary" => ["msg1", "msg2"],
    "language" => "eng"
);

html_show_array($templateMgr->update($template_id, $template_data));


//uploading files for template

echo "<h3>Uploading files</h3>";
//actual file
$file = '/home/nikhil/html/xact/msg1.wav';
html_show_array($templateMgr->upload_file($template_id, $file, false));

//file url
$file = 'http://www.pacdv.com/sounds/voices/come-on-1.wav';
html_show_array($templateMgr->upload_file($template_id, $file, true));


echo "<h3>deleting template</h3>";
html_show_array($templateMgr->delete($template_id));


$webHookMgr = new WebhookManager($authdata);

//getting all templates
html_show_array($webHookMgr->getAll());

//getting template with id
html_show_array($webHookMgr->get(11));

//creating new template
$url = "https://awaaz.de/webhook/";

html_show_array($webHookMgr->create($url));


//updating template
$id = 11;
$new_url = "https://awaaz.de/webhook/upd/";
html_show_array($webHookMgr->modify($id, $new_url));

//deleting webhook
html_show_array($webHookMgr->delete($id));

?>
