import sys
from scrapy.utils.project import get_project_settings

from utils import get_config
from scrapy.crawler import CrawlerProcess

def run():
    # name = sys.argv[1]
    name = 'json_post_demo'
    # name = 'china'
    custom_settings = get_config(name)
    # 爬取使用的 Spider 名称
    spider = custom_settings.get('spider', 'json_post_demo')
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