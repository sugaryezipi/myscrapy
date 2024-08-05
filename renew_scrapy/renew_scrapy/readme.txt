url 分三种 一种是网页给到链接，可能只缺个前缀 url url_prefix   /  next_page_url  next_page_url_prefix
第二种 ，可能只有个页数 ，其余url 要自己format拼接 对应 base_url base_format_id / next_page_base_url   next_page_base_format_id
第三种post 直接写死， 对应 post_url /next_page_post_url

爬虫分为翻页和当前页列表

'''
 'url':'',    post的话就写post 的url
 'url_prefix':"",  自己填写  网页给出url 直接拼接
 ------------------------
'base_url':'',  一定要有 {}    自己填写
'base_format_id':'',    只有个页数 ，要自己拼接 or post

'post_url': '', 如果是post的话 就写post 的url

========================
 'next_page_url':'',  post的话就写post 的url
 'next_page_url_prefix':"", 自己填写
 --------------
'next_page_base_url':'',  一定要有 {}  自己填写
'next_page_base_format_id':'',
'next_page_post_url': '', 翻页post的话就写post 的url

'''

rules的使用：
爬虫目前分为列表和详情
如果直接进的详情 ： restrict_json 和  extra_json 都一样 但是不要写 url
    rule 的参数：
     req_method='POST',"GET","JSON" ,post指的是post-formdata ，urlendcode的那种，json指的是post-json
   req_data={
            'product_id': {'value':'next_page',
                           'source':'meta'},
             'product_id2': {'value': 'next_page',
                            'source': 'constant'}
             # 这个next-page是上面的key， 第二页的时候 就会替换成真实值
         }
     {'value':'next_page','source':'meta'},   指的是要去从meta中取next_page 值，因此 extra_json or restrict_json 必须包括 next_page post中dict的变量如页数
     {'value': 'next_page','source': 'constant'} 指的是常量，post中dict的常量 如xx
     如果遇到post中有时间戳等  需要自己在中间件中写。


from renew_scrapy.zegbee_middleware import MyLxmlLinkExtractor,JsonLinkExtractor

from renew_scrapy.zegbee_middleware import  Rule



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

                                                   'url':'products[*].detail_url',
                                                   'url_prefix':'http://127.0.0.1:8000'

                                                   },
                                    extra_json={'cur_page': 'current_page',
                                                'next_page':'next_page'
                                                },
                                    ext_params=['name', 'created_at', 'cur_page'],

                                    ),
             callback='parse_item',

                  ),
            Rule(JsonLinkExtractor(restrict_json={},
                                                extra_json={
                                                            'post_url':'http://127.0.0.1:8000/demo_products',
                                                            'next_page':'next_page'
                                                            },
                                                ext_params=[]
                                                ),

                 req_method='JSON',
                 req_data={
                     'product_id': {'value': 'next_page',
                                    'source': 'meta'},

                     # 这个next-page是上面的key， 第二页的时候 就会替换成真实值
                 }

                              ),
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

 "datetime": {
        "method": "xpath",
        "args": "//div[@class='post_info']//text()",
        "re": "(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})"
      }

任何的xpath  正则的话必须带括号 ，源码取的是 （1）

配置文件说明
{
  "spider": "common_get_xpath",
  "website": "网易新闻",
  "type": "新闻",
  "index": "https://news.163.com/",
  "settings": {
    "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
  },
  "start_urls": [
    "https://news.163.com/"
  ],
  "allowed_domains": [
    "163.com"
  ],
  "rules": {
    "articles": {
        "link_ext_type": "MyLxmlLinkExtractor",
        "allow": "article/.*?\\.html",
        "restrict_xpaths": "//li[@class='newsdata_item']/div[@class='hidden']",
        "restrict_extra_xpath": {
            "title_1": {
                "method": "xpath",
                "args": ".//a/text()",
                "re": ""
            }

        },
        "extra_xpath": {
        },
        "ext_params": [

        ]
    }

},

  "item": {
    "class": "NewsItem",
    "loader": "ChinaLoader",
    "attrs": {
      "title": {
        "method": "xpath",
        "args": "//h1[@class='post_title']/text()"
      },
      "url": {
        "method": "attr",
        "args": "url"
      },
      "text": {
        "method": "xpath",
        "args": "//div[@class='post_body']//text()"
      },
      "datetime": {
        "method": "xpath",
        "args": "//div[@class='post_info']//text()",
        "re": "(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})"
      },
      "source": {
        "method": "xpath",
        "args": "//div[@class='post_info']//text()",
        "re": "来源：(.*)"
      },
      "website": {
        "method": "value",
        "args": "网易新闻"

      }
    }
  }
}

