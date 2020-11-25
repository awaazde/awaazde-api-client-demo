import argparse
import os
import uuid
from awaazde.constants import CommonConstants, APIConstants
from awaazde.utils import CSVUtils
import logging
from awaazde import AwaazDeAPI


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username", type=str)
    parser.add_argument("password", help="Password", type=str)
    parser.add_argument("organization", help="Organization ", type=str)
    parser.add_argument("csv_file_path", help="Path for the csv ", type=str)
    parser.add_argument('--use_custom_format', type=bool, default=False,
                        help="Set this as True if the messages are of a custom Xact Template")
    args = parser.parse_args()
    return args


def get_next_tag(headers):
    """
    :param headers: list of headers
    :type headers: list
    :return: The next tag field, if the headers has tag1,tag2 returns tag3, If no tag field present returns "tags"
    :rtype: String
    """
    tags = [x for x in headers if x.startswith(CommonConstants.TAG_FIELD)]
    tags = sorted(tags, reverse=True)
    if len(tags) > 0:
        tag_number = int(filter(str.isdigit, str(tags[0])))
        return 'tag{}'.format(tag_number + 1)
    else:
        return CommonConstants.TAGS_FIELD


def create_bulk_messages(headers, message_data, file_path, **kwargs):
    """
    :param headers: Headers of the data
    :type headers: List
    :param message_data: Message data eg: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",template:23,language:"hi"}]
    :type message_data: List of dict
    :param file_path: Path to the folder where the file with created/pending messages are to be kept
    :type file_path: String
    :return: Creates another csv_files in the folder where the csv file was present
            with created and not created messages
    """
    message_request_id = str(uuid.uuid1())
    try:
        """
        Step 1:  Mark the messages sent in this particular request with a unique request
                 is as the next tag,can use this later to check the status of the messages.
        """
        tag = get_next_tag(headers)
        for item in message_data:
            item.update({tag: message_request_id})
        """
        Step 2: Schedule messages and create file for created messages and pending messages if any 
        """
        created_messages = awaazde_api.create_bulk_in_chunks(awaazde_api.messages, message_data, **kwargs)
        CSVUtils.write_csv(created_messages, file_path, file_name="created")

    except Exception as e:
        logging.error(
            "Error occurred trying to schedule calls:{} with message_request_id:{}".format(e, message_request_id))


if __name__ == '__main__':
    # Parse the arguments
    args = parse_arguments()
    awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)
    """
    Step 1: Get Messages from CSV file
    """
    file_path = os.path.dirname(args.csv_file_path)
    headers, message_data = CSVUtils.read_csv(args.csv_file_path)
    """
    Step 2: Create bulk Messages
    """
    created_messages = None
    kwargs = {'use_custom_format': args.use_custom_format}
    create_bulk_messages(headers, message_data, file_path, **kwargs)
