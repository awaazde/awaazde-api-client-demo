import argparse
import uuid

import pandas as pd

from sdk import AwaazDeAPI, APIException
import csv

from utils import ADMessageUtils

message_data = ''


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username", type=str)
    parser.add_argument("password", help="Password", type=str)
    parser.add_argument("organization", help="Organization ", type=str)
    parser.add_argument("path", help="Path for the csv ", type=str)
    args = parser.parse_args()
    return args


def pick_messages_from_file(csvFilePath):
    df = pd.read_csv(csvFilePath, encoding="ISO-8859-1")
    message_data = df.replace({pd.np.nan: None})
    headers = df.head()
    message_data = message_data.to_dict('records')

    return headers, message_data


def get_last_tag(headers):
    tags = [x for x in headers if x.startswith('tag')]
    tags = sorted(tags, reverse=True)
    if len(tags) > 0:
        p = int(filter(str.isdigit, str(tags[0])))
        return 'tag{}'.format(p + 1)
    else:
        return "tags"


def drop_messages_to_file(message_data, file_name):
    if message_data:
        keys = message_data[0].keys()
        path_to_folder = '/Users/ashwini/AD/scripts_for_stuff/cs_python_script/output_folder'
        with open('{}/{}.csv'.format(path_to_folder,file_name),
                  'w')  as output_file:
            writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(message_data)

def process_iterable_in_chunks(iterable, chunk_size=1000):
    '''
    A convenience method for processing a list/queryset of objects in chunks
    pattern stolen from https://stackoverflow.com/a/29708603/199754

    :param iterable: list or queryset of objects
    :param chunk_size: max number of objects to process in one iteration
    :return: None
    '''
    offset = 0
    chunk = iterable[offset:offset+chunk_size]
    while chunk:
        yield chunk  # body executes here

        # increment the iterable
        offset += chunk_size
        chunk = iterable[offset:offset+chunk_size]

def schedule_calls(file_path):
    message_data = None
    created_messages = None
    limit = 10000
    message_request_id = str(uuid.uuid1())
    headers, message_data = pick_messages_from_file(file_path)
    tag = get_last_tag(headers)

    try:
        headers, message_data = pick_messages_from_file(file_path)
        tag = get_last_tag(headers)
        for item in message_data:
            item.update({tag: message_request_id})
        for chunk in process_iterable_in_chunks(message_data, limit):
            created_messages = messages_manager.schedule_ad_messages(chunk)
    except Exception as e:
        print created_messages
        print message_data
        print "Error occurred: " + str(e)

    if created_messages:
        drop_messages_to_file(created_messages, file_name="created")
    else:
        created, not_created = messages_manager.check_created_message(message_data, {"tags": message_request_id})
        drop_messages_to_file(created, file_name="created")
        drop_messages_to_file(not_created, file_name="pending")


if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()
    username = args.__dict__['username']
    password = args.__dict__['password']
    organization = args.__dict__['organization']
    file_path = args.__dict__['path']

    messages_manager = ADMessageUtils(organization, username, password)
    awaazde = AwaazDeAPI(organization, username, password)
    schedule_calls(file_path)
