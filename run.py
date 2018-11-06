#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
Purpose: 启动文件，通过运行该文件启动爬虫及周期校验程序
Author: YajunZheng
Created: 2018/10/25
"""

import logging
import time
from multiprocessing import Pool

import gevent
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool

from pool import settings
from pool.core import ip_crawl, tool_lib

log_pause = logging.getLogger('Crawl_Pause')

def xicidaili():
    while True:
        try:
            th_pool = Pool(settings.VERIFY_MAX_CONCURRENT)           # 初始化协程池
            xici = ip_crawl.XicidailiCrawl()                        # 实例化西刺代理爬虫对象
            for each_table in xici.start_requests():
                threads = []
                for each_tr in each_table:
                    threads.append(th_pool.spawn(xici.parse_ip_info, each_tr))           # 构造协程列表
                gevent.joinall(threads)                                                 # 启动协程
                time.sleep(settings.PAGE_SLEEP_TIME)
            log_pause.info('XICI FINISHED')
            time.sleep(settings.CRAWL_SLEEP_TIME)
        except:
            log_pause.warning('ERROR 503')                 # 利用代理ip访问西刺可能遇到封ip的情况，此时打印503错误，切换ip重连
            time.sleep(settings.CRAWL_SLEEP_TIME/100)



def kuaidaili():
    while True:
        try:
            th_pool = Pool(settings.VERIFY_MAX_CONCURRENT)
            kuai = ip_crawl.KuaidailiCrawl()
            for each_table in kuai.start_requests():
                threads = []
                for each_tr in each_table:
                    threads.append(th_pool.spawn(kuai.parse_ip_info, each_tr))
                gevent.joinall(threads)
                time.sleep(settings.PAGE_SLEEP_TIME)
            log_pause.info('KUAI FINISHED')
            time.sleep(settings.CRAWL_SLEEP_TIME)
        except:
            log_pause.warning('ERROR 503')
            time.sleep(settings.CRAWL_SLEEP_TIME/100)


if __name__ == '__main__':
    """程序启动后不必关闭，放置后台运行，爬虫及验证周期时长设置请参照settings.py"""
    p = Pool(3)                                                  # 初始化进程池
    p.apply_async(xicidaili)                                    # 将xicidaili添加到进程池
    p.apply_async(kuaidaili)                                   # 将kuaidaili添加到进程池
    p.apply_async(tool_lib.periodic_verify)                   # 将循环验证函数添加到进程池
    p.join()                                                 # 启动

