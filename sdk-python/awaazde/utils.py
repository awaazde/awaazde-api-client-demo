import csv
import logging
import pandas as pd
from datetime import datetime
from constants import CommonConstants

from . import AwaazDeAPI


class ADUtils(object):
    def __init__(self, org, user, password):
        """
        Initialize Awaazde Authentication and Call Manager
        :return:
        """
        self.awaazde_api = AwaazDeAPI(org, user, password)

    def get_created_messages(self, filters):
        """
            Gets all messages from awaazde API based on the filters passed
        """

        def _get_url_params(url):
            """
            :param url: A url which looks something like "https://api.awaaz.de/awaazde/v1/xact/message/?state=6&page=2"
            :returns A dictionary of request params in the url something like
                    {
                        "state": 6,
                        "page": 2
                    }
            """
            all_param_strings = url.split('?', 1)[1].split('&')
            url_params = {}
            for param in all_param_strings:
                url_params[param.split('=', 1)[0]] = param.split('=', 1)[1]
            return url_params

        # Get next page URL
        next_page_url = None
        calls_data = []
        while True:
            if not next_page_url:

            else:
                # GEts next page number
                filters['page'] = _get_url_params(next_page_url)['page']
                # And then we request for the data on the next page
                response = self.awaazde_api.messages.list(params=filters)
            if response:
                calls_data.extend(response['results'])
                if response['next']:
                    next_page_url = response['next']
                else:
                    break
            else:
                logging.error("Error in Fetching Results")

                return calls_data
        return calls_data

    def bulk_create_in_chunks(self, messages, limit):
        messages = {'data': messages}
        response = []
        for message_chunk in CommonUtils.process_iterable_in_chunks(messages, limit):
            response += self.awaazde_api.messages.bulk_create(message_chunk)
        return response

    def check_created_message(self, message_data, filter_fields):
        filters = {}
        created = []
        not_created = []
        for filter_field, filter_value in filter_fields.items():
            filters[filter_field] = filter_value

        filters['page'] = CommonConstants.AD_MESSAGE_SCHEDULE_LIMIT
        filters['fields'] = CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD

        ad_response_messages = self.get_created_messages(filters)
        messages_response_dict = {}
        for message in ad_response_messages:
            messages_response_dict[message[CommonConstants.PHONE_NUMBER_FIELD]] = message
        for message in message_data:
            if message.get(CommonConstants.PHONE_NUMBER_FIELD) in messages_response_dict:
                created.append(message)
            else:
                not_created.append(message)
        return created, not_created


class CommonUtils(object):

    @staticmethod
    def process_iterable_in_chunks(iterable, chunk_size=CommonConstants.DEFAULT_CHUNK_SIZE):
        '''
        A convenience method for processing a list/queryset of objects in chunks
        pattern stolen from https://stackoverflow.com/a/29708603/199754

        :param iterable: list or queryset of objects
        :param chunk_size: max number of objects to process in one iteration
        :return: None
        '''
        offset = 0
        chunk = iterable[offset:offset + chunk_size]
        while chunk:
            yield chunk  # body executes here

            # increment the iterable
            offset += chunk_size
            chunk = iterable[offset:offset + chunk_size]


class CSVUtils(object):
    @staticmethod
    def create_csv(data, file_path, file_name):
        if data:
            keys = data[0].keys()
            with open('{}/{}.csv'.format(file_path, file_name),
                      'w')  as output_file:
                writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)

    @staticmethod
    def parse_csv(csv_file_path):
        df = pd.read_csv(csv_file_path, encoding="ISO-8859-1")
        headers = df.head()
        message_data = df.to_dict('records')
        return headers, message_data
