<?php
/**
 * This sample code to call xact 2.0 api for PHP
 **/
require_once 'autoload.php';

$authData = new AuthData('http://localhost:8000/payal/v1/', 'payal@awaaz.de', 'kapil123');

/**
Template API CRUD
**/
$templateAPI = new TemplateAPI($authData);

//Create new template example
$data = ['name' => 'testFinal', 'advanced_options' => [["option" => "response_type", "value" => "none"], ["option" => "num_backups", "value" => 0], ["option" => "phone_numbers", "value" => "+917961344101"]]];

try {
	//$template = $templateAPI->create($data);
	//print_r($template);
	//print_r($template->id);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$template_1 = $templateAPI->get(15);
	//print_r($template_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$allTemplate = $templateAPI->getAll();
	//print_r($allTemplate);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$template = $templateAPI->update(1, $data);
	//print_r($template);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

/**
Content API CRUD
**/
$contentAPI = new ContentAPI($authData);

//Create new template language example
$data1 = [['name' => 'file', 'contents' => fopen('1.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "1"]];
$data2 = [['name' => 'file', 'contents' => fopen('2.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "2"]];
$data3 = [['name' => 'file', 'contents' => fopen('3.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "3"]];
$datakapil = [['name' => 'file', 'contents' => fopen('kapil.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "kapil"]];
$datanikhil = [['name' => 'file', 'contents' => fopen('nikhil.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "nikhil"]];


try {
	//$content = $contentAPI->create($data1);
	//print_r($content->id);
	//$content = $contentAPI->create($data2);
	//print_r($content->id);
	//$content = $contentAPI->create($data3);
	//print_r($content->id);
	//$content = $contentAPI->create($datakapil);
	//print_r($content->id);
	//$content = $contentAPI->create($datanikhil);
	//print_r($content->id);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$content_1 = $contentAPI->get(15);
	//print_r($content_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$allContent = $contentAPI->getAll();
	//print_r($allContent);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$content = $contentAPI->update(1, $data);
	//print_r($content);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

/**
Template Language API API CRUD
**/
$templateLanguageAPI = new TemplateLanguageAPI($authData);

//Create new template language example
$data = ['template' => ['id'=>1], 'language' => 'en', 'syntax' => 'one _N_ two _W_ three', 'content' => [['id'=>30], ['id'=>31], ['id'=>32], ['id'=>33], ['id'=>34]]];

try {
	//$templatelanguage = $templateLanguageAPI->create($data);
	//print_r($templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$templatelanguage_1 = $templateLanguageAPI->get(15);
	//print_r($templatelanguage_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$all_templatelanguage = $templateLanguageAPI->getAll();
	//print_r($all_templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$templatelanguage = $templateLanguageAPI->update(1, $data);
	//print_r($templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}


$messageAPI = new MessageAPI($authData);

//Create new template language example
$data = ['templatelanguage' => 1, 'phone_number' => '+919429515176', 'values' => ['10', 'kapil']];

try {
	$message = $messageAPI->create($data);
	print_r($message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$message_1 = $messageAPI->get(15);
	//print_r($message_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$all_message = $messageAPI->getAll();
	//print_r($all_message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	//$message = $messageAPI->update(1, $data);
	//print_r($message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

?>