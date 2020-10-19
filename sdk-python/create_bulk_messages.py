import argparse
import os
import uuid
import pandas as pd
from awaazde.constants import CommonConstants
from awaazde.models import Message
from awaazde.utils import ADMessageUtils

message_data = ''


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username", type=str)
    parser.add_argument("password", help="Password", type=str)
    parser.add_argument("organization", help="Organization ", type=str)
    parser.add_argument("csv_file_path", help="Path for the csv ", type=str)
    args = parser.parse_args()
    return args


def pick_messages_from_file(csvFilePath):
    df = pd.read_csv(csvFilePath, encoding="ISO-8859-1")
    message_data = df.replace({pd.np.nan: None})
    headers = df.head()
    message_data = message_data.to_dict('records')
    message_data = Message(message_data)
    return headers, message_data


def get_last_tag(headers):
    tags = [x for x in headers if x.startswith(CommonConstants.TAG_FIELD)]
    tags = sorted(tags, reverse=True)
    if len(tags) > 0:
        p = int(filter(str.isdigit, str(tags[0])))
        return 'tag{}'.format(p + 1)
    else:
        return CommonConstants.TAGS_FIELD


def schedule_calls(csv_file_path):
    message_data = Message()
    created_messages = None
    limit = CommonConstants.AD_MESSAGE_SCHEDULE_LIMIT
    message_request_id = str(uuid.uuid1())
    file_path = os.path.dirname(csv_file_path)

    try:
        headers, message_data = pick_messages_from_file(csv_file_path)
        print message_data
        tag = get_last_tag(headers)
        for item in message_data:
            item.update({tag: message_request_id})
        #for chunk in messages_manager.process_iterable_in_chunks(message_data, limit):
            #created_messages = messages_manager.schedule_bulk_messages(chunk)
    except Exception as e:
        print "Error occurred: " + str(e)

    if created_messages:
        messages_manager.create_csv_file(created_messages, file_path, file_name="created")
    else:
        created, not_created = messages_manager.check_created_message(message_data, {"tags": message_request_id})
        messages_manager.create_csv_file(created, file_path, file_name="created")
        messages_manager.create_csv_file(not_created, file_path, file_name="pending")


if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()
    username = args.__dict__['username']
    password = args.__dict__['password']
    organization = args.__dict__['organization']
    csv_file_path = args.__dict__['csv_file_path']

    messages_manager = ADMessageUtils(organization, username, password)
    schedule_calls(csv_file_path)
