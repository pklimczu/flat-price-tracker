from datetime import datetime, timezone

class Offer:

    def __init__(self):
        self.url = ""
        self.price = ""
        self.region = ""
        self.info = ""
        self.history_id = ""
        self.timestamp = None


    def set_url(self, url):
        self.url = url


    def set_price(self, price):
        self.price = price


    def set_region(self, region):
        self.region = region


    def set_info(self, info):
        self.info = info


    def set_history_id(self, history_id):
        self.history_id = history_id


    def set_timestamp(self, epoch_timestamp):
        self.timestamp = datetime.fromtimestamp(int(epoch_timestamp)/1000)


    def show(self):
        print("#"*25)
        print("Okolica:  ", self.region)
        print("Cena:     ", self.price)
        print("Info:     ", self.info)
        print("URL:      ", self.url)
        print("Hist. id: ", self.history_id)
        print("Timestamp:", self.timestamp)

