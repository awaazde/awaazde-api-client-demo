<?php
/**
 * This sample code to call xact 2.0 api for PHP
 **/
require_once 'autoload.php';

$authData = new AuthData('http://localhost:8000/payal/v1/', 'payal@awaaz.de', 'kapil123');

/*************************************************************************************************************************************************************/
/** Template API CRUD **/
$templateAPI = new TemplateAPI($authData);

//Create new template example
$data = ['name' => 'template-varsha-1', 'advanced_options' => [["option" => "response_type", "value" => "none"], ["option" => "num_backups", "value" => 0], ["option" => "phone_numbers", "value" => "+917961344101"]]];
try {
	$template = $templateAPI->create($data);
	echo 'Creating new template with ID ';
	print_r($template->id);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get by ID
try {
	$template_1 = $templateAPI->get(1);
	echo 'Getting single template ';
	print_r($template_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get raw reports
try {
	$template_1 = $templateAPI->getRawReports(1);
	echo 'Getting template raw reports';
	print_r($template_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get statistics
try {
	$template_1 = $templateAPI->getStatistics(1);
	echo 'Getting template statistics';
	print_r($template_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get all 
try {
	$allTemplate = $templateAPI->getAll();
	echo 'Getting all templates';
	print_r($allTemplate->count);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Update by ID
$data = ['advanced_options' => [["option" => "response_type", "value" => "none"], ["option" => "num_backups", "value" => 0], ["option" => "phone_numbers", "value" => "+917961344101"]]];
try {
	
	$template = $templateAPI->update(1, $data);
	echo 'Updating template by ID ';
	print_r($template);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Delete template by ID
try {
	$id = 29;
	$template = $templateAPI->delete($id);
	print_r($template);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

/*************************************************************************************************************************************************************/
/** Content API CRUD **/

$contentAPI = new ContentAPI($authData);

//Create new content
$data1 = [['name' => 'file', 'contents' => fopen('1.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "1"]];
$data2 = [['name' => 'file', 'contents' => fopen('2.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "2"]];
$data3 = [['name' => 'file', 'contents' => fopen('3.wav', 'r')], ['name' => 'type', 'contents' => 1], ['name' => 'name', 'contents' => "3"]];
try {
	echo 'Creating new contents';
	$content = $contentAPI->create($data1);
	print_r($content->id);
	$content = $contentAPI->create($data2);
	print_r($content->id);
	$content = $contentAPI->create($data3);
	print_r($content->id);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}
// Get content by ID
try {
	$id=$content->id;
	echo 'Getting content by ID ';
	$content_1 = $contentAPI->get($id);
	print_r($content_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get all
try {
	echo 'Getting all the contents ';
	$allContent = $contentAPI->getAll();
	print_r($allContent->count);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Update content by ID
try {
	$data = [['name' => 'file-update']];
	echo 'Updating content by ID ';
	$content = $contentAPI->update($id, $data);
	print_r($content);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Delete content by ID
try {
	$id = 29;
	$template = $contentAPI->delete($id);
	print_r($template);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

/*************************************************************************************************************************************************************/
/** Template Language API API CRUD **/
$templateLanguageAPI = new TemplateLanguageAPI($authData);

//Create new template language example
$data = ['template' => ['id'=>1], 'language' => 'gu', 'syntax' => 'one _N_ two _W_ three', 'content' => [['id'=>44], ['id'=>45], ['id'=>46]]];
try {
	echo 'Creating new template languages';
	$templatelanguage = $templateLanguageAPI->create($data);
	print_r($templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get template language by ID
try {
	echo 'Get template language by ID';
	$templatelanguage_1 = $templateLanguageAPI->get($templatelanguage->id);
	print_r($templatelanguage_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Get all template languages
try {
	echo 'Getting all template languages';
	$all_templatelanguage = $templateLanguageAPI->getAll();
	//print_r($all_templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Updating template language  by ID
try {
	echo 'Updating template language by ID';
	$data = ['language' => 'hi'];
	$templatelanguage = $templateLanguageAPI->update(1, $data);
	print_r($templatelanguage);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

// Delete template language by ID
try {
	$id = 29;
	$template = $templateLanguageAPI->delete($id);
	print_r($template);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}


/*************************************************************************************************************************************************************/
/** Message API CRUD **/
$messageAPI = new MessageAPI($authData);


//Create new template language example
$data = ['templatelanguage' => 3, 'phone_number' => '+919429515176', 'values' => ['10', '1']];

try {
	echo 'Creating new messages';
	$message = $messageAPI->create($data);
	print_r($message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	echo 'Get message by ID';
	$message_1 = $messageAPI->get($message->id);
	print_r($message_1);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	echo 'Get all messages';
	$all_message = $messageAPI->getAll();
	// print_r($all_message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}

try {
	echo ' Updating message';
	$data = ['templatelanguage' => 2];
	$message = $messageAPI->update($message->id, $data);
	//print_r($message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}


// upload message via file
try {
	echo ' Uploading messages';
	$message = $messageAPI->upload("sample_messages.csv");
	//print_r($message);
} catch (Awaazde_Exception $e) {
	print_r($e->getMessage());
}
?>
