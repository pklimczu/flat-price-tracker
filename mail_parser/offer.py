class Offer:

    def __init__(self):
        self.url = ""
        self.price = ""
        self.region = ""
        self.info = ""
        self.history_id = ""


    def setUrl(self, url):
        self.url = url


    def setPrice(self, price):
        self.price = price


    def setRegion(self, region):
        self.region = region


    def setInfo(self, info):
        self.info = info


    def setHistoryId(self, history_id):
        self.history_id = history_id


    def show(self):
        print("#"*25)
        print("Okolica: ", self.region)
        print("Cena:    ", self.price)
        print("Info:    ", self.info)
        print("URL:     ", self.url)
        print("Hist. id:", self.history_id)

