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

import java.io.File;
import java.util.HashMap;
import java.util.Map;

import org.xact.client.common.XACTRequester;
import org.xact.client.data.CallDataManager;
import org.xact.client.data.TemplatesDataManager;
import org.xact.client.data.UsersDataManager;
import org.xact.client.data.WebhookManager;

/**
 * It demonstrate on how to call xact apis
 * @author NIKHIL (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
 *
 */
public class XACTClientDemo {

	public static String USERNAME = "<provide your username here>";
	public static String PASSWORD = "<provide your pass here>";
	
	public static String BASE_URL = "https://awaaz.de/console/xact";
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		System.setProperty("jsse.enableSNIExtension", "false");
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
			//System.out.println(tmpltDataMgr.getAll());
			
			//getting specific template data
			//System.out.println(tmpltDataMgr.get("1"));
			
			//creating new template
			Map<String, Object> template_data  = new HashMap<String, Object>();
			template_data.put("text", "This is demo");
			template_data.put("language", "eng");
			String [] vocabulary = { "msg1", "msg2" };
			template_data.put("vocabulary", vocabulary);
			
			System.out.println(tmpltDataMgr.create(template_data));
			
			//updating template
			template_data.put("text", "This is demo - updated");
			System.out.println(tmpltDataMgr.modify("51", template_data));
			
			// template file upload
			// uploading file object
			File fileToUpload = new File("/home/nikhil/apps/awaazde-api-client-sdk/sdk/php/msg1.wav");
			System.out.println(tmpltDataMgr.upload_file("51", fileToUpload));
			
			//uploading file via url
			String file_url = "http://www.pacdv.com/sounds/voices/come-on-1.wav";
			System.out.println(tmpltDataMgr.upload_file_url("51", file_url));
			
			//deleting template
			System.out.println(tmpltDataMgr.delete("51"));
			
			
			//getting users detail
			UsersDataManager usrDataMgr = new UsersDataManager(requester);
			System.out.println(usrDataMgr.getAll());
			
			//getting specific user detail
			System.out.println(usrDataMgr.get("2"));
			
			
			//webhook
			WebhookManager whManager = new WebhookManager(requester);
			System.out.println(whManager.getAll());
			
			//getting specific webhook
			System.out.println(whManager.get("1"));
			
			//creating new
			Map<String, Object> webhook_data  = new HashMap<String, Object>();
			webhook_data.put("url", "https://awaaz.de/webhook");
			System.out.println(whManager.create(webhook_data));
			
			//updating
			webhook_data.put("url", "https://awaaz.de/webhook/2/");
			System.out.println(whManager.modify("3", webhook_data));
			
			//deleting
			System.out.println(whManager.delete("3"));
			
		} catch(Exception e) {
			e.printStackTrace();
		}

	}

}
