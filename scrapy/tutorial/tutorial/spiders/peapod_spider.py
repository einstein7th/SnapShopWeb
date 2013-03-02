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
from tutorial.items import DetailedShopItem
import sys
import logging
import thread
import time

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class PeaPodSpider(BaseSpider):

    name = "peapod"
    allowed_domains = ["peapod.com"]
    start_urls = ["http://www.peapod.com/processShowBrowseAisles.jhtml"]
    # start_urls = ["http://www.peapod.com/index.jhtml"]

    all_items = []
    all_items_detail = []
    all_categories = []

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        # now dump all items and cats out
        file = open("all_items.txt", 'wb')
        exporter = JsonItemExporter(file)
        exporter.start_exporting()
        for item in self.all_items:
            exporter.export_item(item)
        exporter.finish_exporting()

        file3 = open("all_items_detail.txt", 'wb')
        exporter = JsonItemExporter(file3)
        exporter.start_exporting()
        for item in self.all_items_detail:
            exporter.export_item(item)
        exporter.finish_exporting()

        file2 = open("all_categories.txt", 'wb')
        exporter2 = JsonItemExporter(file2)
        exporter2.start_exporting()
        for cat in self.all_categories:
            exporter2.export_item(cat)
        exporter2.finish_exporting()

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
        # Only handles top-level categories: http://www.peapod.com/processShowBrowseAisles.jhtml Only one of these
        # Then looks through each top-level category with new requests to find subcategories, which are processed by parse_category

        # Top level categories: Already in a list on the left with each link class 'mainCat'
        hxs = HtmlXPathSelector(response)
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
            self.all_categories.append(new_cat)

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
        time.sleep(0.10)
        # first determine if we've been redirected to item view, ('')
        # or if we've found a subcategory with more subcategories ('Browse Aisles')
        hxs = HtmlXPathSelector(response)
        page_title = hxs.select('//title/text()').extract()[0]

        # print 'response: ', response.body

        if 'Browse Aisles' == page_title: # Find more subcategories
            category_objects = []

            #This is for third level subcategories
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
                self.all_categories.append(new_cat)

            # print category_objects, '\n<<< Category objects\n\n\n'

            # Now we can use this level of categories to start fetching items

            item_requests = []
            for cat in category_objects:
                url = "http://www.peapod.com/browseAisles_BVproductDisplay.jhtml?cnid=" + cat['cnid']
                request = Request(url=url, callback=self.parse_items_table)
                request.meta['parent_cnid'] = cat['cnid']
                request.meta['referer'] = response.url

                # print 'found cnid=', cat['cnid']

                # TODO debug for now: only parse this flower aisle
                if cat['cnid'] == '2099':
                    print 'Found 2099'
                item_requests.append(request)

            return item_requests

        elif 'Item Shelf' == page_title:
            print 'csb found items yo.'

        else:
            print 'got logged out!? cookies gg.'

    # Looks like http://www.peapod.com/browseAisles_BVproductDisplay.jhtml?cnid=393
    def parse_items_table(self, response):
        if 'techerror' in response.url:
            print 'somehow found tech error at url for parent cnid', response.meta['parent_cnid']

        # time.sleep(0.10)

        hxs = HtmlXPathSelector(response)
        page_title = hxs.select('//title/text()').extract()[0]

        parsed_items = []

        # Get all item rows to parse
        items_table = hxs.select('//table')[2]
        item_rows = items_table.select('tbody/tr')
        item_rows = item_rows[1:-1] # Remove first header row

        # print 'PARSING ITEMS YO'

        itemDetailView_requests = []

        for row in item_rows:
            # get item id
            img = row.select('td/div/img')

            # Some rows are shelfAlerts, so we skip them if there is no image:
            """ <tr id="w134571" style="display:none;vertical-align:middle;height:26px;">
            <td id="td134571" colspan="12" class="shelfAlert">
            </td>
            </tr>
            """
            if len(img) > 0:
                # print 'FOUND PROPER ROW'
                img = row.select('td/div/img')[0]          #19x19 GIF image URL
                img_url = img.select('@src').extract()[0]

                item_id = img.select('@name').extract()[0] # productId
                item_id = re.sub('\D', '', item_id)

                name = row.select('td')[2]
                name = name.select('a/text()').extract()[0]

                size = row.select('td')[4].select('text()').extract()[0] # looks like '\n1 EA \xa0\n'
                size = size.strip().lower()                                 # Remove leading, trailing whitespace

                unit_price = row.select('td')[5].select('text()').extract()[0]
                unit_price = unit_price.strip().lower()  # Unit price $3.99 / ea

                price = row.select('td')[7].select('text()').extract()[0]
                price = price.strip()
                price = re.sub('\D', '', price)         # get rid of non digits: '399' is price.

                item = ShopItem(name=name, size=size, unit_price=unit_price, productId=item_id, price=price, thumb=img_url, cnid=response.meta['parent_cnid'])

                parsed_items.append(item)
                self.all_items.append(item)

                url = "http://www.peapod.com/itemDetailView.jhtml?productId=" + item_id
                request = Request(url=url, callback=self.parse_itemDetailView)
                request.meta['cnid'] = response.meta['parent_cnid']
                request.meta['name'] = name
                request.meta['size'] = size
                request.meta['unit_price'] = unit_price
                request.meta['productId'] = item_id
                request.meta['price'] = price
                request.meta['thumb'] = img_url

                itemDetailView_requests.append(request)


        #print 'parsed items', parsed_items
        # For each item, now go to individual item page to grab:
        return itemDetailView_requests

    def parse_itemDetailView(self, response):
        if 'techerror' in response.url:
            print 'somehow found tech error at url ', response.request.url

        # logfun = logging.getLogger("logfun")
        # time.sleep(0.10)
        try:
            hxs = HtmlXPathSelector(response)
            page_title = hxs.select('//title/text()').extract()[0]

            med_image = hxs.select('//input[@id="imageURL"]/@value')[0].extract() # 200x200 image

            # Should probably do some form of exception, but lazy
            large_image = ''
            large_image_path = hxs.select('//input[@id="primaryImageURL"]/@value')
            if len(large_image_path) > 0:
                large_image = large_image_path[0].extract()
            # large_image = hxs.select('//input[@id="primaryImageURL"]/@value')[0].extract() # 600x600 image

            # Only take information in paragraphs, but preserve HTML & formatting: Combine all paragraphs for this entry
            details_list = hxs.select('//div[@id="productDetails-details"]/p').extract()
            details = ''.join(details_list)
            cut_start = details.find('<a class="')
            cut_end = details.rfind('</p>')

            # Remove the disclaimer link at bottom
            if cut_start > 0 and cut_end > 0:
                details = details[0:cut_start] + details[cut_end:]

            nutrition_path = hxs.select('//div[@id="productDetails-nutrition"]/table').extract()
            nutrition = ''
            if len(nutrition_path) > 0:
                nutrition = nutrition_path[0]
            
            ingredients = ''
            if len(hxs.select('//div[@id="ingredients"]').extract()) > 0:
                ingredients = hxs.select('//div[@id="ingredients"]')[0].extract()

            #ingredients = hxs.select('//div[@id="ingredients"]')[0].extract()

            detailed_item = DetailedShopItem(name = response.meta['name'], size = 
                response.meta['size'], unit_price = response.meta['unit_price'], 
                productId = response.meta['productId'], price = 
                response.meta['price'], cnid = response.meta['cnid'], small_image =
                response.meta['thumb'], med_image = med_image, large_image = 
                large_image, details = details, nutrition = nutrition, ingredients = ingredients)

            self.all_items_detail.append(detailed_item)
        # except:
        #     e = sys.exc_info()[0]
        #     print e.print_stack()
        #     sys.exit("error has occurred")
        except Exception, ex:
            print 'gg exception'
            print 'came from', response.request.url
            raise
            #raise KeyboardInterrupt
            # logfun.exception("Bad gg")
            # logfun.debug("figure this out")
            thread.interrupt_main()

        print 'so far all items: ', len(self.all_items), ' vs. detailed: ', len(self.all_items_detail)

    def logged_in(self, response):
        print "COOL BEANS"
        open("login.txt", 'wb').write(response.body)
        # start parsing rest of start_urls
        # gg_request = Request(url="http://www.peapod.com/processShowBrowseAisles.jhtml", callback=self.category);
        return [self.make_requests_from_url(url) for url in self.start_urls]


