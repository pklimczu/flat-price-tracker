from datetime import datetime, timezone

class Offer:

    def __init__(self):
        self.url = ""
        self.price = ""
        self.region = ""
        
        self.info = ""
        self.rooms = None
        self.area = None
        self.price_per_m2 = None

        self.history_id = ""
        self.timestamp = None


    def set_url(self, url):
        self.url = url


    def set_price(self, price):
        self.price = float(price.replace(" ", "").replace(",","."))


    def set_region(self, region):
        self.region = region


    def set_info(self, info):
        self.info = info.strip()
        splitted_info = self.info.split(", ")
        for chunk in splitted_info:
            if "pok" in chunk:
                self.rooms = chunk.strip()
            elif "zł/" in chunk:
                self.price_per_m2 = chunk.strip()
            else:
                self.area = chunk.strip()
        if not (self.rooms and self.price_per_m2 and self.area):
            print("[ERROR] Parsing info failed, info: ", self.info)


    def set_history_id(self, history_id):
        self.history_id = history_id


    def set_timestamp(self, epoch_timestamp):
        self.timestamp = datetime.fromtimestamp(int(epoch_timestamp)/1000).isoformat()


    def get_info(self):
        info = []
        info.append("#"*25)
        info.append("Okolica:   " + self.region)
        info.append("Cena:      " + str(self.price))
        info.append("Cena m2:   " + self.price_per_m2)
        info.append("URL:       " + self.url)
        info.append("Hist. id:  " + self.history_id)
        info.append("Timestamp: " + self.timestamp)
        return "\n".join(info)

