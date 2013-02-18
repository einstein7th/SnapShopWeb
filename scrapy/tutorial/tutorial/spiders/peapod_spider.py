from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request

class PeaPodSpider(BaseSpider):
    name = "peapod"
    allowed_domains = ["peapod.com"]
    start_urls = ["http://www.peapod.com/processShowBrowseAisles.jhtml"]
    # start_urls = ["http://www.peapod.com/index.jhtml"]

    def start_requests(self):
        # [self.make_requests_from_url(url) for url in self.start_urls]
        return [FormRequest(url="http://www.peapod.com/site/gateway/zip-entry/top/zipEntry_main.jsp?_DARGS=/site/gateway/zip-entry/top/zipEntry_main.jsp",
            formdata={
            "_dyncharset": "ASCII",
"/peapod/handler/iditarod/ZipHandler.continueURL":"/site/gateway/zip-entry/top/selectCity.jsp?NUM1=1361081670096",
"_D:/peapod/handler/iditarod/ZipHandler.continueURL": "",
"/peapod/handler/iditarod/ZipHandler.submitSuccessURL": "/site/gateway/zip-entry/top/zipEntry_main.jsp?NUM1=1361081670096",
"_D:/peapod/handler/iditarod/ZipHandler.submitSuccessURL": "",
"/peapod/handler/iditarod/ZipHandler.submitFailureURL": "/site/gateway/zip-entry/top/zipEntry_main.jsp?NUM1=1361081670096",
"_D:/peapod/handler/iditarod/ZipHandler.submitFailureURL": "",
"zipcode": "02139",
"_D:zipcode": "",
"/peapod/handler/iditarod/ZipHandler.collectProspectURL" : "/site/gateway/zip-entry/top/collectProspect.jsp",
"_D:/peapod/handler/iditarod/ZipHandler.collectProspectURL": "",
"/peapod/handler/iditarod/ZipHandler.storeClosedURL": "/site/gateway/zip-entry/top/storeClosed.jsp",
"_D:/peapod/handler/iditarod/ZipHandler.storeClosedURL": "",
"/peapod/handler/iditarod/ZipHandler.defaultGuestParameters": "true",
"_D:/peapod/handler/iditarod/ZipHandler.defaultGuestParameters": "",
"memberType": "C",
"_D:memberType": "",
"_D:memberType": "",
"Continue": "Create Account",
"_D:Continue": "",
"_DARGS": "/site/gateway/zip-entry/top/zipEntry_main.jsp"
                        },
                    callback=self.logged_in)]

    def parse(self, response):
        open("categories.txt", 'wb').write(response.body)

    def logged_in(self, response):
        print "COOL BEANS"
        open("login.txt", 'wb').write(response.body)
        # start parsing rest of start_urls
        # gg_request = Request(url="http://www.peapod.com/processShowBrowseAisles.jhtml", callback=self.category);
        return [self.make_requests_from_url(url) for url in self.start_urls]

    def category(self, response):
        pass

"""
    def parse(self, response):
        return [FormRequest.from_response(response,
            formdata={},
            callback=self.after_login)]

    def after_login(self, response):
        print "COOL BEANS"


"""

"""
    def parse(self, response):
        print "getting filename"
        filename = response.url.split("/")[-2]
        print "filename: ", filename
        print "response: ", response
        open(filename, 'wb').write(response.body)
        """


