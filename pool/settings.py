"""
Purpose: 定义全局配置及变量
Created: 2018/10/22
Author: YajunZheng
"""

import random

# 请求头user-agent
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

# 有效ip保存位置
DATA_FILE_NAME = r"ip_data.json"

# 爬虫最大并发数
CRAWL_MAX_CONCURRENT = 5

# 验证请求并发数
VERIFY_MAX_CONCURRENT = 5

# 爬虫单次执行完休眠时间，单位秒
CRAWL_SLEEP_TIME = random.uniform(500, 800)

# 爬虫翻页周期，单位秒
PAGE_SLEEP_TIME = random.uniform(6, 9)

# 本地验证周期，单位秒
VALIDATION_SLEEP_TIME = 60

