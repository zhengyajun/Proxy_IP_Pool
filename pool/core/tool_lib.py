#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Purpose: 提供ip有效性验证、获取有效ip、周期性验证ip的有效性、删除ip等一系列工具函数
Author: YajunZheng
Created: 2018/10/25
"""

import sys
sys.path.append(r"./..")

import os
from os.path import abspath, dirname
import datetime
import gevent
from gevent.pool import Pool
from gevent import monkey; monkey.patch_all()

import logging
import logging.config
import json
import os
import random
import requests
import time
import yaml

from pool import settings

abs_path = dirname(abspath(__file__))       # 当前文件的绝对路径

"""初始化日志"""
log_conf_path = abs_path + r'/../../log.yml'
log_path = abs_path + r'/../../log/err.log'
with open(log_conf_path, 'r') as f_conf:
    dict_conf = yaml.load(f_conf)
    dict_conf['handlers']['err_file']['filename'] = log_path        # 改写日志配置文件，将日志文件夹的位置与当前执行文件的相对路径写死
logging.config.dictConfig(dict_conf)
logger = logging.getLogger('validation')
log_update = logging.getLogger('UPDATE')
log_get = logging.getLogger('GET_IP')
# log_pause = logging.getLogger('Crawl_Pause')


"""初始化json文件"""
folder_path = abs_path + r'/../../data/'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)                                # 文件夹不存在创建空文件夹

data_path = abs_path + r'/../../data/' + settings.DATA_FILE_NAME
if not os.path.exists(data_path):
    with open(data_path, 'w') as fp: fp.close()             # 文件不存在创建空文件

if os.path.getsize(data_path) == 0:
    init = []                                               # 若文件为空则初始化为空json数组
    with open(data_path, 'w') as fp:
        json.dump(init, fp)
        fp.close()


def ip_json_load():
    """读取json文件， 返回ip列表"""
    with open(data_path, 'r') as fp:
        ip_list = json.load(fp=fp)
        fp.close()
        return ip_list


def ip_json_dump(ip_list):
    """将ip列表写入json文件"""
    with open(data_path, 'w') as fp:
        json.dump(ip_list, fp=fp)
        fp.close()


def add_ip(new_ip_info):
    """将有效ip添加至json文件"""
    ip_list = ip_json_load()              # 从当前的json数组中获取ip_list
    if not isinstance(ip_list, list):
        ip_list = []
    if new_ip_info not in ip_list:
        ip_list.append(new_ip_info)               # 为ip_list添加新ip，并写入json文件
        ip_json_dump(ip_list)
        log_update.info("Add_IP: {0}".format(new_ip_info))
    else:
        log_update.info("Filter_Existed_IP: {0}".format(new_ip_info['ip']))


def del_ip(rm_ip):
    """删除ip"""
    ip_list = ip_json_load()
    for i in range(len(ip_list)):
        if rm_ip in ip_list[i].values():
            ip_list.pop(i)
            log_update.info("Delete invalid ip {0}".format(rm_ip))
            ip_json_dump(ip_list)
            return None


def verify_ip(ip_proxies, ip):
    """仅用于验证ip的有效性"""
    test_site = r"http://www.httpbin.org/ip"
    headers = settings.HEADERS
    try:
        res = requests.get(url=test_site, headers=headers, proxies=ip_proxies, timeout=5)
        res_ip = eval(res.text)['origin']
    except:
        logger.debug("Invalid_IP: {0}".format(ip_proxies))
        return False
    if res_ip == ip:
        logger.debug("Valid_IP: {0}".format(ip_proxies))
        return True
    else:
        logger.debug("Invalid_IP: {0}".format(ip_proxies))
        return False


def total_num():
    """获取有效ip池ip总数"""
    return len(ip_json_load())


def get_valid_ip():
    """获取单个,有效的ip"""
    while True:
        ip_list = ip_json_load()
        if len(ip_list)>0:
            range_end = len(ip_list) - 1
            ip_num = random.randint(0, range_end)
            ip_info = ip_list[ip_num]
            ip = ip_info['ip']
            ip_proxies = ip_info['proxies']
            if verify_ip(ip_proxies, ip):
                log_get.info("=========>Get ip proxies success: {0}".format(ip_proxies))
                return ip_proxies           # 返回代理proxies
            else:
                del_ip(ip)
                continue
        else:
            logger.warning("IP pool is empty")
            return None


def __verify_and_eliminate(ip_proxies, ip):
    """用于periodic_verify()函数调用，验证已存ip有效性同时剔除无效记录"""
    if not verify_ip(ip_proxies, ip):
        del_ip(rm_ip=ip)


def periodic_verify():
    """周期性验证已存ip的有效性，并发数为5"""
    while True:
        print("Start to verify IP at {0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        ip_list = ip_json_load()
        threads = []
        th_pool = Pool(settings.VERIFY_MAX_CONCURRENT)

        if len(ip_list) > 0:
            for i in range(len(ip_list)):
                ip_info = ip_list[i]
                ip = ip_info['ip']
                ip_proxies = ip_info['proxies']
                threads.append(th_pool.spawn(__verify_and_eliminate, ip_proxies, ip))
            gevent.joinall(threads)
        time.sleep(300)


if __name__ == '__main__':
    periodic_verify()