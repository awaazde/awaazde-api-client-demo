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
    parser.add_argument('match_path', type=str, help='Path for the csv with which filtered data is to be matched')
    parser.add_argument("--params",
                        nargs='+',
                        help="Fields on which filters are to be applied."
                             "Set a number of key-value pairs with double-quotes "
                             "(do not put spaces before or after the = sign)."
                             "Example: --params send_on__gt=10-12-2020 tags=dummy_tag ")
    parser.add_argument('--match_criteria', type=str,
                        help='Field to use when matching User record with the queried resultant record',
                        default=CommonConstants.MESSAGE_ID)
    return parser.parse_args()


def parse_vars(extra_vars):
    """
    Take a list of comma separated key value pair strings, separated
    by comma strings like 'foo=bar' and return as dict.
    :param extra_vars: list[str] ['foo=bar, 'key2=value2']
    :return: dict[str, str] {'foo': 'bar', 'key2': 'value2'}
    """
    vars_list = []
    if extra_vars:
        for i in extra_vars:
            items = i.split('=')
            key = items[0].strip()
            if len(items) > 1:
                value = '='.join(items[1:])
                vars_list.append((key, value))
    return dict(vars_list)


if __name__ == '__main__':
    """
        Step 1 : Parse the arguments
    """
    args = parse_arguments()
    headers, message_data = CSVUtils.read_csv(args.match_path)
    awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)

    """
        Step 2 : Send an api request to  Get List of Messages based on filters
    """
    params = {'page': APIConstants.DEFAULT_BULK_CREATE_LIMIT,
              'fields': (CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD),
              "filters": parse_vars(args.params)}
    messages_from_api = awaazde_api.messages.list_depaginated(params)
    match_criteria = args.match_criteria or CommonConstants.PHONE_NUMBER_FIELD

    """
        Step 3:  Match Messages from the api and from user's csv based on filters
    """
    # Get a list of all messages,present in user's messages as well as in messages from api after filtering
    matched = [i for i in message_data for j in messages_from_api if i[match_criteria] == j[match_criteria]]
    # Get a list of all messages, present in user's messages,for which we did not find a match in the api's response
    non_matched = [i for i in message_data if i not in matched]

    """
        Step 4:  Dump the data in a file for the user
    """
    CSVUtils.write_csv(matched, args.path, file_name="matched_{}".format(datetime.now().timestamp()))
    CSVUtils.write_csv(non_matched, args.path, file_name="non_matched_{}".format(datetime.now().timestamp()))
