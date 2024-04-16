
from risk_scrapy.zegbee_middleware import MyLxmlLinkExtractor



from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse, Request, Response

class MySpider(CrawlSpider):
    name = 'my_spider'
    start_urls = ['http://127.0.0.1:8000/products?page=1']

    rules = (
        Rule(
            link_extractor=MyLxmlLinkExtractor(
                # allow_domains=['example.com'],
                restrict_xpaths='//div[@class="product-item"]',  # 目标div的XPath
                restrict_extra_xpath={'name':'.//a/text()',
                                  'date': './/p/text()',
                                  },
                extra_xpath={'page':'//div[@class="pagination"]/a[@class="active"]/text()'},
                ext_params=['page','name','date']
                # 需要携带的数据  从前端点存入
            ),

            callback='parse_item',
            follow=True,
        ),
    )
    def _build_request(self, rule_index, link):
        base_meta=dict(rule=rule_index, link_text=link.text)
        base_meta.update(link.meta)
        print('link 更新 meta ===')
        return Request(
            url=link.url,
            callback=self._callback,
            errback=self._errback,
            meta=base_meta
        )
    def parse_item(self, response):
        # 从 `meta` 信息中获取 `item_name`、`item_date` 和 `current_page`
        print(response.meta)

        item_name = response.meta.get('name')
        item_date = response.meta.get('date')
        page = response.meta.get('page')

        # 在这里编写解析逻辑
        # 创建并返回 `YourItem` 实例
        item = {}
        item['url'] = response.url
        item['name'] = item_name
        item['date'] = item_date
        item['page'] = page
        print('parse item')

        return item
