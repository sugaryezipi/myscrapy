
from renew_scrapy.zegbee_middleware import MyLxmlLinkExtractor,JsonLinkExtractor

from renew_scrapy.zegbee_middleware import  Rule

'''
'url': '',
'url_prefix': "", 
 =========
'base_url': '',
'base_format_id': ' 帶{} ',
'''

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
),
'json_demo':(Rule(JsonLinkExtractor(restrict_json={'name': 'products[*].name',
                                                    'created_at':'products[*].created_at',

                                                   'url':'products[*].detail_url',
                                                   'url_prefix':'http://127.0.0.1:8000'

                                                   },
                                    extra_json={'cur_page': 'current_page',
                                                'next_page':'next_page_url'
                                                },
                                    ext_params=['name', 'created_at', 'cur_page']
                                    ),
             callback='parse_item',
                  ),

             )

}


rules = {

'json_demo':(Rule(JsonLinkExtractor(restrict_extra_json={'name': 'products[*].name',
                                                    'created_at':'products[*].created_at',

                                                   'url':'products[*].detail_url',
                                                   'url_prefix':'http://127.0.0.1:8000'

                                                   },
                                    extra_json={'cur_page': 'current_page',
                                                'next_page':'next_page_url'
                                                },
                                    transfer_params=['name', 'created_at', 'cur_page']
                                    ),
             callback='parse_item',
                  ),

             )

}