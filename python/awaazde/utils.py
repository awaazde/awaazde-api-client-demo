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
    def write_or_append_to_csv(data, file_path, file_name, append=False):
        if data:
            keys = list(data[0].keys())
            if 'error' not in keys:
                keys.extend(["error"])
            write_append_mode = 'a' if append else 'w'
            with open('{}/{}.csv'.format(file_path, file_name), write_append_mode)  as output_file:
                writer = csv.DictWriter(output_file, fieldnames=keys, extrasaction='ignore')
                if not append:
                    writer.writeheader()
                writer.writerows(data)


    @staticmethod
    def read_csv(csv_file_path, replace_null=False):
        """
        replace_null: If set to True: all  null values in csv will be replaced by ("NA","NaN","None" etc).
                      If set to False: Null values will remain blank. (In cases like "send_on" date,
                      we want it blank,so default for this function w.r.t the usage of this Demo has been kept as false)
        """
        df = pd.read_csv(csv_file_path, na_filter=replace_null)
        headers = df.head()
        data = df.to_dict('records')
        return headers, data
