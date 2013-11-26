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

import java.util.Map;

/**
 * Abstract data manager class
 * @author NIKHIL (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
 *
 */
public abstract class DataManager {

	/**
	 * Returns all objects
	 * @return list of objects
	 */
	public abstract Object getAll() throws XACTDataException;
	
	/**
	 * Returns specific object data
	 * @param objectId object id e.g. call id or template id
	 * @return
	 */
	public abstract Object get(String objectId) throws XACTDataException;
	
	/**
	 * Creates new object
	 * @param objectData object data using which object would be created
	 * @return id of newly created object
	 */
	public abstract Map<String, Object> create(Map<String, Object> objectData) throws XACTDataException;
	
	/**
	 * Modifies new object
	 * @param objectData object data using which object would be modified
	 * @return id of newly created object
	 */
	public abstract Map<String, Object> modify(String objectId, Map<String, Object> objectData) throws XACTDataException;
	
	/**
	 * Creates new object
	 * @param objectId object id e.g. call id or template id
	 * @return boolean indicates whether object has been deleted or not
	 */
	public abstract boolean delete(String objectId) throws XACTDataException;
}
