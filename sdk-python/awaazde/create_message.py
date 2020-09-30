import argparse
import os
import uuid

import pandas as pd
import csv

from utils import ADMessageUtils
from constants import CommonConstants

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

    return headers, message_data


def get_last_tag(headers):
    tags = [x for x in headers if x.startswith(CommonConstants.TAG_FIELD)]
    tags = sorted(tags, reverse=True)
    if len(tags) > 0:
        p = int(filter(str.isdigit, str(tags[0])))
        return 'tag{}'.format(p + 1)
    else:
        return CommonConstants.TAGS_FIELD


def drop_messages_to_file(message_data, file_path, file_name):
    if message_data:
        keys = message_data[0].keys()
        with open('{}/{}.csv'.format(file_path, file_name),
                  'w')  as output_file:
            writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(message_data)


def schedule_calls(csv_file_path):
    message_data = None
    created_messages = None
    limit = CommonConstants.AD_MESSAGE_SCHEDULE_LIMIT
    message_request_id = str(uuid.uuid1())
    file_path = os.path.dirname(csv_file_path)
    print"FILE PATH", file_path
    # try:
    headers, message_data = pick_messages_from_file(csv_file_path)
    tag = get_last_tag(headers)
    for item in message_data:
        item.update({tag: message_request_id})
    for chunk in messages_manager.process_iterable_in_chunks(message_data, limit):
        created_messages = messages_manager.schedule_ad_messages(chunk)

    # except Exception as e:
    #     print "Error occurred: " + str(e)

    if created_messages:
        drop_messages_to_file(created_messages, file_path, file_name="created")
    else:
        created, not_created = messages_manager.check_created_message(message_data, {"tags": message_request_id})
        drop_messages_to_file(created, file_path, file_name="created")
        drop_messages_to_file(not_created, file_path, file_name="pending")


if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()
    username = args.__dict__['username']
    password = args.__dict__['password']
    organization = args.__dict__['organization']
    csv_file_path = args.__dict__['csv_file_path']

    messages_manager = ADMessageUtils(organization, username, password)
    schedule_calls(csv_file_path)
