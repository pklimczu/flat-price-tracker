import datetime, sys
from database.database import DatabaseController
from mail_parser.mail_parser import MailParser
from page_parser.page_parser import PageParser
from constants.constants import Constants

class Controller:
    """
    Controller to manage all operations
    """

    def __init__(self):
        self.CONSTS = Constants()
        self.db = DatabaseController(self.CONSTS, "db.json")


    def show_menu(self):
        """
        Shows menu
        """
        menu = []
        menu.append("*"*25)
        menu.append("Usage: controller.py <command>")
        menu.append("Available commands:")
        menu.append(" * [full-update]       - reads all mails and updates stored data")
        menu.append(" * [usual-update]      - reads only new mails")
        menu.append(" * [clear-all --force] - removes database")
        menu.append(" * [sites-check]       - goes through saved offers and checks for updates on webpage")
        menu.append("*"*25)
        print("\n".join(menu))


    def full_update(self):
        """
        Goes through all mails and inserts or overwrites existing offer.
        If offer is overwrote, only uuid and url are to be unchanged.
        """
        history_id = {self.CONSTS.KEY: self.CONSTS.LATEST_HISTORY_ID,
                      self.CONSTS.VALUE: 0}

        mail_parser = MailParser()
        mail_parser.parse_all_messages()
        offers = mail_parser.get_offers()

        self.__insert_or_update_offers(offers, history_id)


    def usual_update(self):
        """
        Goes through new mails only and inserts new offers.
        However, it is not guaranteed that only new offers
        will be parsed (ie. the assumption is made that
        history_id was correctly updated last time)
        """
        result = self.db.get_general_entry(self.CONSTS.LATEST_HISTORY_ID)

        if result:
            history_id = result[0]

            mail_parser = MailParser()
            mail_parser.parse_new_messages(history_id[self.CONSTS.VALUE])
            offers = mail_parser.get_offers()

            if offers:
                self.__insert_or_update_offers(offers, history_id)


    def __insert_or_update_offers(self, offers, history_id):
        """
        Realizes common part for `full_update` and `usual_update`
        """
        for offer in offers:
            self.db.insert_or_update_offer(vars(offer))
            if offer.history_id > history_id[self.CONSTS.VALUE]:
                history_id[self.CONSTS.VALUE] = offer.history_id

        self.db.insert_or_update_general(history_id)


    def clear_all(self):
        """
        Removes all entries from database
        """
        self.db.drop_all()


    def sites_check(self):
        offers = self.db.get_all_offers()
        page_parser = PageParser(self.CONSTS)
        allowed_days = [1, 3, 4, 5]
        today = datetime.datetime.now()

        for offer in offers:
            if self.CONSTS.OTF_LAST_CHECKUP in offer:
                last_check_date = datetime.datetime.strptime(offer[self.CONSTS.OTF_LAST_CHECKUP], "%Y-%m-%dT%H:%M:%S%z")
                print(last_check_date)
                #TODO: calculate time difference and check only selected sites
            offer_details = page_parser.get_detailed_offer(offer[self.CONSTS.OTF_URL])
            print(offer_details.get_data())
            #TODO: compare hash of this offer with the hash of the lastest update in db


if __name__ == "__main__":
    controller = Controller()
    controller.full_update()