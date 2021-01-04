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


def create_messages(message_data, file_path, **kwargs):
    """
    :param message_data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
    :type message_data: List of dict
    :param file_path: Path to the folder where the file with created/pending messages are to be kept
    :type file_path: String
    :return: Creates another csv_files in the folder where the csv file was present
            with created and not created messages
    """
    try:
        """
            Schedule messages and create file for created messages and pending messages if any 
        """
        awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)
        created_messages = awaazde_api.messages.create_bulk_in_chunks(message_data, **kwargs)
        CSVUtils.write_csv(created_messages, file_path, file_name="created")

    except Exception as e:
        print e
        logging.error("Error occurred trying to schedule calls:{} ".format(e))


if __name__ == '__main__':
    # Parse the arguments
    args = parse_arguments()
    """
    Step 1: Get Messages from CSV file
    """
    file_path = os.path.dirname(args.matching_messages_file_path)
    headers, message_data = CSVUtils.read_csv(args.matching_messages_file_path)
    """
    Step 2: Create bulk Messages
    """
    created_messages = None
    kwargs = {'transform_using_template': args.use_custom_format}
    create_messages(message_data, file_path, **kwargs)
