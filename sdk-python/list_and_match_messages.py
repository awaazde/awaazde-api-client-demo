import argparse
from datetime import datetime

from awaazde import AwaazDeAPI
from awaazde.constants import CommonConstants, APIConstants
from awaazde.utils import CSVUtils


def parse_arguments():
    parser = argparse.ArgumentParser(description='Check Created Messages')
    parser.add_argument('username', type=str, help='Username of the tenant')
    parser.add_argument('password', type=str, help='Password of the tenant')
    parser.add_argument('organization', type=str, help='Organization of the tenant')
    parser.add_argument('matching_messages_file_path', type=str, help='Path for the csv with which filtered data is to be matched')
    parser.add_argument("--params", nargs='+', help="Fields on which filters are to be applied."
                                                    "Set a number of key-value pairs within double-quotes "
                                                    "(do not put spaces before or after the = sign)."
                                                    "Example: --params 'send_on__gt'='10-12-2020' 'tags'='dummy_tag' ")
    parser.add_argument('--match_criteria', type=str,
                        help='Field to use when matching User record with the queried resultant record',
                        default=CommonConstants.MESSAGE_ID)
    return parser.parse_args()


if __name__ == '__main__':
    """
        Step 1 : Parse the arguments
    """
    args = parse_arguments()
    headers, message_data = CSVUtils.read_csv(args.matching_messages_file_path)
    awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)

    """
        Step 2 : Send an api request to  Get List of Messages based on filters
    """
    params = {'page': APIConstants.DEFAULT_BULK_CREATE_LIMIT,
              'fields': (CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD),
              "filters": dict(map(str.strip, s.split('=')) for s in args.params)}
    messages_from_api = awaazde_api.messages.list_depaginated(params)
    match_criteria = args.match_criteria

    """
        Step 3:  Match Messages from the api and from user's csv based on filters
    """
    # Get a list of all messages,present in user's messages as well as in messages from api after filtering
    matched = [i for i in message_data for j in messages_from_api if i[match_criteria] == j[match_criteria]]
    # Get a list of all messages, present in user's messages,for which we did not find a match in the api's response
    unmatched = [i for i in message_data if i not in matched]

    """
        Step 4:  Dump the data in a file for the user
    """
    CSVUtils.write_csv(matched, args.path, file_name="matched_{}".format(datetime.now().timestamp()))
    CSVUtils.write_csv(unmatched, args.path, file_name="non_matched_{}".format(datetime.now().timestamp()))
