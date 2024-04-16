import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import *

from utils import get_config

from rules import rules
from loaders import *

class ChinaSpider(CrawlSpider):
    name = "china"
    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        super(ChinaSpider, self).__init__(*args, **kwargs)

    def _build_request(self, rule_index, link):
        base_meta = dict(rule=rule_index, link_text=link.text)
        base_meta.update(link.meta)
        return Request(
            url=link.url,
            callback=self._callback,
            errback=self._errback,
            meta=base_meta
        )

    def parse_item(self, response):

        meta=response.meta
        print('meta::',meta)
        ext_params=meta.get('ext_params')

        item = self.config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(cls, response=response)

            if ext_params:
                for k in ext_params:
                    print('loader add value :;',k,'===',meta.get(k))
                    value=meta.get(k)
                    if value:
                        loader.add_value(k, value)

            # 动态获取属性配置
            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'css':
                        loader.add_css(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            yield loader.load_item()