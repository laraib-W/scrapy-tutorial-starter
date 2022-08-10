# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


# pylint: disable=missing-function-docstring
def remove_quotes(text):
    return text.strip('\u201c').strip('\u201c').strip('\u201d')

def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y')

def parse_location(text):
    return text[3:]

class QuoteItem(Item):

    """ Item class for quote """

    quote_content = Field(
        input_processor = MapCompose(remove_quotes),
        # TakeFirst return the first value not the whole list
        output_processor=TakeFirst()
        )
    author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    author_birthday = Field(
        input_processor = MapCompose(convert_date),
        output_processor = TakeFirst()
        )
    author_bornlocation = Field(
        input_processor = MapCompose(parse_location),
        output_processor = TakeFirst()
        )
    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )
    tags = Field()

