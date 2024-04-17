# test proxy
import aiohttp
from loguru import logger
logger.add('./proxy_demo.log')

username = "d2135401422"
password = "xqh76h0s"

proxy_auth = aiohttp.BasicAuth(username, password)


import aiohttp
import asyncio
import numpy as np
from aiohttp import ClientSession
from statistics import mean

# 目标 URL
url = "https://www.baidu.com"

# 测试次数
num_requests = 300

# 代理地址



# 异步请求函数
async def fetch(session, url):
    start_time = asyncio.get_event_loop().time()
    try:
        async with session.get(url, proxy=proxy,proxy_auth=proxy_auth,ssl=False) as response:
            end_time = asyncio.get_event_loop().time()
            response_time = end_time - start_time
            # 判断状态码是否为 200
            if response.status == 200:
                logger.info(f'{proxy} ==> {response_time}')
                return response_time, True
            else:
                logger.info(f"请求失败，状态码: {response.status}")
                return None, False
    except Exception as e:
        logger.info(f"请求失败：{e}")
        return None, False

# 执行异步测试
async def main():
    # 创建一个 ClientSession
    async with ClientSession() as session:
        tasks = []
        response_times = []
        success_count = 0
        fail_count = 0

        # 创建异步请求任务
        for _ in range(num_requests):
            task = asyncio.create_task(fetch(session, url))
            tasks.append(task)

        # 等待所有任务完成
        for task in asyncio.as_completed(tasks):
            response_time, success = await task
            if success:
                response_times.append(response_time)
                success_count += 1
            else:
                fail_count += 1

        # 使用 numpy 计算统计数据
        if response_times:
            response_times_np = np.array(response_times)
            p99 = np.percentile(response_times_np, 99)
            p90 = np.percentile(response_times_np, 90)
            p50 = np.percentile(response_times_np, 50)
            mean_response_time = mean(response_times)
            max_response_time = np.max(response_times_np)
            min_response_time = np.min(response_times_np)
        else:
            p99 = p90 = p50 = mean_response_time = max_response_time = min_response_time = None

        # 输出统计信息
        logger.info(f"成功次数: {success_count}")
        logger.info(f"失败次数: {fail_count}")
        logger.info(f"均值: {mean_response_time}")
        logger.info(f"最大值: {max_response_time}")
        logger.info(f"最小值: {min_response_time}")
        logger.info(f"p99: {p99}")
        logger.info(f"p90: {p90}")
        logger.info(f"p50: {p50}")


async def check_ip(proxy):
    async with ClientSession() as session:
        async with session.get('https://ifconfig.me/', proxy=proxy, proxy_auth=proxy_auth) as response:
            # 判断状态码是否为 200
            res_rtext=await response.text()
            logger.info(res_rtext)


proxy = "http://123.96.41.12:19761"


# asyncio.run(check_ip(proxy))
asyncio.run(main())
