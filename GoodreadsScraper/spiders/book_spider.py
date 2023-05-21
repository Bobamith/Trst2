"""Spider to extract information from a /book/show type page on Goodreads"""

import scrapy

from .author_spider import AuthorSpider
from ..items import BookItem, BookLoader

class BookSpider(scrapy.Spider):
    """Extract information from a /book/show type page on Goodreads

        Technically, this is not a Spider in the sense that
        it is never initialized by scrapy. Consequently,
         - its from_crawler method is never invoked
         - its `crawler` attribute is not set
         - it does not have a list of start_urls or start_requests
         - running this spider with scrapy crawl will do nothing
    """
    name = "book"

    def __init__(self):
        super().__init__()
        self.author_spider = AuthorSpider()

    def parse(self, response, loader=None):
        if not loader:
            loader = BookLoader(BookItem(), response=response)

        loader.add_value('url', response.request.url)

        # The new Goodreads page sends JSON in a script tag
        # that has these values


        loader.add_css('genres', 'script#__NEXT_DATA__::text')
        loader.add_css('publisher', 'script#__NEXT_DATA__::text')


        


        yield loader.load_item()
