import pymongo
import scrapy
from ..loaders import AutoyoulaLoader
from gb_parse.spiders.xpaths import AUTO_YOULA_PAGE_XPATH, AUTO_YOULA_BRAND_XPATH, AUTO_YOULA_CAR_XPATH


class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    _xpath_selectors = AUTO_YOULA_PAGE_XPATH.update(AUTO_YOULA_BRAND_XPATH)
    _xpath_data_selectors = AUTO_YOULA_CAR_XPATH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def _get_follow(self, response, selector_str, callback):
        for itm in response.xpath(selector_str):
            yield response.follow(itm, callback=callback)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(
            response, self._xpath_selectors["brands"], self.brand_parse,
        )

    def brand_parse(self, response):
        yield from self._get_follow(
            response, self._xpath_selectors["pagination"], self.brand_parse
        )
        yield from self._get_follow(
            response, self._xpath_selectors["car"], self.car_parse,
        )

    def car_parse(self, response):
        loader = AutoyoulaLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in self._xpath_data_selectors.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
