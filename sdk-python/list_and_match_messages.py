import argparse
from datetime import datetime
from awaazde.constants import CommonConstants, APIConstants
from awaazde.utils import CSVUtils
from awaazde import AwaazDeAPI


def parse_arguments():
    parser = argparse.ArgumentParser(description='Check Created Messages')
    parser.add_argument('username', type=str, help='Username of the tenant')
    parser.add_argument('password', type=str, help='Password of the tenant')
    parser.add_argument('organization', type=str, help='Organization of the tenant')
    parser.add_argument('path', type=str, help='Path for the csv')
    parser.add_argument('--params', type=str,
                        help='Fields on which filters are to be applied in the form: {"send_on__gt":"10-12-2020",'
                             '"send_on__lt":"10-12-2020","tags":"dummy_tag"}')
    parser.add_argument('--match_criteria', type=str,
                        help='Field to use when matching User record with the queried resultant record',
                        default=CommonConstants.MESSAGE_ID)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    """
        Step 1 : Parse the arguments
    """
    args = parse_arguments()
    headers, message_data = CSVUtils.read_csv(args.path)
    awaazde_api = AwaazDeAPI(args.organization, args.username, args.password)

    """
        Step 2 : Send an api request to  Get List of Messages based on filters
    """
    params = {}
    params["tags"] = CommonConstants.PHONE_NUMBER_FIELD
    params['page'] = APIConstants.DEFAULT_BULK_CREATE_LIMIT
    params['fields'] = CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD
    responses = awaazde_api.list_depaginated(awaazde_api.messages, params)
    response_dict = {[response[CommonConstants.PHONE_NUMBER_FIELD]] for response in responses}

    """
        Step 3:  Match Messages from the api and from user's csv based on filters
    """
    matched, non_matched = [], []
    for idx, datum in enumerate(message_data):
        response = matched if datum.get(CommonConstants.PHONE_NUMBER_FIELD) in response_dict else non_matched
        response.append(idx)

    """
        Step 4:  Dump the data in a file for the user
    """
    CSVUtils.write_csv(matched, args.path, file_name="matched_{}".format(datetime.now().timestamp()))
    CSVUtils.write_csv(non_matched, args.path, file_name="non_matched_{}".format(datetime.now().timestamp()))
