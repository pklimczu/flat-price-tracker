from tinydb import TinyDB, Query, where
import datetime, os, uuid

class DatabaseController:
    """
    Encapsulates operations on TinyDB
    """
    
    def __init__(self, consts, path):
        self.CONSTS = consts
        self.db = TinyDB(path)
        self.offers_table = self.db.table(self.CONSTS.OFFERS_TABLE)
        self.offer_details_table = self.db.table(self.CONSTS.OFFER_DETAILS_TABLE)
        self.general_table = self.db.table(self.CONSTS.GENERAL_TABLE)
        #TODO: log path to db

    def insert_or_update_offer(self, offer):
        Offer = Query()
        search_result = self.offers_table.search(Offer.url == offer[self.CONSTS.OTF_URL])
        if search_result:
            self.offers_table.update(offer, Offer.url == offer[self.CONSTS.OTF_URL])
        else:
            offer[self.CONSTS.OTF_UUID] = str(uuid.uuid4())
            offer[self.CONSTS.OTF_UPDATE_DATE] = datetime.datetime.now().isoformat()
            offer[self.CONSTS.OTF_LAST_CHECKUP] = datetime.datetime.now().isoformat()
            self.offers_table.insert(offer)


    def insert_or_update_offer_details(self, offer_details):
        OfferDetails = Query()
        search_result = self.db.search(OfferDetails.hash == offer_details.hash)


    def insert_or_update_general(self, entry):
        General = Query()
        search_result = self.general_table.search(General.key == entry[self.CONSTS.KEY])
        if search_result:
            self.general_table.update(entry, General.key == entry[self.CONSTS.KEY])
        else:
            self.general_table.insert(entry)


    def get_all_offers(self):
        return self.offers_table.all()


    def get_details_for_offer(self, offer_uuid):
        return self.offer_details_table.search(where(self.CONSTS.OFFER_UUID) == offer_uuid)


    def get_general_entry(self, key):
        return self.general_table.search(where(self.CONSTS.KEY) == key)


    def drop_all(self):
        self.db.truncate()

if __name__ == "__main__":
    dc = DatabaseController("db.json")