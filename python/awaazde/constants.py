class CommonConstants():
    PHONE_NUMBER_FIELD = "phone_number"
    ID_FIELD = "id"
    SEND_ON_FIELD = "send_on"
    DEFAULT_CHUNK_SIZE = 10000


class APIConstants():
    # Backend can handle 10k records per request. But request session got limited by 5k. So setting this limit
    DEFAULT_BULK_CREATE_LIMIT = 5000
