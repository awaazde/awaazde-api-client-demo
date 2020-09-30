import argparse
import csv
from datetime import datetime

from constants import CommonConstants
from utils import ADMessageUtils

message_data = ''


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="Username", type=str)
    parser.add_argument("password", help="Password", type=str)
    parser.add_argument("organization", help="Organization ", type=str)
    parser.add_argument("path", help="Path for the csv ", type=str)
    parser.add_argument("-f", "--fields", help="Filters Used for checking messages ", nargs="*", type=str,
                        default="send_on")
    parser.add_argument("-v", "--values", help="Value for filters for checking messages ", type=str,
                        default=datetime.now().strftime(CommonConstants.DEFAULT_DATE_FORMAT))
    args = parser.parse_args()
    return args


def drop_messages_to_file(message_data, path, file_name):
    keys = message_data[0].keys()
    with open('{}/{}.csv'.format(path, file_name),
              'w')  as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(message_data)


# Algorithm:
# 1) Gather and Transform Filter attributes from not command
#     (This is how the messages will get identified; so if we want to check if all messages scheduled for December 21,
#     were created or not, use sendon and 21-12-2020 as fields and values in the arguments)
# 2) Send an api filter request and gather the crea.ted messages and separate the not created messages_manager
# 3) Dump the data in a file for the user

if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments()
    username = args.__dict__['username']
    password = args.__dict__['password']
    organization = args.__dict__['organization']
    file_path = args.__dict__['path']
    path = args.__dict__['path']
    fields = args.__dict__['fields']
    values = args.__dict__['values']

    messages_manager = ADMessageUtils(organization, username, password)

    """ Step 1"""
    filters = {fields[i]: values[i] for i in range(len(fields))}
    messages_manager.transform_value(filters)

    """ Step 2"""
    created, not_created = messages_manager.check_created_message(message_data, filters)

    """ Step 3"""
    drop_messages_to_file(created, path, file_name="created_{}".format(datetime.now().timestamp()))
    drop_messages_to_file(not_created, path, file_name="pending_{}".format(datetime.now().timestamp()))
