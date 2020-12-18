# utils.py
#
# import csv
# import logging
# import urlparse
#
# import pandas as pd
# from datetime import datetime
# from constants import CommonConstants, APIConstants
#
# from . import AwaazDeAPI
#
#
# class APIUtils(AwaazDeAPI):
#     def __init__(self, org, user, password):
#         """
#         Initialize Awaazde Authentication and Call Manager
#         :return:
#         """
#         self.awaazde_api = AwaazDeAPI(org, user, password)
#
#     def get_list_depaginated(api, params=None):
#         """
#             Gets all messages from awaazde API based on the filters passed
#         """
#
#     data = []
#     response = api.list(params=params)
#     while response.get('next'):
#         # Get next page URL
#         next_page_url = response['next']
#         filters['page'] = urlparse.parse_qs(urlparse.urlparse(next_page_url).query)['page'][0]
#         # And then we request for the data on the next page
#         response = self.api_map.get(api).list(params=params)
#
#     if response:
#         data.extend(response['results'])
#     else:
#         logging.error("Error in Fetching Results")
#
#     return data
#
#     def create_bulk_in_chunks(self, api, data, limit=None):
#         """
#         Create messages in chunks based on limit if present, takes DEFAULT_BULK_CREATE_LIMIT as default.
#         :param api:
#         :type api:
#         :param Data: Data to create. eg: if messages: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi"}]
#         :type Data: List of dict
#         :param limit: Number of messages to create in one chunked request
#         :type limit: integer
#         :return: Response from bulk create api
#         :rtype: List of dict [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi",status:"created"}}
#         """
#         if not limit:
#             limit = CommonConstants.DEFAULT_BULK_CREATE_LIMIT
#         data = {'data': data}
#         response = []
#         for data_chunk in CommonUtils.process_iterable_in_chunks(data, limit):
#             response += self.api_map.get(api).create_bulk(data_chunk)
#         return response
#
#     def filter_data(self, api, data, match_criteria, filter_criteria, response_fields):
#         """
#         This method will lookup to check how much of the is present in the system for the given data matching the filter criteria
#         Eg: Given a list of messages, Use this method to check how many of these messages have been created on 9th october.
#         :param api: The app for which we want to make the request.
#         :type api: String, Use any one api From the following ["message_api", "content_api", "template_api","template_language_api"]
#         :param data:  Source list of data against which we need to apply the filter
#         :type data: List of dict
#         :param match_criteria: Field value which should be matched to compare the given data against the retrived data
#         :type match_criteria: String, Eg: phone_number, since if msg_id is same in both given and retrieved data,
#                               we can count it as the same data
#         :param filter_criteria: All the filters that the data needs to be checked against.
#         :type filter_criteria: dict Eg: {phone_number:909090909090,msg_request_id:"32344IOWEPOWEWE"}
#         :param response_fields: All the fields we need When retrieving data from request.
#         :type response_fields: List eg: [phone_number,id,send_on]
#         :return: The source data will be divided into two chunks, and they will be returned, The data that passed the filtered criteria
#                 and the ones that didn't
#         :rtype: List of dicts.[{phone_number:8929292929,send_on:"2020-09-09 00:00:00",id:"12"}]
#         """
#         params = {}
#         filtered = []
#         remainder = []
#         for filter_field, filter_value in filter_criteria.items():
#             params[filter_field] = filter_value
#
#         params['page'] = APIConstants.DEFAULT_BULK_CREATE_LIMIT
#         params['fields'] = response_fields
#
#         filtered_api_data = self.list_depaginated(api, params)
#         filtered_responses = [response[match_criteria] for response in responses]
#         filtered, remainder = [], []
#         for idx, datum in enumerate(data):
#             response = filtered if datum.get(match_criteria) in response_dict else remainder
#             response.append(idx)
#
#         return filtered, remainder
#
#
# class CommonUtils(object):
#
#     @staticmethod
#     def process_iterable_in_chunks(iterable, chunk_size=CommonConstants.DEFAULT_CHUNK_SIZE):
#         '''
#         A convenience method for processing a list/queryset of objects in chunks
#         pattern stolen from https://stackoverflow.com/a/29708603/199754
#
#         :param iterable: list or queryset of objects
#         :param chunk_size: max number of objects to process in one iteration
#         :return: None
#         '''
#         offset = 0
#         chunk = iterable[offset:offset + chunk_size]
#         while chunk:
#             yield chunk  # body executes here
#
#             # increment the iterable
#             offset += chunk_size
#             chunk = iterable[offset:offset + chunk_size]
#
#
# class CSVUtils(object):
#     @staticmethod
#     def write_csv(data, file_path, file_name):
#         if data:
#             keys = data[0].keys()
#             with open('{}/{}.csv'.format(file_path, file_name),
#                       'w')  as output_file:
#                 writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
#                 writer.writeheader()
#                 writer.writerows(data)
#
#     @staticmethod
#     def read_csv(csv_file_path):
#         df = pd.read_csv(csv_file_path, encoding="ISO-8859-1")
#         headers = df.head()
#         data = df.to_dict('records')
#         return headers, data
#
#
# create_bulk_messages.py
# import argparse
# import os
# import uuid
# from awaazde.constants import CommonConstants, APIConstants
# from awaazde.utils import APIUtils, CSVUtils
# import logging
#
#
# def parseArguments():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("username", help="Username", type=str)
#     parser.add_argument("password", help="Password", type=str)
#     parser.add_argument("organization", help="Organization ", type=str)
#     parser.add_argument("csv_file_path", help="Path for the csv ", type=str)
#     args = parser.parse_args()
#     return args
#
#
# def get_next_tag(headers):
#     """
#     :param headers: list of headers
#     :type headers: list
#     :return: The next tag field, if the headers has tag1,tag2 returns tag3, If no tag field present returns "tags"
#     :rtype: String
#     """
#     tags = [x for x in headers if x.startswith(CommonConstants.TAG_FIELD)]
#     tags = sorted(tags, reverse=True)
#     if len(tags) > 0:
#         tag_number = int(filter(str.isdigit, str(tags[0])))
#         return 'tag{}'.format(tag_number + 1)
#     else:
#         return CommonConstants.TAGS_FIELD
#
#
# def create_bulk_messages(headers, message_data, file_path):
#     """
#     :param headers: Headers of the data
#     :type headers: List
#     :param message_data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
#     :type message_data: List of dict
#     :param file_path: Path to the folder where the file with created/pending messages are to be kept
#     :type file_path: String
#     :return: Creates another csv_files in the folder where the csv file was present
#             with created and not created messages
#     """
#     message_request_id = str(uuid.uuid1())
#     try:
#         """
#         Step 1:  Mark the messages sent in this particular request with a unique request
#                  is as the next tag,can use this later to check the status of the messages.
#         """
#         tag = get_next_tag(headers)
#         for item in message_data:
#             item.update({tag: message_request_id})
#         """
#         Step 2: Schedule messages and  Create file for created messages and pending messages if any
#         """
#         created_messages = ad_manager.bulk_create_in_chunks(APIConstants.MESSAGE_API, message_data)
#         CSVUtils.write_csv(created_messages, file_path, file_name="created")
#
#     except Exception as e:
#         logging.error("Error occurred trying to schedule calls : {}".format(e))
#
#         logging.error("Creating Files for created and pending messages:{}")
#         match_criteria = CommonConstants.PHONE_NUMBER_FIELD
#         filter_fields = {"tags": message_request_id}
#         response_fields = CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD
#         created, not_created = ad_manager.filter_data(api_manager.awaazde_api.messages, message_data, match_criteria,
#                                                       filter_fields, response_fields)
#         CSVUtils.write_csv(created, file_path, file_name="created")
#         CSVUtils.write_csv(not_created, file_path, file_name="pending")
#
#
# if __name__ == '__main__':
#     # Parse the arguments
#     args = parseArguments()
#     username = args.__dict__['username']
#     password = args.__dict__['password']
#     organization = args.__dict__['organization']
#     csv_file_path = args.__dict__['csv_file_path']
#     ad_manager = APIUtils(organization, username, password)
#
#     """
#     Step 1: Get Messages from CSV file
#     """
#     file_path = os.path.dirname(csv_file_path)
#     headers, message_data = CSVUtils.read_csv(csv_file_path)
#
#     """
#     Step 2: Create bulk Messages
#     """
#     created_messages = None
#     create_bulk_messages(headers, message_data, file_path)
#
# filter_messages.py
# cimport
# argparse
# from datetime import datetime
# from awaazde.constants import CommonConstants, APIConstants
# from awaazde.utils import APIUtils, CSVUtils
#
#
# def parseArguments():
#     parser = argparse.ArgumentParser(
#         description='Check which Messages are already present in the system based on the filters')
#     parser.add_argument('username', type=str, help='Username of the tenant')
#     parser.add_argument('password', type=str, help='Password of the tenant')
#     parser.add_argument('organization', type=str, help='Organization of the tenant')
#     parser.add_argument('message_data_file_path', type=str, help='Path for the csv which contains message data')
#     parser.add_argument('--filters', type=str,
#                         help='Filters to be applied in the form: {"send_on__gt":"10-12-2020",'
#                              '"send_on__lt":"10-12-2020","tags":"dummy_tag"}')
#
#
# parser.add_argument('--match_criteria', type=str,
#                     help='Field to use when matching User record with the queried resultant record',
#                     default=CommonConstants.MESSAGE_ID)
#
# return args
#
# if __name__ == '__main__':
#     """
#         Step 1 : Parse the arguments
#     """
#     args = parseArguments()
#     headers, message_data = CSVUtils.read_csv(args.path)
#
#     """
#         Step 2 : Send an api filter request and gather the created messages and separate the not created messags   """
#
#     ad_manager = APIUtils(args.organization, args.username, args.password)
#     response_fields = CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD
#     filtered, remainder = ad_manager.filter_data(APIConstants.MESSAGE_API, message_data, args.match_criteria,
#                                                  args.filters, response_fields)
#
#     """
#         Step 3:  Dump the data in a file for the user
#     """
#     CSVUtils.write_csv(filtered, args.path, file_name="filtered_{}".format(datetime.now().timestamp()))
#     CSVUtils.write_csv(remainder, args.path, file_name="remainder_{}".format(datetime.now().timestamp()))
#
#
#
