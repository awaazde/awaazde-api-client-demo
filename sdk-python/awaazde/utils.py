from datetime import datetime

from constants import CommonConstants
from sdk import AwaazDeAPI


class ADMessageUtils(object):
    def __init__(self, org, user, password):
        """
        Initialize Awaazde Authentication and Call Manager
        :return:
        """
        self.awaazde_api = AwaazDeAPI(org, user, password)

    @classmethod
    def is_message_created(cls, message):
        return message['status'].lower() == 'created'

    @classmethod
    def get_message_id(cls, message):
        return message['id']

    @classmethod
    def get_message_error(cls, message):
        return message['error']

    @classmethod
    def get_ad_schedule_date_time(cls, message):
        return message['send_on']

    @classmethod
    def get_ad_status(cls, message):
        return str(message['state']).lower().replace(' ', '_')

    @classmethod
    def get_execution_state_code_reason(cls, message):
        return message['execution_state_reason_code']

    @classmethod
    def get_duration_seconds(cls, duration):
        if duration and ':' in duration:
            duration_list = duration.split(':')
            return int(duration_list[0]) * 3600 + int(duration_list[1]) * 60 + int(duration_list[2])
        return 0


    def get_messages(self, filters):
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
                response = self.awaazde_api.messages.list(params=filters)
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
                print "Error in Fetching Results"

                return calls_data
        return calls_data

    def schedule_ad_messages(self, messages):
        """
            Sends request to awaazde for scheduling Messages in bulk
            :param messages: List of messages in the format as follows
             [{
                'templatelanguage': 3,
                'phone_number': '+91999999999',
                'send_on': "2018-04-04T10:00:00",
                'values': ['dynamic11', 'dynamic21']
                },
                {
                'templatelanguage': 3,
                'phone_number': '+919999999998',
                'values': ['dynamic12', 'dynamic22']
                }]
        """
        messages = {'data': messages}
        response = self.awaazde_api.messages.bulk_create(messages)
        print response,"++++++++"
        return response

    def check_created_message(self, message_data, filter_fields):
        filters = {}
        created = []
        not_created = []
        for filter_field, filter_value in filter_fields.items():
            filters[filter_field] = filter_value
        #filters['page'] = CommonConstants.AD_MESSAGE_SCHEDULE_LIMIT
        filters['fields'] = CommonConstants.PHONE_NUMBER_FIELD, CommonConstants.ID_FIELD, CommonConstants.SEND_ON_FIELD

        ad_response_messages = self.get_messages(filters)
        messages_response_dict = {}
        for message in ad_response_messages:
            messages_response_dict[message[ CommonConstants.PHONE_NUMBER_FIELD]] = message
        for message in message_data:
            if message.get( CommonConstants.PHONE_NUMBER_FIELD) in messages_response_dict:
                created.append(message)
            else:
                not_created.append(message)
        return created, not_created

    def transform_value(self, filters):
        for field, value in filters:
            try:
                if field is not None:
                    if field in CommonConstants.DATE_FIELDS:
                        value = datetime.strptime(field, CommonConstants.DEFAULT_DATE_FORMAT)
                        if not value:
                            raise Exception('{} is not in the expected date format'.format(field))
            except (Exception, ValueError) as e:
                print e.message

    def process_iterable_in_chunks(self, iterable, chunk_size=CommonConstants.DEFAULT_CHUNK_SIZE):
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
