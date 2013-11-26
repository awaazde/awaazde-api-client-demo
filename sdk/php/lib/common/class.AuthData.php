<?php

/**
  * Copyright (c) 2013 Awaaz.De
  * Authentication Data container
  *
  * @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
  * 
  */
class AuthData {
	
	/*** username ***/
	private $username;
	
	/*** password ***/
	private $password;
	
	/*** ws_url ***/
	private $baseurl;
	
	/*** the constructor ***/
	public function __construct($uname, $pass, $url){
		$this->username = $uname;
		$this->password = $pass;
		$this->baseurl = $url;
	}
	
	/**
	 * returns username
     * @return
     * 
    */
	public function getUsername(){
		/*** return the username ***/
		return $this->username;
	}
	
	/**
	 * returns password
     * @return
     * 
    */
	public function getPassword(){
		/*** return the password ***/
		return $this->password;
	}
	
	/**
	 * returns ws_url
     * @return
     * 
    */
	public function getUrl(){
		/*** return the baseurl ***/
		return $this->baseurl;
	}
}