import datetime, logging, sys, uuid
from database.database import DatabaseController
from mail_parser.mail_parser import MailParser
from page_parser.page_parser import PageParser
from constants.constants import Constants
from config.configuration import Configuration

class Controller:
    """
    Controller to manage all operations
    """

    def __init__(self):
        self.config = Configuration()
        self.__setup_logger()
        self.CONSTS = Constants()
        self.db = DatabaseController(self.CONSTS, self.config.get_db_path())


    def show_menu(self):
        """
        Shows menu
        """
        menu = []
        menu.append("*"*25)
        menu.append("Usage: controller.py <command>")
        menu.append("Available commands:")
        menu.append(" * [full-update]           - reads all mails and updates stored data")
        menu.append(" * [usual-update]          - reads only new mails")
        menu.append(" * [clear-all --force]     - removes database")
        menu.append(" * [sites-check [--force]] - goes through saved offers and checks for updates on webpage. \
            If --force, all oferts will be checked")
        menu.append("*"*25)
        print("\n".join(menu))


    def full_update(self):
        """
        Goes through all mails and inserts or overwrites existing offer.
        If offer is overwrote, only uuid and url are to be unchanged.
        """
        history_id = {self.CONSTS.KEY: self.CONSTS.LATEST_HISTORY_ID,
                      self.CONSTS.VALUE: 0}

        mail_parser = MailParser(self.config)
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
            history_id = result

            mail_parser = MailParser(self.config)
            mail_parser.parse_new_messages(history_id[self.CONSTS.VALUE])
            offers = mail_parser.get_offers()

            if offers:
                self.__insert_or_update_offers(offers, history_id)
        else:
            self.full_update()


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


    def sites_check(self, force = False):
        """
        Parsing website with the URL provided in e-mails, in order to get more details
        """
        offers = self.db.get_all_offers(only_valid=True)
        self.page_parser = PageParser(self.CONSTS)
        self.today = datetime.datetime.now()

        for offer in offers:
            self.__check_offer(offer, force)

        today = datetime.datetime.today().isoformat()
        last_update_entry_db = {self.CONSTS.KEY: self.CONSTS.LATEST_UPDATE_DATE,
                                self.CONSTS.VALUE: today}
        self.db.insert_or_update_general(last_update_entry_db)
        self.logger.info(f"Update successful: {today}")


    def get_all_offers(self):
        """
        Returns all offers in JSON format
        """
        offers = self.db.get_all_offers()
        last_update = self.db.get_general_entry(self.CONSTS.LATEST_UPDATE_DATE)[self.CONSTS.VALUE]
        return (offers, last_update)


    def get_offer(self, uuid):
        """
        Returns offer with given uuid in JSON format
        """
        return self.db.get_offer(uuid)


    def get_details_for_offer(self, uuid, all_data=False):
        """
        Returns offer details for given offer uuid
        """
        return self.db.get_details_for_offer(uuid)


    def __check_offer(self, offer, force):
        allowed_days = [1, 2, 3]

        # That segment is for skipping offers that were checked recently (as in `allowed_days`)
        if not force:
            if self.CONSTS.OTF_UPDATE_DATE in offer:
                last_check_date = datetime.datetime.strptime(offer[self.CONSTS.OTF_UPDATE_DATE], "%Y-%m-%dT%H:%M:%S.%f")
                days_diff = int((self.today - last_check_date).days)

                if days_diff not in allowed_days and days_diff % allowed_days[-1] != 0:
                    self.logger.info("Skipped - it is not the right time for update")
                    return

        # Here the webpage is fetched and parsed
        offer_details = self.page_parser.get_detailed_offer(offer[self.CONSTS.OTF_URL])

        if not offer_details:
            if self.page_parser.is_checked_offer_removed():
                offer[self.CONSTS.OTF_IS_REMOVED] = True
                self.db.insert_or_update_offer(offer)
                self.logger.info(f"Offer was removed: {offer[self.CONSTS.OTF_URL]}")
                return
            else:
                self.logger.error("Page was not parsed")
                return

        offer_details_data = offer_details.get_data()
        stored_offer_details = self.db.get_details_for_offer(offer[self.CONSTS.OTF_UUID],
                                                        only_most_recent=True)
        
        # If hash of previous offer is the same as the current one, skip insertion
        if stored_offer_details:
            if stored_offer_details[self.CONSTS.HASH] == offer_details_data[self.CONSTS.HASH]:
                self.logger.info(f"Skipped - the same hash: {offer[self.CONSTS.OTF_URL]}")
                return
        
        # Insert new details
        offer_details_data[self.CONSTS.UUID_OFFER_DETAILS] = str(uuid.uuid4())
        offer_details_data[self.CONSTS.OFFER_UUID] = offer[self.CONSTS.OTF_UUID]
        offer_details_data[self.CONSTS.DATE] = datetime.datetime.now().isoformat()
        self.db.insert_or_update_offer_details(offer_details_data)

        # Update `update_date` of offer
        offer[self.CONSTS.OTF_UPDATE_DATE] = datetime.datetime.now().isoformat()
        self.db.insert_or_update_offer(offer)


    def __setup_logger(self):
        """
        Setups logging facility
        """
        file_handler = logging.FileHandler(self.config.get_logs_path())
        console_handler = logging.StreamHandler()
        handlers = [file_handler, console_handler]
        logging.basicConfig(level=logging.INFO,
                            format='[%(levelname)-7s][%(asctime)s][%(filename)s:%(funcName)s]: %(message)s',
                            handlers=handlers)
        self.logger = logging.getLogger("Controller")


if __name__ == "__main__":
    controller = Controller()
    controller.usual_update()
    controller.sites_check()
 