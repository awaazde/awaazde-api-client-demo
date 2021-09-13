import argparse
import logging
import os

from awaazde import AwaazDeAPI
from awaazde.utils import CSVUtils


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


def create_messages(message_data, **kwargs):
    """
    :param message_data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
    :type message_data: List of dict
    :return: created messages from the message data.
    :type created_messages: List of dict
    """
    try:
        """
            Schedule messages and create file for created messages and pending messages if any 
        """
        awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)
        created_messages = awaazde_api.messages.create_bulk_in_chunks(message_data, **kwargs)
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
    kwargs = {'transform_using_template': args.use_custom_format}
    created_messages = create_messages(message_data, **kwargs)
    """
    Step 3: Write created messages to csv
    """
    CSVUtils.write_csv(created_messages, file_path, file_name="created")
