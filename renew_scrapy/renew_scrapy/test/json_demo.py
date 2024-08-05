import json

import jmespath


from renew_scrapy.zegbee_middleware import CrawlSpider, Rule
from items import *

from utils import get_config

from rules import rules
from loaders import *


'''
'url': '',
'url_prefix': "",
'base_url': '',
'base_format_id': '',
'''
# get -返回json
class JsonDemoSpider(CrawlSpider):
    name = "json_demo"
    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        self.rules = rules.get(config.get('rules'))
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        super(JsonDemoSpider, self).__init__(*args, **kwargs)



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
                    if extractor.get('method') == 'jmespath':
                        loader.add_value(key, jmespath.search(*extractor.get('args'),json.loads(response.text)))
            yield loader.load_item()

