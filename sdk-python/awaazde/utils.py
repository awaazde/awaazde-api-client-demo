import csv

import pandas as pd

from .constants import CommonConstants


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
            keys = list(data[0].keys())
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
