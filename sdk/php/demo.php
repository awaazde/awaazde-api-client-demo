<?php
/**
 * Copyright (c) 2013 Awaaz.De 
 * This sample code to call xact api
 * API documentation: http://awaaz.de/console/xact/
 **/


// Setting up 
require_once 'include_all.php';

 // Xact auth info
$user 		= "<your  username>";
$password 	= "<password>";
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
?>
