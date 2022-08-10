
""" Module to use scrappy to scrap quotes """
import scrapy

class QuotesSpider(scrapy.Spider):

    """
    Spider class for quotes, inherited from scrapy spider
    """
    name = "quotes"

    #start_urls = ['http://quotes.toscrape.com']
    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # pylint: disable=arguments-differ

        self.logger.info('Hello! this is my first spider.')
        quotes = response.css('div.quote')
        for quote in quotes:
            yield{
                'text' : quote.css('.text::text').get().strip(),
                'author' : quote.css('.author::text').get(),
                'tags' : quote.css('.tag::text').getall()
            }
            

        #next_page = response.css('li.next a').attrib['href']
        anchors = response.css('ul.pager a')
        #if next_page is not None:
            #next_page = response.urljoin(next_page)
            #yield scrapy.Request(url = next_page, callback=self.parse)
        yield from response.follow_all(anchors, callback = self.parse)
