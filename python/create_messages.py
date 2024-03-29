import argparse
import logging
import os

from awaazde import AwaazDeAPI
from awaazde.utils import CSVUtils
from awaazde.constants import APIConstants


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username", type=str)
    parser.add_argument("password", help="Password", type=str)
    parser.add_argument("organization", help="Organization ", type=str)
    parser.add_argument("messages_file_path",
                        help="Path for the csv with messages against which we want to check created messages", type=str)
    return parser.parse_args()


def create_messages(message_data,  **kwargs):
    """
    :param message_data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
    :type: message_data: List of dict
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
        awaazde_api.messages.create_bulk_and_save_in_chunks(message_data, **kwargs)
        
    except Exception as e:
        print(e)
        logging.error("Error occurred trying to schedule calls:{} ".format(e))


if __name__ == '__main__':
    # Parse the arguments
    args = parse_arguments()
    """
    Step 1: Get Messages from CSV file
    """
    if os.path.exists(args.messages_file_path):
        file_path = args.messages_file_path
    else:
        print("File path don't exists")
    headers, message_data = CSVUtils.read_csv(args.messages_file_path)
    """
    Step 2: Create bulk Messages
    """
    kwargs = {'limit': APIConstants.DEFAULT_BULK_CREATE_LIMIT}
    kwargs = {'file_path':file_path}

    create_messages(message_data, **kwargs)

    print("Completed")
