from html.parser import HTMLParser
from .offer_data import OfferDetails

class OtodomParser(HTMLParser):

    def __init__(self, consts):
        super().__init__()
        self.CONSTS = consts
        self.read_content = False
        self.offer = OfferDetails(self.CONSTS)

    
    def handle_starttag(self, tag, attrs):
        # Capture `section-overview` and 'section-description'
        if tag == "section":
            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] in ["section-overview", "section-description"]:
                        self.read_content = True
                        if attr[1] == "section-overview":
                            self.offer.start_reading_details()
                        elif attr[1] == "section-description":
                            self.offer.start_reading_description()
    
    
    def handle_endtag(self, tag):
        if self.read_content and tag == "section":
            self.read_content = False
            self.offer.stop_any_reading()


    def handle_data(self, data):        
        if self.read_content:
            if ".css-" not in data:
                self.offer.read(data)


    def get_offer(self):
        return self.offer