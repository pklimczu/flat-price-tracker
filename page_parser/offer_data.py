class OfferData:
    """
    Parses offer data
    """
    
    def __init__(self):
        self.is_key_value_paired = True
        self.values = {}
        self.recent_added_key = ""
        self.description = ""
        self.is_reading_details = False
        self.is_reading_descirption = False


    def show(self):
        print("Overview:", self.values)
        print("Description:", self.description)


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
            self.values[key] = ""
            self.recent_added_key = key
            self.is_key_value_paired = False
        else:
            pass
            #TODO: It is not a key probably


    def __prepare_value_detail(self, value):
        self.values[self.recent_added_key] = value
        self.is_key_value_paired = True