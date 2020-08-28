from tinydb import TinyDB, Query, where
import datetime, logging, os, uuid

class DatabaseController:
    """
    Encapsulates operations on TinyDB
    """
    
    def __init__(self, consts, path):
        self.logger = logging.getLogger(__name__)
        self.CONSTS = consts
        self.path = path
        self.logger.info(f"Path to DB passed: {path}")
        self.__load_db()


    def insert_or_update_offer(self, offer):
        Offer = Query()
        search_result = self.offers_table.search(Offer.url == offer[self.CONSTS.OTF_URL])
        if search_result:
            self.offers_table.update(offer, Offer.url == offer[self.CONSTS.OTF_URL])
        else:
            offer[self.CONSTS.OTF_UUID] = str(uuid.uuid4())
            offer[self.CONSTS.OTF_UPDATE_DATE] = datetime.datetime.now().isoformat()
            self.offers_table.insert(offer)


    def insert_or_update_offer_details(self, offer_details):
        OfferDetails = Query()
        search_result = self.offer_details_table.search(OfferDetails.hash == offer_details[self.CONSTS.UUID_OFFER_DETAILS])
        if search_result:
            self.offer_details_table.update(offer_details, OfferDetails.hash == offer_details[self.CONSTS.UUID_OFFER_DETAILS])
        else:
            self.offer_details_table.insert(offer_details)


    def insert_or_update_general(self, entry):
        General = Query()
        search_result = self.general_table.search(General.key == entry[self.CONSTS.KEY])
        if search_result:
            self.general_table.update(entry, General.key == entry[self.CONSTS.KEY])
        else:
            self.general_table.insert(entry)


    def get_all_offers(self, only_valid = False):
        """
        Returns all offers. If `only_valid` specified, the removed offers
        are filtred out.
        """
        if only_valid:
            Offers = Query()
            return self.offers_table.search(~ Offers.is_removed.exists())
        else:
            return self.offers_table.all()


    def get_offer(self, offer_uuid):
        """
        Returns only offer with given offer_uuid
        """
        Offer = Query()
        return self.offers_table.get(Offer.uuid == offer_uuid)


    def get_details_for_offer(self, offer_uuid, only_most_recent = False):
        offers = self.offer_details_table.search(where(self.CONSTS.OFFER_UUID) == offer_uuid)
        if offers and only_most_recent:
            # the last one inserted is the most recent
            return offers[-1]
        return offers


    def get_general_entry(self, key):
        return self.general_table.get(where(self.CONSTS.KEY) == key)


    def drop_all(self):
        self.db.truncate()

    
    def reload_db(self):
        self.__load_db()
        self.logger("Database reloaded")


    def __load_db(self):
        self.db = TinyDB(self.path)
        self.offers_table = self.db.table(self.CONSTS.OFFERS_TABLE)
        self.offer_details_table = self.db.table(self.CONSTS.OFFER_DETAILS_TABLE)
        self.general_table = self.db.table(self.CONSTS.GENERAL_TABLE)