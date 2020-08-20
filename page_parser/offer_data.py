import hashlib

class OfferDetails:
    """
    Parses offer data from webpage
    """    
    def __init__(self, consts):
        self.CONSTS = consts
        self.is_key_value_paired = True
        self.details = {}
        self.recent_added_key = ""
        self.description = ""
        self.is_reading_details = False
        self.is_reading_descirption = False

        self.price = None
        self.price_per_m2 = None


    def show(self):
        print("Overview:    ", self.details)
        print("Description: ", self.description)
        print("Price:       ", self.price)
        print("Price/m2:    ", self.price_per_m2)
        print("Hash256:     ", self.get_offer_hash())


    def get_data(self):
        """
        Returns structured details of the offer
        """
        self.details[self.CONSTS.ODTF_PRICE] = self.price
        self.details[self.CONSTS.OTDF_PRICE_PER_M2] = self.price_per_m2
        return {self.CONSTS.DETAILS: self.details, self.CONSTS.DESCRIPTION: self.description,
                self.CONSTS.HASH: self.get_offer_hash()}


    def start_reading_details(self):
        self.is_reading_details = True


    def start_reading_description(self):
        self.is_reading_descirption = True


    def read(self, entry):
        """
        Gets some data and decides how to parse it
        """
        if self.is_reading_details:
            self.__read_details(entry)
        elif self.is_reading_descirption:
            self.__read_description(entry)


    def stop_any_reading(self):
        """
        Stops any reading
        """
        if self.is_reading_details:
            self.is_reading_details = False
            if not self.is_key_value_paired:
                print("ERROR", self.is_key_value_paired)
                #TODO: add some logging for issue investigation
        elif self.is_reading_descirption:
            self.is_reading_descirption = False


    def get_offer_hash(self):
        """
        Calculates hash from details and description. Hash value is used
        to check offer updates
        """
        entry = "#".join((str(self.details), self.description))
        hash256 = hashlib.sha256()
        hash256.update(entry.encode("utf-8"))
        return hash256.hexdigest()


    def __read_details(self, entry):
        if self.is_key_value_paired:
            self.__prepare_key_detail(entry)
        else:
            self.__prepare_value_detail(entry)


    def __read_description(self, entry):
        if len(entry.strip()):
            self.description += entry
            self.description += "\n"


    def __prepare_key_detail(self, key):
        if ":" in key:
            key = key.strip()[:-1]
            self.details[key] = ""
            self.recent_added_key = key
            self.is_key_value_paired = False
        else:
            pass
            #TODO: It is not a key probably


    def __prepare_value_detail(self, value):
        self.details[self.recent_added_key] = value
        self.is_key_value_paired = True