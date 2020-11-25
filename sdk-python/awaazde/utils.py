import csv
import logging
import urlparse

import pandas as pd
from constants import CommonConstants, APIConstants


class APIUtils(object):

    def list_depaginated(self, api, params=None):
        """
            Gets all messages from awaazde API based on the filters passed
        """
        data = []
        response = api.list(params=params)
        while response.get('next') is not None:
            # Get next page URL
            next_page_url = response['next']
            params['page'] = urlparse.parse_qs(urlparse.urlparse(next_page_url).query)['page'][0]
            # And then we request for the data on the next page
            response = api.list(params=params)

        if response:
            data.extend(response['results'])
        else:
            logging.error("Error in Fetching Results")

        return data

    def create_bulk_in_chunks(self, api, data, **kwargs):
        """
        Create messages in chunks based on limit if present, takes DEFAULT_BULK_CREATE_LIMIT as default.
        :param api:
        :type api:
        :param Data: Data to create. eg: if messages: [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi"}]
        :type Data: List of dict
        :param limit: Number of messages to create in one chunked request
        :type limit: integer
        :return: Response from bulk create api
        :rtype: List of dict [{phone_number:8929292929,send_on:"",tag1:"tag_number1",templatelanguage:23,language:"hi",status:"created"}}
        """
        limit = kwargs.get('limit') if kwargs.get('limit') else APIConstants.DEFAULT_BULK_CREATE_LIMIT
        response = []
        for data_chunk in CommonUtils.process_iterable_in_chunks(data, limit):
            response += api.create_bulk(data_chunk, **kwargs)
        return response


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
    def write_csv(data, file_path, file_name):
        if data:
            keys = data[0].keys()
            with open('{}/{}.csv'.format(file_path, file_name),
                      'w')  as output_file:
                writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)

    @staticmethod
    def read_csv(csv_file_path):
        df = pd.read_csv(csv_file_path)
        headers = df.head()
        data = df.to_dict('records')
        return headers, data
