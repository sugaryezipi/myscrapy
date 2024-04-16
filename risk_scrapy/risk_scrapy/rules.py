
from risk_scrapy.zegbee_middleware import MyLxmlLinkExtractor

from scrapy.spiders import Rule

rules = {
    'china': (Rule(MyLxmlLinkExtractor(allow='article\/.*\.html',
                                       restrict_xpaths='//div[@id="rank-defList"]//div[@class="item-con-inner"]',


                                       restrict_extra_xpath={'name': './/a/text()',
                                                             'date': './/span[@class="time"]/text()',
                                                             },
                                       extra_xpath={'page': '//div[@class="page"]/span/text()'},
                                       ext_params=['page', 'name', 'date']
                                       ),
                   callback='parse_item',

                   ),
    # Rule(MyLxmlLinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
)
}