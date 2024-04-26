import json
import logging
import operator
from functools import partial
from urllib.parse import urljoin, urlparse

import jmespath
from lxml import etree
from parsel.csstranslator import HTMLTranslator
from scrapy import Selector, FormRequest
from w3lib.html import strip_html5_whitespace
from w3lib.url import canonicalize_url, safe_url_string

from scrapy.linkextractors import (
    IGNORED_EXTENSIONS,
    _is_valid_url,
    _matches,
    _re_type,
    re,
)
from scrapy.utils.misc import arg_to_iter, rel_has_nofollow
from scrapy.utils.python import unique as unique_list
from scrapy.utils.response import get_base_url
from scrapy.utils.url import url_has_any_extension, url_is_from_any_domain

logger = logging.getLogger(__name__)

# from lxml/src/lxml/html/__init__.py
XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"

_collect_string_content = etree.XPath("string()")


def _nons(tag):
    if isinstance(tag, str):
        if tag[0] == "{" and tag[1 : len(XHTML_NAMESPACE) + 1] == XHTML_NAMESPACE:
            return tag.split("}")[-1]
    return tag


def _identity(x):
    return x


def _canonicalize_link_url(link):
    return canonicalize_url(link.url, keep_fragments=True)



"""
This modules implements the CrawlSpider which is the recommended spider to use
for scraping typical web sites that requires crawling pages.

See documentation in docs/topics/spiders.rst
"""

import copy
from typing import AsyncIterable, Awaitable, Sequence

from scrapy.http import HtmlResponse, Request, Response, JsonRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.utils.asyncgen import collect_asyncgen
from scrapy.utils.spider import iterate_spider_output


def _identity(x):
    return x


def _identity_process_request(request, response):
    return request


def _get_method(method, spider):
    if callable(method):
        return method
    if isinstance(method, str):
        return getattr(spider, method, None)





class Rule:
    def __init__(
        self,
        link_extractor=None,
        callback=None,
        cb_kwargs=None,
        follow=None,
        process_links=None,
        process_request=None,
        errback=None,
        req_method='GET',
        req_data=None
    ):
        self.link_extractor = link_extractor or _default_link_extractor
        self.callback = callback
        self.errback = errback
        self.cb_kwargs = cb_kwargs or {}
        self.process_links = process_links or _identity
        self.process_request = process_request or _identity_process_request
        self.follow = follow if follow is not None else not callback
        self.req_method = req_method
        self.req_data = req_data if req_data is not None else {}

    def _compile(self, spider):
        self.callback = _get_method(self.callback, spider)
        self.errback = _get_method(self.errback, spider)
        self.process_links = _get_method(self.process_links, spider)
        self.process_request = _get_method(self.process_request, spider)


class CrawlSpider(Spider):
    rules: Sequence[Rule] = ()

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._compile_rules()

    def start_requests(self):
        '''
          "start_requests":{
                "method": "POST",
                "data": {"product_id": 1},
                "meta":{}
              },
        :return:
        '''
        for url in self.start_urls:
            method=self.config.get('start_requests',{}).get('method',"GET")
            meta=self.config.get('start_requests',{}).get('meta',{})
            data = {}
            # 如果是POST请求，获取请求数据
            if method != "GET":
                data = self.config.get('start_requests',{}).get('data',{})
                print('生成data:  ', data)
            print('url::',url)
            if method == "GET":
                # GET请求
                yield Request(
                    url=url,
                    method=method,
                    errback=self._errback,
                    meta=meta
                )

            elif method == "POST":
                # POST请求
                yield FormRequest(
                    url=url,
                    method="POST",
                    formdata=data,
                    errback=self._errback,
                    meta=meta
                )
            elif method == "JSON":
                # JSON请求
                yield JsonRequest(
                    url=url,
                    method="POST",
                    data=data,
                    errback=self._errback,
                    meta=meta
                )
            else:
                raise ValueError("Unsupported HTTP method: {}".format(method))
    def _parse(self, response, **kwargs):
        return self._parse_response(
            response=response,
            callback=self.parse_start_url,
            cb_kwargs=kwargs,
            follow=True,
        )

    def parse_start_url(self, response, **kwargs):
        return []

    def process_results(self, response: Response, results: list):
        return results

    def _build_request(self, rule_index, link,**kwargs):
        base_meta = dict(rule=rule_index, link_text=link.text)
        base_meta.update(link.meta)
        # 自己传入的字段

        method = "GET"
        data = {}

        if kwargs and kwargs.get('req_method'):
            # 根据参数中传递的请求方法来设置method变量
            method = kwargs.get('req_method').upper()

            # 如果是POST请求，获取请求数据
            if method != "GET":
                req_data_ = kwargs.get('req_data',{})
                data={}
                for k, v in req_data_.items():
                    if v['source']=='meta':
                        data[k] = base_meta[v['value']]
                    else:
                        data[k] = v['value']
                print('生成data:  ',data)
                # 'product_id': {'value': 'next_page',
                #                'source': 'meta'},
                # 'product_id2': {'value': 'next_page',
                #                 'source': 'constant'}
        # 根据请求方法来选择合适的Scrapy请求类型
        if method == "GET":
            # GET请求
            return Request(
                url=link.url,
                method=method,
                callback=self._callback,
                errback=self._errback,
                meta=base_meta
            )
        elif method == "POST":
            # POST请求
            return FormRequest(
                url=link.url,
                method="POST",
                formdata=data,
                callback=self._callback,
                errback=self._errback,
                meta=base_meta
            )
        elif method == "JSON":
            # JSON请求
            return JsonRequest(
                url=link.url,
                method="POST",
                data=data,
                callback=self._callback,
                errback=self._errback,
                meta=base_meta
            )
        else:
            raise ValueError("Unsupported HTTP method: {}".format(method))

    def _requests_to_follow(self, response):
        # if not isinstance(response, HtmlResponse):
        #     return
        seen = set()
        for rule_index, rule in enumerate(self._rules):
            links = [
                lnk
                for lnk in rule.link_extractor.extract_links(response)
                if lnk not in seen
            ]
            for link in rule.process_links(links):
                seen.add(link)
                request = self._build_request(rule_index, link,req_method=rule.req_method,req_data=rule.req_data)
                yield rule.process_request(request, response)

    def _callback(self, response, **cb_kwargs):
        rule = self._rules[response.meta["rule"]]
        return self._parse_response(
            response, rule.callback, {**rule.cb_kwargs, **cb_kwargs}, rule.follow
        )

    def _errback(self, failure):
        rule = self._rules[failure.request.meta["rule"]]
        return self._handle_failure(failure, rule.errback)

    async def _parse_response(self, response, callback, cb_kwargs, follow=True):
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            if isinstance(cb_res, AsyncIterable):
                cb_res = await collect_asyncgen(cb_res)
            elif isinstance(cb_res, Awaitable):
                cb_res = await cb_res
            cb_res = self.process_results(response, cb_res)
            for request_or_item in iterate_spider_output(cb_res):
                yield request_or_item

        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                yield request_or_item

    def _handle_failure(self, failure, errback):
        if errback:
            results = errback(failure) or ()
            for request_or_item in iterate_spider_output(results):
                yield request_or_item

    def _compile_rules(self):
        self._rules = []
        for rule in self.rules:
            self._rules.append(copy.copy(rule))
            self._rules[-1]._compile(self)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            "CRAWLSPIDER_FOLLOW_LINKS", True
        )
        return spider


import pandas as pd

class JsonLinkExtractor:
    '''
                 'url':'',
                 'url_prefix':"",  自己填写
                'base_url':'',  一定要有 {}    自己填写
                'base_format_id':'',
                ========================
                  'next_page_url':'',
                 'next_page_url_prefix':"", 自己填写
                'next_page_base_url':'',  一定要有 {}  自己填写
                'next_page_base_format_id':'',

    '''
    def __init__(self, *args, **kwargs):
        self.restrict_json = kwargs.pop('restrict_json', {})
        self.extra_json = kwargs.pop('extra_json', {})
        self.ext_params = kwargs.pop('ext_params', {})
        self.unique = True

    def ensure_list(self, value):
        if isinstance(value, list):
            return value
        else:
            # 如果不是列表，将其包装在一个列表中
            return [value]

    def extract_links(self, response):
        res = json.loads(response.text)
        print('res=========',res)

        extra_json_obj = {}
        # 全局
        if self.extra_json:
            has_next_page=self.extra_json.get('next_page_url')
            for k, v in self.extra_json.items():
                if k == 'next_page_url_prefix' or k =='next_page_base_url' or k =='post_url':
                    continue
                if not has_next_page:
                    # 没有指定url
                    if k == 'next_page_base_format_id':
                        base_format_value = jmespath.search(v, res)
                        base_url_ = self.restrict_json.get('next_page_base_url')
                        extra_json_obj['next_page_url'] = base_url_.format(base_format_value)

                print('k {} ==> v {}'.format(k, v))
                extra_json_obj[k] = jmespath.search(v, res)
        print('extra_json_obj  ==>', extra_json_obj)
        restrict_extra_json_obj = {}
        has_url= self.restrict_json.get('url')
        for k, v in self.restrict_json.items():
            if k=='url_prefix' or k == 'base_url' or k=='post_url':
                continue
            if not has_url:
                #没有指定url
                if k=='base_format_id':
                    base_format_value=jmespath.search(v, res)
                    base_url_=self.restrict_json.get('base_url')
                    restrict_extra_json_obj['url']=self.ensure_list(base_url_.format(base_format_value))
                    # 拼接url

            restrict_extra_json_obj[k] = self.ensure_list(jmespath.search(v, res))
        df = pd.DataFrame(restrict_extra_json_obj)
        restrict_extra_list = df.to_dict(orient='records')
        if restrict_extra_list:
            final_list = [{**extra_json_obj, **restrict_} for restrict_ in restrict_extra_list]
        else:
            final_list = [extra_json_obj]
        all_links=[]
        print('final_list ::: ',final_list)
        for restrict_ in final_list:
            restrict_['ext_params'] = self.ext_params
            if restrict_.get('url'):
                url= restrict_.pop('url')
                if self.restrict_json.get('url_prefix')  and url:
                    url=self.restrict_json.get('url_prefix')+url
            else:
                url= restrict_.get('next_page_url')
                if url:
                    url = restrict_.pop('next_page_url')
                    if self.extra_json.get('next_page_url_prefix') and url :
                        url = self.extra_json.get('next_page_url_prefix') + url
                else:
                    url = self.extra_json.get('next_page_post_url') or self.restrict_json.get('post_url') or  self.extra_json.get('post_url')
            if url:
                all_links.append(Link(url,meta=restrict_))

        if self.unique:
            return unique_list(all_links)
        return all_links




class Link:
    """Link objects represent an extracted link by the LinkExtractor, now with additional meta data.

    Using the anchor tag sample below to illustrate the parameters::

            <a href="https://example.com/nofollow.html#foo" rel="nofollow">Product 1 Name</a>
            <!-- Assuming there's a way to extract metadata like this -->
            <p class="product-meta">Publish Time: 2023-01-01</p>

    :param url: the absolute url being linked to in the anchor tag.
                From the sample, this is ``https://example.com/nofollow.html``.

    :param text: the text in the anchor tag, often used as the product name. From the sample, this is ``Product 1 Name``.

    :param fragment: the part of the url after the hash symbol. From the sample, this is ``foo``.

    :param nofollow: an indication of the presence or absence of a nofollow value in the ``rel`` attribute
                    of the anchor tag.

    :param meta: a dictionary to store extra metadata such as the product name and publish time.
    """

    __slots__ = ["url", "text", "fragment", "nofollow", "meta"]

    def __init__(self, url, text="", fragment="", nofollow=False, meta=None):
        if not isinstance(url, str):
            got = url.__class__.__name__
            raise TypeError(f"Link urls must be str objects, got {got}")
        self.url = url
        self.text = text
        self.fragment = fragment
        self.nofollow = nofollow
        self.meta = {} if meta is None else meta

    def add_meta(self, obj):
        """Adds a single piece of metadata."""
        for k,v in obj.items():

            self.meta[k] = v
    def get_meta_keys(self):
        return list(self.meta.keys())
    def __eq__(self, other):
        return (
            self.url == other.url
            and self.text == other.text
            and self.fragment == other.fragment
            and self.nofollow == other.nofollow

        )

    def __hash__(self):
        return (
            hash(self.url)
            ^ hash(self.text)
            ^ hash(self.fragment)
            ^ hash(self.nofollow)
        )

    def __repr__(self):
        meta_str = ", ".join([f"{k}={v!r}" for k, v in self.meta.items()])
        return (
            f"Link(url={self.url!r}, text={self.text!r}, "
            f"fragment={self.fragment!r}, nofollow={self.nofollow!r}, "
            f"meta={{{meta_str}}})"
        )



class MyLxmlParserLinkExtractor:
    def __init__(
        self,
        tag="a",
        attr="href",
        process=None,
        unique=False,
        strip=True,
        canonicalized=False,
        restrict_extra_xpath=None,
        restrict_extra_json=None,


    ):

        self.scan_tag = tag if callable(tag) else partial(operator.eq, tag)
        self.scan_attr = attr if callable(attr) else partial(operator.eq, attr)
        self.process_attr = process if callable(process) else _identity
        self.unique = unique
        self.strip = strip
        self.link_key = (
            operator.attrgetter("url") if canonicalized else _canonicalize_link_url
        )
        self.restrict_extra_xpath=restrict_extra_xpath
        self.restrict_json=restrict_extra_json

    def _iter_links(self, document):
        for el in document.iter(etree.Element):
            if not self.scan_tag(_nons(el.tag)):
                continue
            attribs = el.attrib
            for attrib in attribs:
                if not self.scan_attr(attrib):
                    continue
                yield (el, attrib, attribs[attrib])

    def _extract_links(self, selector, response_url, response_encoding, base_url):
        links = []
        # hacky way to get the underlying lxml parsed document
        for el, attr, attr_val in self._iter_links(selector.root):
            # pseudo lxml.html.HtmlElement.make_links_absolute(base_url)
            try:
                if self.strip:
                    attr_val = strip_html5_whitespace(attr_val)
                attr_val = urljoin(base_url, attr_val)
            except ValueError:
                continue  # skipping bogus links
            else:
                url = self.process_attr(attr_val)
                if url is None:
                    continue
            try:
                url = safe_url_string(url, encoding=response_encoding)
            except ValueError:
                logger.debug(f"Skipping extraction of link with bad URL {url!r}")
                continue
            custom_data = {}

            if self.restrict_extra_xpath:
                for attr_name, extra_xpath in self.restrict_extra_xpath.items():

                    for extra_tag in selector.xpath(extra_xpath):
                        print('extra_tag:::',extra_tag)
                        print('type (extra_tag):::',type(extra_tag))
                        if not extra_xpath:continue
                        # 提取自定义数据

                        if not custom_data.get(attr_name):
                            custom_data[attr_name]=extra_tag.get()

            # if self.restrict_json:
            #     for attr_name, extra_json in self.restrict_json.items():
            #         # 这里要用jmspath 来解析
            #         jmes_value=jmespath.search(extra_json,)


            link = Link(
                urljoin(base_url, attr_val),
                _collect_string_content(el) or "",
                nofollow=rel_has_nofollow(el.get("rel")),
            )
            link.add_meta(custom_data)
            links.append(link)
        return self._deduplicate_if_needed(links)

    def extract_links(self, response):
        base_url = get_base_url(response)
        return self._extract_links(
            response.selector, response.url, response.encoding, base_url
        )

    def _process_links(self, links):
        """Normalize and filter extracted links

        The subclass should override it if necessary
        """
        return self._deduplicate_if_needed(links)

    def _deduplicate_if_needed(self, links):
        if self.unique:
            return unique_list(links, key=self.link_key)
        return links

class MyLxmlLinkExtractor:
    _csstranslator = HTMLTranslator()

    def __init__(
        self,
        allow=(),
        deny=(),
        allow_domains=(),
        deny_domains=(),
        restrict_xpaths=(),
        tags=("a", "area"),
        attrs=("href",),
        canonicalize=False,
        unique=True,
        process_value=None,
        deny_extensions=None,
        restrict_css=(),
        strip=True,
        restrict_text=None,
        restrict_extra_xpath=None,
        restrict_extra_json=None,
        extra_xpath=None,
        extra_json=None,
        ext_params=None
        # 由前端传入
    ):
        tags, attrs = set(arg_to_iter(tags)), set(arg_to_iter(attrs))
        self.link_extractor = MyLxmlParserLinkExtractor(
            tag=partial(operator.contains, tags),
            attr=partial(operator.contains, attrs),
            unique=unique,
            process=process_value,
            strip=strip,
            canonicalized=canonicalize,
            restrict_extra_xpath=restrict_extra_xpath,
            restrict_extra_json=restrict_extra_json,

        )
        self.allow_res = [
            x if isinstance(x, _re_type) else re.compile(x) for x in arg_to_iter(allow)
        ]
        self.deny_res = [
            x if isinstance(x, _re_type) else re.compile(x) for x in arg_to_iter(deny)
        ]
        self.extra_xpath = extra_xpath
        self.extra_json = extra_json
        self.allow_domains = set(arg_to_iter(allow_domains))
        self.deny_domains = set(arg_to_iter(deny_domains))

        self.restrict_xpaths = tuple(arg_to_iter(restrict_xpaths))
        self.restrict_xpaths += tuple(
            map(self._csstranslator.css_to_xpath, arg_to_iter(restrict_css))
        )

        if deny_extensions is None:
            deny_extensions = IGNORED_EXTENSIONS
        self.canonicalize = canonicalize
        self.deny_extensions = {"." + e for e in arg_to_iter(deny_extensions)}
        self.restrict_text = [
            x if isinstance(x, _re_type) else re.compile(x)
            for x in arg_to_iter(restrict_text)
        ]
        self.ext_params=ext_params

    def _link_allowed(self, link):
        if not _is_valid_url(link.url):
            return False
        if self.allow_res and not _matches(link.url, self.allow_res):
            return False
        if self.deny_res and _matches(link.url, self.deny_res):
            return False
        parsed_url = urlparse(link.url)
        if self.allow_domains and not url_is_from_any_domain(
            parsed_url, self.allow_domains
        ):
            return False
        if self.deny_domains and url_is_from_any_domain(parsed_url, self.deny_domains):
            return False
        if self.deny_extensions and url_has_any_extension(
            parsed_url, self.deny_extensions
        ):
            return False
        if self.restrict_text and not _matches(link.text, self.restrict_text):
            return False
        return True

    def matches(self, url):
        if self.allow_domains and not url_is_from_any_domain(url, self.allow_domains):
            return False
        if self.deny_domains and url_is_from_any_domain(url, self.deny_domains):
            return False

        allowed = (
            (regex.search(url) for regex in self.allow_res)
            if self.allow_res
            else [True]
        )
        denied = (regex.search(url) for regex in self.deny_res) if self.deny_res else []
        return any(allowed) and not any(denied)

    def _process_links(self, links):
        links = [x for x in links if self._link_allowed(x)]
        if self.canonicalize:
            for link in links:
                link.url = canonicalize_url(link.url)
        links = self.link_extractor._process_links(links)
        return links

    def _extract_links(self, *args, **kwargs):

        # 传入 restrict_extra_xpath ，key 和value ，除了解析url，也把自定义的东西解析出来
        return self.link_extractor._extract_links(*args, **kwargs)

    def extract_links(self, response):
        """Returns a list of :class:`~scrapy.link.Link` objects from the
        specified :class:`response <scrapy.http.Response>`.

        Only links that match the settings passed to the ``__init__`` method of
        the link extractor are returned.

        Duplicate links are omitted if the ``unique`` attribute is set to ``True``,
        otherwise they are returned.
        """
        base_url = get_base_url(response)
        extra_xpath_value={}
        if self.extra_xpath:
            for k,v in self.extra_xpath.items():
                extra_xpath_value[k]=response.xpath(v).get()
        if self.restrict_xpaths:
            docs = [
                subdoc for x in self.restrict_xpaths for subdoc in response.xpath(x)
            ]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        for link in all_links:
            link.add_meta(extra_xpath_value)
            link.add_meta({'ext_params':self.ext_params})
            # 把要解析的参数放到meta


        if self.link_extractor.unique:
            return unique_list(all_links)
        return all_links

    def _extract_links_back(self, *args, **kwargs):
        return self.link_extractor._extract_links(*args, **kwargs)

    def extract_links_back(self, response):
        """Returns a list of :class:`~scrapy.link.Link` objects from the
        specified :class:`response <scrapy.http.Response>`.

        Only links that match the settings passed to the ``__init__`` method of
        the link extractor are returned.

        Duplicate links are omitted if the ``unique`` attribute is set to ``True``,
        otherwise they are returned.
        """
        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [
                subdoc for x in self.restrict_xpaths for subdoc in response.xpath(x)
            ]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))

        if self.link_extractor.unique:
            return unique_list(all_links)
        return all_links


_default_link_extractor = MyLxmlLinkExtractor()
