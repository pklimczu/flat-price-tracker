
class Constants:
    """
    Contains constants
    """

    # Database
    OFFERS_TABLE = "offers"
    OFFER_DETAILS_TABLE = "offer_details"
    GENERAL_TABLE = "general"
    ###################################


    # Offer table fields
    OTF_URL = "url"
    OTF_PRICE = "price"
    OTF_REGION = "region"
    OTF_INFO = "info"
    OTF_HISTORY_ID = "history_id"
    OTF_TIMESTAMP = "timestamp"
    OTF_UPDATE_DATE = "update_date"
    OTF_UUID = "uuid"
    OTF_PRICE_PER_M2 = "price_per_m2"
    OTF_AREA = "area"
    OTF_ROOMS = "rooms"
    OTF_IS_REMOVED = "is_removed"
    ###################################


    # Offer details table fields
    UUID_OFFER_DETAILS = "uuid_details" # uuid for given offer details entry
    OFFER_UUID = "offer_uuid"           # uuid for main offer
    DESCRIPTION = "description"
    VALUES = "values"
    HASH = "hash" #(description + values)
    DATE = "date"
    ODTF_PRICE = "price"
    OTDF_PRICE_PER_M2 = "price_per_m2"
    ###################################


    # General table fields
    LATEST_HISTORY_ID = "latest_history_id"
    ###################################


    # Offer details dir fields
    DETAILS = "details"
    #DESCRIPTION already defined in # Offer details table fields
    #HASH already defined in # Offer details table fields
    ###################################


    # Others
    KEY = "key"
    VALUE = "value"
    ###################################
