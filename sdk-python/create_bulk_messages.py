import argparse
import os
import uuid
from awaazde.constants import CommonConstants
from awaazde.utils import ADUtils, CSVUtils, CommonUtils
import logging


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username", type=str)
    parser.add_argument("password", help="Password", type=str)
    parser.add_argument("organization", help="Organization ", type=str)
    parser.add_argument("csv_file_path", help="Path for the csv ", type=str)
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


def schedule_calls(csv_file_path):
    """
    :param csv_file_path: Path to the csv file where messages to be sent are present
    :type csv_file_path: String
    :return: Creates another csv_files in the folder where the csv file was present
            with created and not created messages
    """
    ad_manager = ADUtils(organization, username, password)
    created_messages = None
    limit = CommonConstants.AD_MESSAGE_SCHEDULE_LIMIT
    message_request_id = str(uuid.uuid1())
    file_path = os.path.dirname(csv_file_path)
    try:
        """
        Step 1: Get Messages from CSV file
        """
        headers, message_data = CSVUtils.parse_csv(csv_file_path)

        """
        Step 2:  Mark the messages sent in this particular request with a unique request
                 is as the next tag, use this later to check the status of the messages.
        """
        tag = get_next_tag(headers)
        for item in message_data:
            item.update({tag: message_request_id})
        """
        Step 3: Schedule messages in chunks
        """
        ad_manager.bulk_create_in_chunks(message_data, limit)
        scheduling_completed = True

    except Exception as e:
        scheduling_completed = False
        logging.error("Error occurred trying to schedule calls : {}".format(e))

        """
        Step 4: Create file for created messages and pending messages if any.
        """
    if scheduling_completed:
        CSVUtils.create_csv(created_messages, file_path, file_name="created")
    else:
        created, not_created = ad_manager.check_created_message(message_data, {"tags": message_request_id})
        CSVUtils.create_csv(created, file_path, file_name="created")
        CSVUtils.create_csv(not_created, file_path, file_name="pending")


if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()
    username = args.__dict__['username']
    password = args.__dict__['password']
    organization = args.__dict__['organization']
    csv_file_path = args.__dict__['csv_file_path']
    schedule_calls(csv_file_path)
