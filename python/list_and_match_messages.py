import argparse
import logging
import os
from datetime import datetime

from awaazde import AwaazDeAPI
from awaazde.constants import CommonConstants
from awaazde.utils import CSVUtils


def parse_arguments():
    parser = argparse.ArgumentParser(description='Check Created Messages')
    parser.add_argument('username', type=str, help='Username of the tenant')
    parser.add_argument('password', type=str, help='Password of the tenant')
    parser.add_argument('organization', type=str, help='Organization of the tenant')
    parser.add_argument('matching_messages_file_path', type=str,
                        help='Path for the csv with which filtered data is to be matched')
    parser.add_argument("--params", nargs='+', help="Fields on which filters are to be applied."
                                                    "Set a number of key-value pairs within double-quotes "
                                                    "(do not put spaces before or after the = sign)."
                                                    "Example: --params send_on__gt => a date in the format "
                                                    "YYYY-MM-DDTHH:MM:SS to filter by messages scheduled after the "
                                                    "given date send_on__lt => a date in the format "
                                                    "YYYY-MM-DDTHH:MM:SS to filter by messages scheduled before the "
                                                    "given date 'tags'='dummy_tag' ")
    parser.add_argument('--match_criteria', type=str,
                        help='Field to use when matching User record with the queried resultant record',
                        default=CommonConstants.ID_FIELD)
    return parser.parse_args()


if __name__ == '__main__':
    """
        Step 1 : Parse the arguments
    """
    args = parse_arguments()
    headers, message_data = CSVUtils.read_csv(args.matching_messages_file_path)
    awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)

    """
        Step 2 : Send an api request to get list of messages based on filters
    """
    params = {'fields': ','.join(
        [CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD]),
    }
    filters = dict(list(map(str.strip, s.split('='))) for s in args.params)
    params = params.update(filters)
    messages_from_api = awaazde_api.messages.list_depaginated(params)

    """
        Step 3:  Match Messages from the api and from user's csv based on filters if they exist
    """
    if messages_from_api:
        match_criteria = args.match_criteria
        # Get a list of all messages,present in user's messages as well as in messages from api after filtering
        matched = [i for i in message_data for j in messages_from_api if i[match_criteria] == j[match_criteria]]
        # Get a list of all messages, present in user's messages,for which we did not find a match in the api's response
        unmatched = [i for i in message_data if i not in matched]

        """
            Step 4:  Dump the data in a file for the user
        """
        file_path = os.path.dirname(args.matching_messages_file_path)
        CSVUtils.write_csv(matched, file_path, file_name="matched_{}".format(datetime.now().timestamp()))
        CSVUtils.write_csv(unmatched, file_path, file_name="unmatched_{}".format(datetime.now().timestamp()))
    else:
        logging.info(" No messages Found matching with your criteria")
