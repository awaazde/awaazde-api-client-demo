/*
 * Copyright (c) 2013 Awaaz.De
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */

package org.xact.client.common;

import java.util.HashMap;
import java.util.Map;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientHandlerException;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.UniformInterfaceException;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.client.filter.HTTPBasicAuthFilter;
import com.sun.jersey.api.client.filter.LoggingFilter;

/**
 * Its a wrapper for sending calls to xact apis. Requester is responsible for sending any request to xact api.
 * @author NIKHIL (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
 *
 */
public class XACTRequester {

	private String x_username; //username which would be used for authentication
	private String x_password; //password for authentication
	private String x_baseurl; //base url where each request would be send, its an optional

	private String x_token; //used in case of token based authentication
	private boolean isTokenbasedAuth = false;

	private Client m_client = null;
	
	private static ObjectMapper objMapper = new ObjectMapper();

	/**
	 * Content types
	 * @author NIKHIL
	 *
	 */
	public static enum ContentFormat {
		APPLICATION_JSON("application/json");
		private String value;
		private ContentFormat(String value) {
			this.value = value;
		}
		public String  getValue() {
			return value;
		}
	}

	/**
	 * Constructor
	 * @param username username using which authentication would be done
	 * @param password password for username
	 * @param baseUrl web service base url
	 */
	public XACTRequester(String username, String password, String baseUrl) {
		this.x_baseurl = baseUrl==null?"http://awaaz.de/console/xact/":baseUrl;
		this.x_username = username;
		this.x_password = password;
	}

	/**
	 * Constructor
	 * @param authToken authentication token
	 */
	public XACTRequester(String authToken) {
		this.x_token = authToken;
		this.isTokenbasedAuth = true;
	}


	/**
	 * Make a get request
	 * @param methodUrl
	 * @return
	 */
	public String get(String methodUrl) throws XACTRequesterException {
		//calling webservice
		WebResource webResource = getClient().resource(x_baseurl + "/" + methodUrl + "/");
		ClientResponse response = webResource.accept(ContentFormat.APPLICATION_JSON.getValue()).get(ClientResponse.class);
		
		String responseText = response.getEntity(String.class);
		if (response.getStatus() != 200)
			throw new XACTRequesterException(responseText, XACTRequesterException.XACTExceptionErrorCode.DATA_GET_ERROR);
		return responseText;
	}
	
	/**
	 * Make a post request
	 * @param methodUrl url
	 * @param data data which needs to be post
	 * @return
	 * @throws XACTRequesterException 
	 */
	public String post(String methodUrl, Map<String, Object> data) throws XACTRequesterException {
		String responseText = null;
		try {
			WebResource webResource = getClient().resource(x_baseurl + "/" + methodUrl + "/");
			ClientResponse response;
			response = webResource.accept(ContentFormat.APPLICATION_JSON.getValue()).type(ContentFormat.APPLICATION_JSON.getValue()).post(ClientResponse.class, XACTRequester.objMapper.writeValueAsString(data));
			responseText = response.getEntity(String.class);
			if (response.getStatus() != 201)
				throw new XACTRequesterException(responseText, XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		} catch (UniformInterfaceException e) {
			throw new XACTRequesterException(e.getLocalizedMessage(), XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		} catch (ClientHandlerException e) {
			throw new XACTRequesterException(e.getLocalizedMessage(), XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		} catch (JsonProcessingException e) {
			throw new XACTRequesterException(e.getLocalizedMessage(), XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		}
		return responseText;
	}
	
	
	/**
	 * Make a put request
	 * @param methodUrl url
	 * @param data data which needs to be post
	 * @return
	 * @throws XACTRequesterException 
	 */
	public String put(String methodUrl, Map<String, Object> data) throws XACTRequesterException {
		String responseText = null;
		try {
		WebResource webResource = getClient().resource(x_baseurl + "/" + methodUrl + "/");
		ClientResponse response = webResource.accept(ContentFormat.APPLICATION_JSON.getValue()).type(ContentFormat.APPLICATION_JSON.getValue()).put(ClientResponse.class, XACTRequester.objMapper.writeValueAsString(data));
		responseText = response.getEntity(String.class);
		if (response.getStatus() != 200)
			throw new XACTRequesterException(responseText, XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		} catch (UniformInterfaceException e) {
			throw new XACTRequesterException(e.getLocalizedMessage(), XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		} catch (ClientHandlerException e) {
			throw new XACTRequesterException(e.getLocalizedMessage(), XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		} catch (JsonProcessingException e) {
			throw new XACTRequesterException(e.getLocalizedMessage(), XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		}
		return responseText;
	}
	
	/**
	 * Make a delete request
	 * @param methodUrl url
	 * @param data data which needs to be post
	 * @return
	 * @throws XACTRequesterException 
	 */
	public boolean delete(String methodUrl) throws XACTRequesterException {
		WebResource webResource = getClient().resource(x_baseurl + "/" + methodUrl + "/");
		ClientResponse response = webResource.accept(ContentFormat.APPLICATION_JSON.getValue()).delete(ClientResponse.class);
		if (response.getStatus() != 204) {
			String responseText = response.getEntity(String.class);
			throw new XACTRequesterException(responseText, XACTRequesterException.XACTExceptionErrorCode.DATA_POST_ERROR);
		}
		return true;
	}

	/**
	 * Returns jersey client to make any call to webservice 
	 * @return
	 */
	private Client getClient() {
		if(m_client == null) {
			m_client = new Client();
			if(!isTokenbasedAuth) {
				final HTTPBasicAuthFilter authFilter = new HTTPBasicAuthFilter(x_username, x_password);
				m_client.addFilter(authFilter);
				m_client.addFilter(new LoggingFilter());
			} else {
				//TODO for token based authentication
			}
		}

		return m_client;
	}
}
