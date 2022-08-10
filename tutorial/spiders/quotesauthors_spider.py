
""" Module to use scrappy to scrap quotes """
import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QuotesAuthorSpider(scrapy.Spider):

    """
    Spider class for quotes, inherited from scrapy spider
    """
    name = "quotesauthor"

    start_urls = ['http://quotes.toscrape.com']
    
    def parse(self, response):
        # pylint: disable=arguments-differ
        quotes = response.css('div.quote')
        for quote in quotes:
            loader = ItemLoader( item= QuoteItem(),
                                selector= quote)
            loader.add_css('quote_content', '.text::text')
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()
            author_url = quote.css('.author + a::attr(href)').get()
            # go to the author page and pass the current collected quote info
            yield response.follow(author_url, self.parse_author, meta={'quote_item': quote_item})

        for anchor in response.css('ul.pager a'):
            yield response.follow(anchor, callback= self.parse)

    def parse_author(self, response):
        """ Parsing Author into Item """
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item= quote_item, response= response)
        loader.add_css('author_name','.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_bornlocation', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')
        yield loader.load_item()
