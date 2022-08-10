
""" Module to use scrappy to scrap all authors """

import scrapy

class AuthorsSpider(scrapy.Spider):

    """
    Spider class for Authors, inherited from scrapy spider
    """
    name = "authors"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        # pylint: disable=arguments-differ

        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, callback = self.parse_author)

        pagination_links = response.css('.next a')
        yield from response.follow_all(pagination_links, callback = self.parse)

    def parse_author(self, response):

        """ Funtion to parse Author of quote"""
        def extract_from_css(query):
            return response.css(query).get(default = '').strip()

        yield {
            "name" : extract_from_css('.author-title::text'),
            "birth-date" : extract_from_css('.author-born-date::text'),
            "description" : extract_from_css('.author-description::text')
        }    