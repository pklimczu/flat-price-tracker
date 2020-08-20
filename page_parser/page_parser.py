import re, socket, urllib.request
from .html_parser import OtodomParser

class PageParser:
    """
    Reads URL and parses info from webpage
    """

    def __init__(self, consts):
        self.CONSTS = consts
        self.page_data = None

    
    def get_detailed_offer(self, url):
        """
        Returns detailed offer
        """
        self.url = url
        self.__parse_url(url)

        if self.page_data:
            otodom_html_parser = OtodomParser(self.CONSTS)
            otodom_html_parser.feed(self.page_data)
            self.offer_details = otodom_html_parser.get_offer()
            self.__get_extra_details()
            return self.offer_details
        else:
            #TODO: log some erros
            print("[ERROR] Page not parsed, url: ", url)
        return None


    def is_checked_offer_removed(self):
        """
        If the offer is removed, the returned URL will contain 'from404'
        """
        if "from404" in self.returned_url:
            return True
        return False


    def __parse_url(self, url):
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
                self.returned_url = url_request_open.geturl()
                return data.decode("utf-8")
        except Exception as error:
            pass
            #TODO: log some erros
        return None
        

    def __get_extra_details(self):
        """
        Searches for price and price/m2 in the html
        """
        price_pattern = r">([\d\s]+) zł<"
        price_per_m2_pattern = r">([\d\s]+) zł\/m²<"

        price_match = re.search(price_pattern, self.page_data)
        if price_match:
            self.offer_details.price = price_match.group(1)
        
        price_per_m2_match = re.search(price_per_m2_pattern, self.page_data)
        if price_per_m2_match:
            self.offer_details.price_per_m2 = price_per_m2_match.group(1)

        if not (price_match and price_per_m2_match):
            #TODO: logs error
            print("[ERROR] Webpage was not parsed properly: ", self.url)
            self.offer_details = None