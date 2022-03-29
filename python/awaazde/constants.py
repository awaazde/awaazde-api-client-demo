class CommonConstants():
    PHONE_NUMBER_FIELD = "phone_number"
    ID_FIELD = "id"
    SEND_ON_FIELD = "send_on"
    DEFAULT_CHUNK_SIZE = 10000


class APIConstants():
    # Backend can only handle 10k records per request. So setting this limit
    DEFAULT_BULK_CREATE_LIMIT = 5000
