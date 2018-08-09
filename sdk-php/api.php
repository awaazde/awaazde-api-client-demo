<?php
require_once 'vendor/autoload.php';
use GuzzleHttp\Psr7;
use GuzzleHttp\Exception\RequestException;

class AuthData {
	// Email and password for authentication
	public $email = null;
	public $password = null;
	// base api
	public $baseURL = null;

	// Set Username, Password and base URL using constructore
  // Also after setting us username and password get authentication token
	function __construct($baseURL, $email, $password) {
    $this->baseURL = $baseURL;
    $this->email = $email;
    $this->password = $password;
    //Request for authentication
    $authData = [['name' => 'email', 'contents' => $email], ['name' => 'password', 'contents' => $password]];
    $url = $baseURL . "account/login/";
    $client = new \GuzzleHttp\Client();
    try {
      $response = $client->request('POST', $url, ['multipart' => $authData]);
    } catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
    // Set auth token
    $this->token = 'JWT ' . json_decode($response->getBody()->getContents())->token ;
  }
}

class BaseApi { 
  // Set authData for authentication and base url, We are using Username and Password for authentication
  public $authData = null;
  public $client = null;
  public $url = null;

  // Constructor to initialize client for rest request
  function __construct() {
    $this->client = new \GuzzleHttp\Client();
  }

  // Check response and based on response return data or throw exception
  public function returnData( $response ) {
    // Check and return data based on status code of reponse
    $data = $response->getBody()->getContents();
    return json_decode($data);
  }

  // getAll 
  public function getAll() {
    // Sent GET request
    try {
      $response = $this->client->request('GET', $this->url, ['headers' => ['Authorization' =>  $this->authData->token]]);
    } catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
    // Return data
    return $this->returnData($response);
  }

  // Get perticular id data
	public function get( $id ) {
    try {
      $url = $this->url . $id . "/";
      $response = $this->client->request('GET', $url, ['headers' => ['Authorization' =>  $this->authData->token]]);
    } catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
    // Return data
    return $this->returnData($response);
	}

  // Create new object
	public function create( $data ) {
    try {
		  $response = $this->client->request('POST', $this->url, ['headers' => ['Authorization' =>  $this->authData->token], 'json' => $data]);
    }catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
		// Return data
    return $this->returnData($response);
	}

	public function update( $id, $data ) {
		$url = $this->url . $id . "/";
		try {
      $response = $this->client->request('PATCH', $url, ['headers' => ['Authorization' =>  $this->authData->token], 'json' => $data]);
    }catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
    // Return data
    return $this->returnData($response);
	}
}

class TemplateAPI extends BaseApi {
	/** Wrapper for template api */
   	protected $resource_url = 'xact/template/';
   	function __construct( $authData ) {
        $this->authData = $authData;
        $this->url = $this->authData->baseURL . $this->resource_url;
        parent::__construct();
    }

  /**
   *  Get perticular template raw data
   */
	public function getRawReports( $id ) {
    try {
      $url = $this->url . $id . "/raw_data/";
      $response = $this->client->request('GET', $url, ['headers' => ['Authorization' =>  $this->authData->token]]);
    } catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
    // Return data
    return $this->returnData($response);
  }
  
  /**
   *  Get perticular template statistics data
   */
	public function getStatistics( $id ) {
    try {
      $url = $this->url . $id . "/statistics/";
      $response = $this->client->request('GET', $url, ['headers' => ['Authorization' =>  $this->authData->token]]);
    } catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
    // Return data
    return $this->returnData($response);
	}
}

class TemplateLanguageAPI extends BaseApi {
	/** Wrapper for template language api */
   	protected $resource_url = 'xact/templatelanguage/';
   	function __construct( $authData ) {
        $this->authData = $authData;
        $this->url = $this->authData->baseURL . $this->resource_url;
        parent::__construct();
    }
}

class MessageAPI extends BaseApi {
	/** Wrapper for messgae api */
   	protected $resource_url = 'xact/message/';
   	function __construct( $authData ) {
        $this->authData = $authData;
        $this->url = $this->authData->baseURL . $this->resource_url;
        $this->uploadUrl = $this->url . 'import/';
        parent::__construct();
    }

    /**
     * Upload messages from given file
     */
    public function upload($filePath) {
      $data = [['name' => 'file', 'contents' => fopen($filePath, 'r')]];
      $response = $this->client->request('POST', $this->uploadUrl, ['headers' => ['Authorization' => $this->authData->token], 'multipart' => $data]);
      // Return data
      return $this->returnData($response);
    }
}

class ContentAPI extends BaseApi {
  /** Wrapper for messgae api */
  protected $resource_url = 'content/';
  function __construct( $authData ) {
      $this->authData = $authData;
      $this->url = $this->authData->baseURL . $this->resource_url;
      parent::__construct();
  }

  // Create new object
  public function create( $data ) {
    $response = $this->client->request('POST', $this->url, ['headers' => ['Authorization' => $this->authData->token], 'multipart' => $data]);
    // Return data
    return $this->returnData($response);
  }

  public function update( $id, $data ) {
    $url = $this->url . $id . "/";
    try {
      $response = $this->client->request('PATCH', $url, ['headers' => ['Authorization' => $this->authData->token], 'multipart' => $data]);
    }catch (RequestException $e) {
      throw new Awaazde_Exception($e->getMessage(), $e->getCode());
    }
    // Return data
    return $this->returnData($response);
  }
}

?>
