<?php
/*
  The Beyonic_Exception class provides information on errors that may arise
  when using the Beyonic interface.
*/
class Awaazde_Exception extends Exception {

  public function __construct($message, $code, Exception $previous = null) {
    parent::__construct($message, $code, $previous);
  }

}
?>