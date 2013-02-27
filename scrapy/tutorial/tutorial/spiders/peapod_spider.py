from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
import string
import unicodedata
import re # for string manipulation: removing all digits from a string
from scrapy.contrib.exporter import JsonItemExporter
from scrapy.selector import HtmlXPathSelector

from tutorial.items import ShopItem
from tutorial.items import ShopCategory

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

        # Very rudimentary switch: If the page title is the top level, then we process top-level categories
        # Wait. we Can use different callbacks to process the subcategories.

        # Find top-level categories from response and create objects.
        # http://www.peapod.com/processShowBrowseAisles.jhtml Only one of these
        hxs = HtmlXPathSelector(response)
        # Top level categories: Already in a list on the left with each link class 'mainCat'
        big_categories = hxs.select('//a[@class="mainCat"]')

        big_category_objects = []

        # Extract categories one-by-one. We are now in the scope of each <a>:
        # <a href="?cnid=2098" target="_self" class="mainCat">Produce</a>
        for cat in big_categories:
            # Get category id (cnid): Remove all text except digits from href that links to category
            cnid_href = cat.select('@href').extract()[0].translate(string.digits)
            cnid = re.sub('\D', '', cnid_href) # remove all non-digits, again!?
            name = cat.select('text()').extract()[0].rstrip() # Category name: Remove the \n at end

            new_cat = ShopCategory(name=name, cnid=cnid, parent='')

            big_category_objects.append(new_cat)

            # unicodedata.normalize('NFKD', title).encode('ascii','ignore') turn the text fields to ascii

        # Prepare requests to parse subcategories
        subcategory_requests = []
        for cat in big_category_objects:
            url = "http://www.peapod.com/processShowBrowseAisles.jhtml?cnid=" + cat['cnid']
            request = Request(url=url, callback=self.parse_category)
            request.meta['parent_cnid'] = cat['cnid']
            subcategory_requests.append(request)

        # Export big categories
        print big_category_objects, '\n\n'

        file = open("categories_top.txt", 'wb')
        exporter = JsonItemExporter(file)
        exporter.start_exporting()

        for cat in big_category_objects:
            exporter.export_item(cat)

        exporter.finish_exporting()

        # Move on to parsing subcategories
        print '\n\n\n\n\ndone with top level category request. moving on to next\n\n\n'
        return subcategory_requests

    def parse_category(self, response): # Parse middle level cateogries, 1 level beneath 
        # first determine if we've been redirected to item view, ('')
        # or if we've found a subcategory with more subcategories ('Browse Aisles')
        hxs = HtmlXPathSelector(response)
        page_title = hxs.select('//title/text()').extract()[0]

        # print 'response: ', response.body

        if 'Browse Aisles' == page_title: # Find more subcategories
            category_objects = []

            #sub_categories_links = hxs.select('//div[@id="BASubCol1"]/p/a')
            sub_categories_links = hxs.select('//div[@id="BALeft"]/ul/li/ul/li/a') 
            # Middle level 

            for cat in sub_categories_links:
                # href looks like /processShowBrowseAisles.jhtml?cnid=2100&amp;L=4
                # Just translate to digits and strip out the 4
                cnid_href = cat.select('@href').extract()[0]
                cnid = re.sub('\D', '', cnid_href) # remove all non-digits
                #cnid = cnid[0:-1]                  # Hack to remove the last 4
                name = cat.select('text()').extract()[0].rstrip() # Category name: Remove the \n at end, and remove the number in parenthesis
                name = name[0:name.find('(') - 1]

                new_cat = ShopCategory(name=name, cnid=cnid, parent=response.meta['parent_cnid'])

                category_objects.append(new_cat)

            print category_objects, '\n<<< Category objects\n\n\n'

            # Now we can use this level of categories to start fetching items

        elif 'Item Shelf' == page_title:
            print 'csb found items yo.'

        else:
            print 'got logged out!? cookies gg.'

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


