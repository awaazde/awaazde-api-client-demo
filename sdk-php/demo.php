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
	$template = $templateAPI->create($data);
	print_r($template);
	print_r($template->id);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get template  by id
try {
    $id=15
	$template_1 = $templateAPI->get($id);
	print_r($template_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}


// Get all templates
try {
	$allTemplate = $templateAPI->getAll();
	print_r($allTemplate);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Update template by id
try {
    $id=1
	$template = $templateAPI->update($id, $data);
	print_r($template);
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


// Create content
try {
	$content = $contentAPI->create($data1);
	print_r($content->id);
	$content = $contentAPI->create($data2);
	print_r($content->id);
	$content = $contentAPI->create($data3);
	print_r($content->id);
	$content = $contentAPI->create($datakapil);
	print_r($content->id);
	$content = $contentAPI->create($datanikhil);
	print_r($content->id);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get content
try {
    $id=15
	$content_1 = $contentAPI->get($id);
	print_r($content_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get all contents
try {
	$allContent = $contentAPI->getAll();
	print_r($allContent);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Update content by id
try {
    $id=1
	$content = $contentAPI->update($id, $data);
	print_r($content);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

/**
Template Language API API CRUD
**/
$templateLanguageAPI = new TemplateLanguageAPI($authData);

//Create new template language example
$data = ['template' => ['id'=>1], 'language' => 'en', 'syntax' => 'one _N_ two _W_ three', 'content' => [['id'=>30], ['id'=>31], ['id'=>32], ['id'=>33], ['id'=>34]]];

// Create template language
try {
	$templatelanguage = $templateLanguageAPI->create($data);
	print_r($templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

//Get template language by ID
try {
    $id=15
	$templatelanguage_1 = $templateLanguageAPI->get($id);
	print_r($templatelanguage_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get all template languages
try {
	$all_templatelanguage = $templateLanguageAPI->getAll();
	print_r($all_templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}


// Update template language by id
try {
    $id=1
	$templatelanguage = $templateLanguageAPI->update($id, $data);
	print_r($templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

/**
Message API API CRUD
**/
$messageAPI = new MessageAPI($authData);

//Create new template language example
$data = ['templatelanguage' => 1, 'phone_number' => '+919429515176', 'values' => ['10', 'kapil']];

// Create message
try {
	$message = $messageAPI->create($data);
	print_r($message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get message by ID
try {
	$message_1 = $messageAPI->get(15);
	print_r($message_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get all messages
try {
	$all_message = $messageAPI->getAll();
	print_r($all_message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Update message by ID
try {
	$message = $messageAPI->update(1, $data);
	print_r($message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

?>