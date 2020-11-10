import argparse
from datetime import datetime
from awaazde.utils import ADUtils, CSVUtils

def parseArguments():
    parser = argparse.ArgumentParser(description='Check Created Messages')
    parser.add_argument('username', type=str, help='Username of the tenant')
    parser.add_argument('password', type=str, help='Password of the tenant')
    parser.add_argument('organization', type=str, help='Organization of the tenant')
    parser.add_argument('path', type=str, help='Path for the csv')
    parser.add_argument('--filters', type=str,
                        help='Filters to be applied in the form: {"send_on__gt":"10-12-2020",'
                             '"send_on__lt":"10-12-2020","tags":"dummy_tag"}')
    return args


if __name__ == '__main__':
    """
        Step 1 : Parse the arguments
    """
    args = parseArguments()
    headers, message_data = CSVUtils.parse_csv(args.path)

    """
        Step 2 : Send an api filter request and gather the created messages and separate the not created messages_manager
    """

    ad_manager = ADUtils(args.organization, args.username, args.password)
    created, not_created = ad_manager.check_created_message(message_data, args.filters)

    """
        Step 3:  Dump the data in a file for the user
    """
    CSVUtils.create_csv(created, args.path, file_name="created_{}".format(datetime.now().timestamp()))
    CSVUtils.create_csv(not_created, args.path, file_name="pending_{}".format(datetime.now().timestamp()))
