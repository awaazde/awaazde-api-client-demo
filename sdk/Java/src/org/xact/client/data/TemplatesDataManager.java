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

package org.xact.client.data;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import org.xact.client.common.XACTRequester;
import org.xact.client.common.XACTRequesterException;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Templates Data manager will help to deal with templates data
 * @author NIKHIL (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
 *
 */
public class TemplatesDataManager extends DataManager { 
	
	private static final String TEMPLATE_METHOD_NAME = "templates";
	private static final String TEMPLATE_FILE_METHOD_NAME = "files";
	//requester
	private XACTRequester x_requester;
	//Objectmapper
	private static ObjectMapper objMapper = new ObjectMapper();
	
	public TemplatesDataManager(XACTRequester requester) {
		this.x_requester = requester;
	}

	@Override
	public Collection<Map<String, Object>> getAll() throws XACTDataException {
		Collection<Map<String, Object>> templateData = new ArrayList<Map<String,Object>>();
		try {
			String responseJson = x_requester.get(TEMPLATE_METHOD_NAME);
			templateData = objMapper.readValue(responseJson, ArrayList.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		return templateData;
	}

	@Override
	public Map<String, Object> get(String objectId) throws XACTDataException {
		Map<String, Object> templateData = new HashMap<String,Object>();
		try {
			String responseJson = x_requester.get(TEMPLATE_METHOD_NAME + "/" + objectId);
			templateData = objMapper.readValue(responseJson, HashMap.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		return templateData;
	}

	@Override
	public Map<String, Object> create(Map<String, Object> objectData) throws XACTDataException {
		Map<String, Object> templateData = new HashMap<String,Object>();
		
		try {
			String responseJson = x_requester.post(TEMPLATE_METHOD_NAME + "/", objectData);
			templateData = objMapper.readValue(responseJson, HashMap.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		return templateData;
	}

	@Override
	public Map<String, Object> modify(String objectId, Map<String, Object> objectData) throws XACTDataException {
		
		Map<String, Object> templateData = new HashMap<String,Object>();
		
		try {
			String responseJson = x_requester.put(TEMPLATE_METHOD_NAME + "/" + objectId, objectData);
			templateData = objMapper.readValue(responseJson, HashMap.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		return templateData;
	}
	
	@Override
	public boolean delete(String objectId) throws XACTDataException {
		try {
			return x_requester.delete(TEMPLATE_METHOD_NAME + "/" + objectId);
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		}
	}
	
	public Map<String, Object> upload_file_url(String objectId, String file_url) throws XACTDataException {
		Map<String, Object> templateFileData = new HashMap<String,Object>();
		
		Map<String, Object> request_data  = new HashMap<String, Object>();
		request_data.put("template_id", objectId);
		request_data.put("file_url", file_url);
		
		try {
			String responseJson = x_requester.post(TEMPLATE_METHOD_NAME + "/" + objectId + "/" + TEMPLATE_FILE_METHOD_NAME, request_data);
			templateFileData = objMapper.readValue(responseJson, HashMap.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		
		return templateFileData;
	}

	public Map<String, Object> upload_file(String objectId, File file) throws XACTDataException {
		Map<String, Object> templateFileData = new HashMap<String,Object>();
		
		Map<String, Object> request_data  = new HashMap<String, Object>();
		request_data.put("template_id", objectId);
		
		try {
			String responseJson = x_requester.postWithFile(TEMPLATE_METHOD_NAME + "/" + objectId + "/" + TEMPLATE_FILE_METHOD_NAME, request_data, file);
			templateFileData = objMapper.readValue(responseJson, HashMap.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		
		return templateFileData;
	}
}
