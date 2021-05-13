import scrapy

from gb_parse.loaders import AvitoLoader
from gb_parse.spiders.xpaths import AVITO_PAGE_XPATH, AVITO_OFFER_XPATH


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/krasnodar/kvartiry/prodam/']
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.5",
        "Connection": "keep-alive",
        #"Host": "www.avito.ru",
    }

    def _get_follow_xpath(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback, headers=self.headers)

    def parse(self, response):
        callbacks = {"pagination": self.parse, "offer": self.offer_parse}

        for key, xpath in AVITO_PAGE_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, callbacks[key])

    def offer_parse(self, response):
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in AVITO_OFFER_XPATH.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
