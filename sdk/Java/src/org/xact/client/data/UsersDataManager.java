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
 * Users Data manager will help to deal with user data
 * @author NIKHIL (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
 *
 */
public class UsersDataManager extends DataManager { 
	
	private static final String CALL_METHOD_NAME = "user";
	//requester
	private XACTRequester x_requester;
	//Objectmapper
	private static ObjectMapper objMapper = new ObjectMapper();
	
	public UsersDataManager(XACTRequester requester) {
		this.x_requester = requester;
	}

	@Override
	public Collection<Map<String, Object>> getAll() throws XACTDataException {
		Collection<Map<String, Object>> callData = new ArrayList<Map<String,Object>>();
		try {
			String responseJson = x_requester.get(CALL_METHOD_NAME);
			callData = objMapper.readValue(responseJson, ArrayList.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		return callData;
	}

	@Override
	public Map<String, Object> get(String objectId) throws XACTDataException {
		Map<String, Object> callData = new HashMap<String,Object>();
		try {
			String responseJson = x_requester.get(CALL_METHOD_NAME + "/" + objectId);
			callData = objMapper.readValue(responseJson, HashMap.class); 
		}  catch(XACTRequesterException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getErrorCode());
		} catch (JsonParseException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (JsonMappingException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		} catch (IOException e) {
			throw new XACTDataException(e.getLocalizedMessage(), e.getMessage());
		}
		return callData;
	}

	@Override
	public Map<String, Object> create(Map<String, Object> objectData) throws XACTDataException {
		throw new UnsupportedOperationException("Creating of new user through web service is not available for now");
	}

	@Override
	public Map<String, Object> modify(String objectId, Map<String, Object> objectData) throws XACTDataException {
		throw new UnsupportedOperationException("Editing of user through web service is not available for now");	}

	@Override
	public boolean delete(String objectId) throws XACTDataException {
		throw new UnsupportedOperationException("Deleting of user through web service is not available for now");
	}
}
