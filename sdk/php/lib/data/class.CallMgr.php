<?php

/**
  * Copyright (c) 2013 Awaaz.De
  * Call Manager class is responsible for dealing with call data
  *
  * @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
  * 
  */
class CallManager {
	
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
	 * Returns all call data
     * @return array containing all call data
     * 
    */
	public function getAll() {
		try {		    
			$calljson = $this->pest->get('/calls/');
			return json_decode($calljson,true);
		} 
		catch (Exception $e) {
			echo "<br>Caught exception when retrieving call data : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Returns all call data
	 * @callId id of call object
	 * 
     * @return array containing call data
     * 
    */
	public function get($callId) {
		try {		    
			$calljson = $this->pest->get('/calls/' . $callId .'/');
			return json_decode($calljson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when retrieving call data : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Creates/schedule new call using given data
	 * @data call data
	 * 
     * @return array containing all data
     * 
    */
	public function create($data) {
		try {		    
			$calljson = $this->pest->post('/calls/', $data);
			return json_decode($calljson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when creating call data : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Modifies existing call using given data
	 * @callId call which needs to be modified
	 * @data call data
	 * 
     * @return array containing all data
     * 
    */
	public function modify($callId, $data) {
		try {		    
			$calljson = $this->pest->put('/calls/'.$callId .'/', $data);
			return json_decode($calljson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when editing call data : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Delete call with given call id
	 * @callId call which needs to be deleted
	 * 
     * @return
     * 
    */
	public function delete($callId) {
		try {		    
			$this->pest->delete('/calls/'.$callId .'/');
		}
		catch (Exception $e) {
			echo "<br>Caught exception when deleting call data : " .  $e->getMessage() . "<br>";
		}
	}
}


/*
Webhook Manager
*/
class WebhookManager {
	
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
	 * Returns all webhooks
     * @return array containing all webhooks
     * 
    */
	public function getAll() {
		try {		    
			$hooksjson = $this->pest->get('/webhook/');
			return json_decode($hooksjson,true);
		} 
		catch (Exception $e) {
			echo "<br>Caught exception when retrieving webhook data : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Returns webhook
	 * @id id of webhook
	 * 
     * @return 
     * 
    */
	public function get($id) {
		try {		    
			$hooksjson = $this->pest->get('/webhook/' . $id .'/');
			return json_decode($hooksjson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when retrieving webhook : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * created new webhook
	 * @data 
	 * 
     * @return
     * 
    */
	public function create($url) {
		try {		    
			$data = array("url" => $url);
			$hooksjson = $this->pest->post('/webhook/', $data);
			return json_decode($hooksjson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when creating webhook : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Modifies existing webhook
	 * @id
	 * @data 
	 * 
     * @return
     * 
    */
	public function modify($id, $url) {
		try {
			$data = array("url" => $url);
			$hooksjson = $this->pest->put('/webhook/'.$id .'/', $data);
			return json_decode($hooksjson,true);
		}
		catch (Exception $e) {
			echo "<br>Caught exception when editing webhook : " .  $e->getMessage() . "<br>";
		}
	}
	
	/**
	 * Delete webhook with id id
	 * @id
	 * 
     * @return
     * 
    */
	public function delete($id) {
		try {		    
			$this->pest->delete('/webhook/'.$id .'/');
		}
		catch (Exception $e) {
			echo "<br>Caught exception when deleting webhook : " .  $e->getMessage() . "<br>";
		}
	}
}