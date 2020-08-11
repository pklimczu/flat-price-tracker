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


    def get_info(self):
        info = []
        info.append("#"*25)
        info.append("Okolica:  " + self.region)
        info.append("Cena:     " + self.price)
        info.append("Info:     " + self.info)
        info.append("URL:      " + self.url)
        info.append("Hist. id: " + self.history_id)
        info.append("Timestamp:" + str(self.timestamp))
        return "\n".join(info)

