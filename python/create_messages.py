import argparse
import logging
import os

from awaazde import AwaazDeAPI
from awaazde.utils import CSVUtils
from python.awaazde.constants import APIConstants


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username", type=str)
    parser.add_argument("password", help="Password", type=str)
    parser.add_argument("organization", help="Organization ", type=str)
    parser.add_argument("messages_file_path",
                        help="Path for the csv with messages against which we want to check created messages", type=str)
    parser.add_argument('--use_custom_format', action="store_true",
                        help="Include this flag if the messages are of a custom Xact Template")
    return parser.parse_args()


def create_messages(message_data, transform_using_template, **kwargs):
    """
    :param message_data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
    :type: message_data: List of dict
    :param transform_using_template: True ;if It uses a predefined custom xact implementation like XFIN,
                     False;if it is normal XACT.
                     Note: We need to pop send "transform_using_template" as a separate parameter other than "data"because the ad2 api expects it to be a separate parameter,
    :type: transform_using_template:Boolean
    :param: kwargs: Contains a param named "limit" where you specify the size of each batch in which messages are created.
                    If not specified, APIConstants.DEFAULT_BULK_CREATE_LIMIT will be used
    :type: kwargs:Dictionary
    :return: Response from bulk create api(Create objects in chunks based on limit if present,
             takes DEFAULT_BULK_CREATE_LIMIT as default.)
    :rtype: List of dict [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi",status:"created"}}
    """
    try:
        """
            Schedule messages and create file for created messages and pending messages if any 
        """
        awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)
        created_messages = awaazde_api.messages.create_bulk_in_chunks(message_data, transform_using_template, **kwargs)
        return created_messages
    except Exception as e:
        print(e)
        logging.error("Error occurred trying to schedule calls:{} ".format(e))


if __name__ == '__main__':
    # Parse the arguments
    args = parse_arguments()
    """
    Step 1: Get Messages from CSV file
    """
    file_path = os.path.dirname(args.messages_file_path)
    headers, message_data = CSVUtils.read_csv(args.messages_file_path)
    """
    Step 2: Create bulk Messages
    """
    transform_using_template = args.use_custom_format
    kwargs = {'limit': APIConstants.DEFAULT_BULK_CREATE_LIMIT}
    created_messages = create_messages(message_data, transform_using_template, **kwargs)
    """
    Step 3: Write created messages to csv
    """
    CSVUtils.write_csv(created_messages, file_path, file_name="created")
    logging.info("Completed")
