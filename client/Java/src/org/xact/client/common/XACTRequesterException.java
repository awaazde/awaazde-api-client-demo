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

/**
 * Its an exception class for requester
 * @author NIKHIL (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
 *
 */
public class XACTRequesterException extends Exception {
	
	/**
	 * Error codes
	 *
	 */
	public static interface XACTExceptionErrorCode {
		public static String DATA_GET_ERROR 	= "1001";
		public static String DATA_POST_ERROR 	= "1002";
		public static String DATA_PUT_ERROR 	= "1003";
		public static String DATA_DELETE_ERROR 	= "1004";
	}
	
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	//exception error code
	private String errorCode="Unknown_Exception";
	
	public XACTRequesterException(String message, String errorCode){
        super(message);
        this.errorCode = errorCode;
    }
    
	/**
	 * Returns error code
	 * @return
	 */
    public String getErrorCode(){
        return this.errorCode;
    }
	
}
