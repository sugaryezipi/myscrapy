import aiohttp
import asyncio
import numpy as np
from statistics import mean

from aiohttp import ClientSession

# 设置日志
from loguru import logger
logger.add('./proxy_demo_batch.log')
# 代理认证信息（根据需求设置）
username = "d2135401422"
password = "xqh76h0s"

proxy_auth = aiohttp.BasicAuth(username, password)

# 要测试的目标 URL
url = "https://www.baidu.com"

# 每个 IP 要测试的请求次数
requests_per_ip = 20

# 最外层循环中的 IP 列表（需要替换为实际的 IP 列表）
ip_list = [
            "218.95.37.135:40740",
            "180.114.12.20:17491",
            "221.229.212.170:40859",
            "221.229.212.170:40072",
            "123.96.41.12:19761",
            "222.89.70.65:25104",
            "221.229.212.173:25022",
            "123.160.10.195:25196",
            "219.150.218.53:40194",
            "221.229.212.170:40283",
            "218.95.37.135:40590",
            "36.151.192.6:25204",
            "218.95.37.161:25129",
            "122.239.146.162:17307",
            "117.82.146.251:17448",
            "117.86.125.78:16507",
            "221.131.165.73:40925",
            "221.229.212.170:40431",
            "219.150.218.53:40441",
            "117.92.152.110:19200"
        ]  # 替换为实际的代理 IP 列表

# 异步请求函数
async def fetch(session, url, proxy):
    start_time = asyncio.get_event_loop().time()
    try:
        async with session.get(url, proxy=proxy, proxy_auth=proxy_auth, ssl=False) as response:
            end_time = asyncio.get_event_loop().time()
            response_time = end_time - start_time
            # 判断状态码是否为 200
            if response.status == 200:
                logger.info(f"{proxy}===>{response_time}")
                return response_time, True
            else:
                logger.info(f"请求失败，状态码: {response.status}")
                return None, False
    except Exception as e:
        logger.info(f"请求失败：{e}")
        return None, False

# 执行异步测试
async def test_ip(ip):
    async with ClientSession() as session:
        tasks = []
        response_times = []
        success_count = 0
        fail_count = 0

        # 创建异步请求任务
        for _ in range(requests_per_ip):
            task = asyncio.create_task(fetch(session, url, proxy=f"http://{ip}"))
            tasks.append(task)

        # 等待所有任务完成
        for task in asyncio.as_completed(tasks):
            response_time, success = await task
            if success:
                response_times.append(response_time)
                success_count += 1
            else:
                fail_count += 1

        return response_times, success_count, fail_count

# 最外层函数，循环测试所有 IP
async def main():
    # 存储每个 IP 的响应时间和统计数据
    all_response_times = []
    total_success_count = 0
    total_fail_count = 0

    # 循环遍历所有 IP
    for ip in ip_list:
        response_times, success_count, fail_count = await test_ip(ip)
        total_success_count += success_count
        total_fail_count += fail_count
        all_response_times.extend(response_times)
        await asyncio.sleep(0.5)

    # 使用 numpy 计算统计数据
    if all_response_times:
        response_times_np = np.array(all_response_times)
        p99 = np.percentile(response_times_np, 99)
        p90 = np.percentile(response_times_np, 90)
        p50 = np.percentile(response_times_np, 50)
        mean_response_time = mean(all_response_times)
        max_response_time = np.max(response_times_np)
        min_response_time = np.min(response_times_np)
    else:
        p99 = p90 = p50 = mean_response_time = max_response_time = min_response_time = None

    # 输出汇总的统计信息
    logger.info(f"总成功次数: {total_success_count}")
    logger.info(f"总失败次数: {total_fail_count}")
    logger.info(f"均值: {mean_response_time:.2f} 秒")
    logger.info(f"最大值: {max_response_time:.2f} 秒")
    logger.info(f"最小值: {min_response_time:.2f} 秒")
    logger.info(f"p99: {p99:.2f} 秒")
    logger.info(f"p90: {p90:.2f} 秒")
    logger.info(f"p50: {p50:.2f} 秒")

# 执行最外层函数
asyncio.run(main())
