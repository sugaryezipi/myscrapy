
from renew_scrapy.zegbee_middleware import MyLxmlLinkExtractor,JsonLinkExtractor

from renew_scrapy.zegbee_middleware import  Rule

'''
 
 'url':'',    post的话就写post 的url
 'url_prefix':"",  自己填写  网页给出url 直接拼接 
 ------------------------
'base_url':'',  一定要有 {}    自己填写
'base_format_id':'',    只有个页数 ，要自己拼接 or post  
========================
  'next_page_url':'',  post的话就写post 的url
 'next_page_url_prefix':"", 自己填写
 --------------
'next_page_base_url':'',  一定要有 {}  自己填写
'next_page_base_format_id':'',

------------------------
 "name": {
          "method": "xpath",
          "args": "//div[@class='page']/span/text()",
          "re":""
        }
      ,
'''

rules = {
    'china': (Rule(MyLxmlLinkExtractor(allow='article\/.*\.html',
                                       restrict_xpaths='//div[@id="rank-defList"]//div[@class="item-con-inner"]',


                                       restrict_extra_xpath={
                                                             "name": {
                                                              "method": "xpath",
                                                              "args": ".//a/text()",
                                                              "re":""
                                                            },
                                                             "date": {
                                                              "method": "xpath",
                                                              "args": ".//span[@class='time']/text()",
                                                              "re":""
                                                            }
                                                             },
                                       extra_xpath={'page': {
                                                              "method": "xpath",
                                                              "args": "//div[@class='page']/span/text()",
                                                              "re":""
                                                            }},
                                       ext_params=['page', 'name', 'date']
                                       ),
                   callback='parse_item',

                   ),
    Rule(MyLxmlLinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))

),
    # 问题1  extra_xpath 中xpath以后还得要正则
    #  self.req_method = req_method
    #     self.req_data = req_data
'json_demo':(
    Rule(JsonLinkExtractor(restrict_json={'name': 'products[*].name',
                                                    'created_at':'products[*].created_at',

                                                   'url':'products[*].detail_url',
                                                   'url_prefix':'http://127.0.0.1:8000'

                                                   },
                                    extra_json={'cur_page': 'current_page',
                                                'next_page':'next_page_url'
                                                },
                                    ext_params=['name', 'created_at', 'cur_page'],

                                    ),
             callback='parse_item',
            req_method='POST',
             req_data={
                'product_id': {'value':'next_page',
                               'source':'meta'},
                 'product_id2': {'value': 'next_page',
                                'source': 'constant'}
                 # 这个next-page是上面的key， 第二页的时候 就会替换成真实值
             }
                  ),
            Rule(JsonLinkExtractor(restrict_json={},
                                                extra_json={
                                                            'next_page_url_prefix':'http://127.0.0.1:8000',
                                                            'next_page_url':'next_page_url'
                                                            },
                                                ext_params=[]
                                                ),

                              ),
             ),

'json_post_demo':(
    Rule(JsonLinkExtractor(restrict_json={'name': 'products[*].name',
                                                    'created_at':'products[*].created_at',

                                                   # 'url':'products[*].detail_url',
                                                   # 'url_prefix':'http://127.0.0.1:8000'

                                                   },
                                    extra_json={'cur_page': 'current_page',
                                                'next_page':'next_page'
                                                },
                                    ext_params=['name', 'created_at', 'cur_page'],

                                    ),
             callback='parse_item',

                  ),
            # Rule(JsonLinkExtractor(restrict_json={},
            #                                     extra_json={
            #                                                 'post_url':'http://127.0.0.1:8000/demo_products',
            #                                                 'next_page':'next_page'
            #                                                 },
            #                                     ext_params=[]
            #                                     ),
            #
            #      req_method='JSON',
            #      req_data={
            #          'product_id': {'value': 'next_page',
            #                         'source': 'meta'},
            #
            #          # 这个next-page是上面的key， 第二页的时候 就会替换成真实值
            #      }
            #
            #                   ),
             )


}

'''
'post_url': '', post的话就写post 的url
 'url':'',   
 'url_prefix':"",  自己填写  网页给出url 直接拼接 
 ------------------------
'base_url':'',  一定要有 {}    自己填写
'base_format_id':'',    只有个页数 ，要自己拼接 or post  
========================
'post_url': '', post的话就写post 的url

 'next_page_url':'',  
 'next_page_url_prefix':"", 自己填写
 --------------
'next_page_base_url':'',  一定要有 {}  自己填写
'next_page_base_format_id':'',

rule 多了这两个参数  
        self.req_method = req_method   GET  POST 
        self.req_data = req_data   （json形式的 ）
'''