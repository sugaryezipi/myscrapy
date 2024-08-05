
from renew_scrapy.zegbee_middleware import CrawlSpider, Rule
from renew_scrapy.items import *

from renew_scrapy.utils import get_config

from renew_scrapy.loaders import *

from renew_scrapy.zegbee_middleware import MyLxmlLinkExtractor, JsonLinkExtractor


# 一个 get 的spider
class CommonGetXpathSpider(CrawlSpider):
    name = "common_get_xpath"
    def __init__(self, name, *args, **kwargs):
        config = get_config(name)
        self.config = config
        # self.rules = rules.get(config.get('rules'))
        self.rules = self.build_rules(config.get('rules'))
        self.start_urls = config.get('start_urls')
        self.allowed_domains = config.get('allowed_domains')
        super(CommonGetXpathSpider, self).__init__(*args, **kwargs)

    def build_rules(self, rules_config):
        rules = []
        for rule_name,rule_config in rules_config.items():
            link_ext_type =rule_config.pop("link_ext_type")
            if link_ext_type == 'MyLxmlLinkExtractor':
                articles_rule = Rule(
                    MyLxmlLinkExtractor(
                       **rule_config
                    ),
                    callback='parse_item'
                )
                rules.append(articles_rule)

            if link_ext_type=='JsonLinkExtractor':
                articles_rule = Rule(
                    JsonLinkExtractor(
                        **rule_config
                    ),
                    callback='parse_item'
                )
                rules.append(articles_rule)

        return rules
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
            for key, extractor in item.get('attrs').items():
                # for extractor in value:
                if extractor.get('method') == 'xpath':
                    loader.add_xpath(key, extractor.get('args'), **{'re': extractor.get('re')})
                if extractor.get('method') == 'css':
                    loader.add_css(key, extractor.get('args'), **{'re': extractor.get('re')})
                if extractor.get('method') == 'value':
                    loader.add_value(key, extractor.get('args'), **{'re': extractor.get('re')})
                if extractor.get('method') == 'attr':
                    loader.add_value(key, getattr(response, extractor.get('args')),**{'re': extractor.get('re')})

            yield loader.load_item()