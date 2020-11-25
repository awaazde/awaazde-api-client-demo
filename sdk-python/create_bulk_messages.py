import argparse
import os
import uuid
from awaazde.constants import CommonConstants, APIConstants
from awaazde.utils import APIUtils, CSVUtils
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


def create_bulk_messages(headers, message_data, file_path):
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
    ad_manager = APIUtils()
    try:
        """
        Step 1:  Mark the messages sent in this particular request with a unique request
                 is as the next tag,can use this later to check the status of the messages.
        """
        tag = get_next_tag(headers)
        for item in message_data:
            item.update({tag: message_request_id})
        """
        Step 2: Schedule messages and  Create file for created messages and pending messages if any 
        """
        kwargs = {'limit': args.limit, 'use_custom_format': args.transform_with_template}
        created_messages = ad_manager.create_bulk_in_chunks(awaazde_api.messages, message_data, **kwargs)
        CSVUtils.write_csv(created_messages, file_path, file_name="created")

    except Exception as e:
        logging.error("Error occurred trying to schedule calls : {}".format(e))
        logging.error("Creating Files for created and pending messages")
        params = {"tags": message_request_id, 'page': APIConstants.DEFAULT_BULK_CREATE_LIMIT, 'fields': (
            CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD)}

        responses = ad_manager.list_depaginated(awaazde_api.messages, params)
        response_dict = {[response[CommonConstants.PHONE_NUMBER_FIELD]] for response in responses}
        filtered, remainder = [], []
        for idx, datum in enumerate(message_data):
            response = filtered if datum.get(CommonConstants.PHONE_NUMBER_FIELD) in response_dict else remainder
            response.append(idx)

        CSVUtils.write_csv(filtered, file_path, file_name="created")
        CSVUtils.write_csv(remainder, file_path, file_name="pending")


if __name__ == '__main__':
    # Parse the arguments
    args = parse_arguments()
    username = args.__dict__['username']
    password = args.__dict__['password']
    organization = args.__dict__['organization']
    csv_file_path = args.__dict__['csv_file_path']
    transform_using_template = args.__dict__['transform_using_template']
    api_manager = APIUtils()
    awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)

    """
    Step 1: Get Messages from CSV file
    """
    file_path = os.path.dirname(csv_file_path)
    headers, message_data = CSVUtils.read_csv(csv_file_path)

    """
    Step 2: Create bulk Messages
    """
    created_messages = None
    create_bulk_messages(headers, message_data, file_path)
