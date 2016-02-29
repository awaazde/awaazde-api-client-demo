<?php

/**
  * Copyright (c) 2013 Awaaz.De
  * Template Manager class is responsible for dealing with templates
  *
  * @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
  * 
  */
class TemplateManager {
	
	/*** auth data ***/
	private $authdata;
	
	
	/*** pest object ***/
	private $pest;
	
	/*** the constructor ***/
	public function __construct($authdata){
		$this->authdata = $authdata;
		$this->pest = new Pest($authdata->getUrl());
		$this->pest->setupAuth($authdata->getUsername(),$authdata->getPassword());
		$this->pest->curl_opts[CURLOPT_FOLLOWLOCATION] = false; // Not supported on hosts running safe_mode!
	}
	
	/**
	 * Returns all templates
     * @return array containing all templates
     * 
    */
	public function getAll() {
		try {		    
			$calljson = $this->pest->get('/templates/');
			return json_decode($calljson,true);
		} 
		catch (Exception $e) {
			echo "<br>Caught exception when retrieving templates data : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Returns template
	 * @callId id of template
	 * 
     * @return
     * 
    */
	public function get($templateId) {
		try {		    
			$datajson = $this->pest->get('/templates/' . $templateId .'/');
			return json_decode($datajson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when retrieving template : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Creates new template
	 * @data template data
	 * 
     * @return
     * 
    */
	public function create($data) {
		try {		    
			$datajson = $this->pest->post('/templates/', $data);
			return json_decode($datajson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when creating template : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Modifies existing templates using given data
	 * @templateId template id
	 * @data template data
	 * 
     * @return array containing all data
     * 
    */
	public function update($templateId, $data) {
		try {		    
			$datajson = $this->pest->put('/templates/'.$templateId .'/', $data);
			return json_decode($datajson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when editing template : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Delete template
	 * @templateId 
	 * 
     * @return
     * 
    */
	public function delete($templateId) {
		try {		    
			$this->pest->delete('/templates/'.$templateId .'/');
		}
		catch (Exception $e) {
			echo "<br>Caught exception when deleting templates: " .  $e->getMessage() . "<br>";
		}
	}


	/**
	 * Upload file aginst template
	 * @templateId - template id
	 * @file - file object or url
	 * 
     * @return
     * 
    */
	public function upload_file($templateId, $file, $is_url=false) {
		try {		    
			$data = array(
    			'template_pk' => $templateId
    		);

			if($is_url) {
				$data['file_url'] = $file;
			}
			else {
				$data['file'] = '@' . realpath($file);
			}

			$datajson = $this->pest->post('/templates/'.$templateId .'/files/', $data);
			return json_decode($datajson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when uploading files: " .  $e->getMessage() . "<br>";
		}
	}
}