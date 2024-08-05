import sys
from scrapy.utils.project import get_project_settings

from scrapy.crawler import CrawlerProcess
from os.path import realpath, dirname
import json
def get_config(name):
    path = dirname(realpath(__file__)) + '\\configs\\' + name + '.json'
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())
def run():
    # name = sys.argv[1]
    name = 'wangyi_news'
    # name = 'china'
    custom_settings = get_config(name)
    # 爬取使用的 Spider 名称
    spider = custom_settings.get('spider', name)
    project_settings = get_project_settings()
    print('project_settings  :: ',project_settings)
    settings = dict(project_settings.copy())
    # 合并配置
    settings.update(custom_settings.get('settings'))
    print('final settings::',settings)
    process = CrawlerProcess(settings)
    # 启动爬虫
    process.crawl(spider, **{'name': name})
    process.start()

if __name__ == '__main__':
    run()