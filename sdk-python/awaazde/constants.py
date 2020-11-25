class CommonConstants(object):
    DATE_FIELDS = ["send_on"]
    DEFAULT_DATE_FORMAT = "%m-%d-%Y"
    PHONE_NUMBER_FIELD = "phone_number"
    MESSAGE_ID="message_id"
    ID_FIELD = "id"
    SEND_ON_FIELD = "send_on"
    TAG_FIELD = "tag"
    TAGS_FIELD = "tags"
    DEFAULT_CHUNK_SIZE = 10000


class APIConstants(object):
    MESSAGE_API = "message_api",
    CONTENT_API = "content_api",
    TEMPLATE_API = "template_api",
    TEMPLATE_LANGUAGE_API = "template_language_api"
    DEFAULT_BULK_CREATE_LIMIT = 100000
