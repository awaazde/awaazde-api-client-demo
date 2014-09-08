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
package org.xact.client;

import java.util.HashMap;
import java.util.Map;

import org.xact.client.common.XACTRequester;
import org.xact.client.data.CallDataManager;
import org.xact.client.data.TemplatesDataManager;
import org.xact.client.data.UsersDataManager;

/**
 * It demonstrate on how to call xact apis
 * @author NIKHIL (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
 *
 */
public class XACTClientDemo {

	public static String USERNAME = "<provide your username here>";
	public static String PASSWORD = "<provide your pass here>";
	
	public static String BASE_URL = "https://awaaz.de/console/xact/";
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		try {
			//Creates XACTRequester object to call any api
			XACTRequester requester = new XACTRequester(USERNAME, PASSWORD, BASE_URL);

			//getting call information
			CallDataManager callDataMgr = new CallDataManager(requester);
			System.out.println(callDataMgr.getAll());

			Map<String, Object> data  = new HashMap<String, Object>();
			data.put("recipient", "0123456789"); //phone number
			data.put("text", "You have 99 elephants waiting at awaaz");
			data.put("send_on", "2013-11-30T14:32:00");

			//creating new call
			System.out.println(callDataMgr.create(data));
			
			//getting specific call information
			System.out.println(callDataMgr.get("11"));
			
			System.out.println(callDataMgr.modify("32", data));
			System.out.println(callDataMgr.delete("33"));
			
			//getting templates detail
			TemplatesDataManager tmpltDataMgr = new TemplatesDataManager(requester);
			System.out.println(tmpltDataMgr.getAll());
			
			//getting specific template data
			System.out.println(tmpltDataMgr.get("1"));
			
			//getting users detail
			UsersDataManager usrDataMgr = new UsersDataManager(requester);
			System.out.println(usrDataMgr.getAll());
			
			//getting specific user detail
			System.out.println(usrDataMgr.get("2"));
			
		} catch(Exception e) {
			e.printStackTrace();
		}

	}

}
