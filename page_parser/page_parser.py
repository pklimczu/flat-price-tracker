import re, socket, urllib.request
from html_parser import OtodomParser

class PageParser:
    """
    Reads URL and parses info from webpage
    """

    def __init__(self):
        self.page_data = None

    
    def get_detailed_offer(self):
        """
        Returns detailed offer
        """
        if self.page_data:
            op = OtodomParser()
            op.feed(self.page_data)
            offer = op.get_offer()
            self.__get_details_from_data(offer)
            return offer
        else:
            #TODO: log some erros
            print("[ERROR] Page not parsed")
        return None


    def parse_url(self, url):
        """
        Parses URL and returns data as OfferData
        """
        self.page_data = self.__get_webpage(url)


    def __get_webpage(self, url):
        socket.setdefaulttimeout(10) # 10 seconds
        request = urllib.request.Request(url)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
        request.add_header('User-Agent', user_agent)

        try:
            with urllib.request.urlopen(request) as url_request_open:
                data = url_request_open.read()
                return data.decode("utf-8")
        except Exception as error:
            pass
            #TODO: log some erros
        return None
        

    def __get_details_from_data(self, offer):
        """
        Searches for price and price/m2 in the html
        """
        price_pattern = r">([\d\s]+) zł<"
        price_per_m2_pattern = r">([\d\s]+) zł\/m²<"

        price_match = re.search(price_pattern, self.page_data)
        if price_match:
            offer.price = price_match.group(1)
        
        price_per_m2_match = re.search(price_per_m2_pattern, self.page_data)
        if price_per_m2_match:
            offer.price_per_m2 = price_per_m2_match.group(1)

        if not (price_match and price_per_m2_match):
            #TODO: logs error
            print("[ERROR] Webpage was not parsed properly")


if __name__ == "__main__":
    pp = PageParser()
    url = "https://www.otodom.pl/oferta/2-pokoje-z-widna-kuchnia-i-wyposazenem-metro-las-ID477Kg.html"
    pp.parse_url(url)
    offer = pp.get_detailed_offer()
    offer.show()