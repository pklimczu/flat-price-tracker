import socket, urllib.request
from html_parser import OtodomParser

class PageParser:
    """
    Reads URL and parses info from webpage
    """

    def __init__(self):
        super().__init__()

    
    def parse_url(self, url):
        """
        Parses URL and returns data as OfferData
        """
        return self.__get_webpage(url)


    def __get_webpage(self, url):
        socket.setdefaulttimeout(10) # 10 seconds
        request = urllib.request.Request(url)
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
        request.add_header('User-Agent', user_agent)
        data = None

        try:
            with urllib.request.urlopen(request) as url_request_open:
                data = url_request_open.read()
        except Exception as error:
            pass
            #TODO: log some erros

        return data.decode("utf-8")


if __name__ == "__main__":
    pp = PageParser()
    url = "https://www.otodom.pl/oferta/2-pokoje-z-widna-kuchnia-i-wyposazenem-metro-las-ID477Kg.html"
    data = pp.parse_url(url)

    if data:
        op = OtodomParser()
        op.feed(data)
        offer = op.get_offer()
        offer.show()