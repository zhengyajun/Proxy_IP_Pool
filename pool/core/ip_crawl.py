#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Purpose: 从公开网站抓取高匿ip代理，创建ip池，每10分钟检测可用性进行更新一次，提供api接口，每次获取一个ip地址，并在取用之前进行检测
Author: YajunZheng
Created: 2018/10/25
"""

import sys
sys.path.append(r"./..")

import datetime
import requests
from lxml import etree

from pool.items import IpDataFormat
from pool import settings
from pool.core import tool_lib


class XicidailiCrawl(object):
    """西刺代理"""
    def __init__(self):
        self.init_url = "http://www.xicidaili.com/nn/{0}"
        self.s = requests.session()
        self.s.keep_alive = False
        self.proxies = tool_lib.get_valid_ip()

    def start_requests(self):
        """获取第一页中包含的ip列表"""
        for i in range(1, 2):
            url = self.init_url.format(str(i))
            headers = settings.HEADERS
            res = self.s.get(url=url, headers=headers, proxies=self.proxies, timeout=60)
            selector_1 = etree.HTML(res.text)
            ip_table = selector_1.xpath('//*[@id="ip_list"]//tr')
            print("Xicidaili: {0} ALL:{1} TIME:{2}".format(url, len(ip_table), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            yield ip_table

    def parse_ip_info(self, each_tr):
        """解析ip列表中的每一条ip信息，验证添加至储存文件"""
        ip_info = IpDataFormat()
        try:
            ip = each_tr.xpath('./td[2]/text()')[0]
            port = each_tr.xpath('./td[3]/text()')[0]
            ip_type = each_tr.xpath('./td[6]/text()')[0].casefold()
            ip_info['ip'] = str(ip)
            ip_info['port'] = str(port)
            ip_info['type'] = str(ip_type)
            # print(ip_info.__dict__.values())

            ip_proxies_str = "{'%s':'%s:%s'}" % (ip_info['type'], ip_info['ip'], ip_info['port'])
            ip_proxies = eval(ip_proxies_str)                                 # 字符串转列表
            if tool_lib.verify_ip(ip_proxies=ip_proxies, ip=ip):             # 验证ip的有效性
                valid_ip_info = dict(ip=ip, proxies=ip_proxies)
                tool_lib.add_ip(new_ip_info=valid_ip_info)                 # 添加ip
        except:
            pass


class KuaidailiCrawl:
    """快代理"""
    def __init__(self):
        self.init_url = "https://www.kuaidaili.com/ops/proxylist/{0}/"
        self.s = requests.Session()
        self.s.keep_alive = False
        self.proxies = tool_lib.get_valid_ip()

    def start_requests(self):
        """获取规定页数中包含的ip列表，以列表未单位构造生成器"""
        for i in range(11):
            url = self.init_url.format(str(i))
            headers = settings.HEADERS
            res = self.s.get(url=url, headers=headers, proxies=self.proxies, timeout=60)
            selector = etree.HTML(res.text)
            ip_table = selector.xpath('//*[@id="freelist"]/table/tbody/tr')
            print("Kuaidaili: {0} ALL:{1} TIME:{2}".format(url, len(ip_table), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            yield ip_table

    def parse_ip_info(self, each_tr):
        """解析单条ip的信息，验证添加至储存文件"""
        ip_info = IpDataFormat()
        try:
            flag = each_tr.xpath('./td[3]/text()')[0]
            if flag == "高匿名":
                ip = each_tr.xpath('./td[1]/text()')[0]
                port = each_tr.xpath('./td[2]/text()')[0]
                ip_type_list = each_tr.xpath('./td[4]/text()')[0].split(',')
                if len(ip_type_list) == 1:
                    ip_type = ip_type_list[0].strip().lower()
                else:
                    ip_type = ip_type_list[1].strip().lower()
                ip_info['ip'] = str(ip)
                ip_info['port'] = str(port)
                ip_info['type'] = str(ip_type)
                ip_proxies_str = "{'%(ip_type)s':'%(ip)s:%(port)s'}" % {'ip_type': ip_info['type'], 'ip': ip_info['ip'], 'port': ip_info['port']}
                ip_proxies = eval(ip_proxies_str)
                if tool_lib.verify_ip(ip_proxies=ip_proxies, ip=ip):
                    ip_info_dict = dict(ip=ip, proxies=ip_proxies)
                    tool_lib.add_ip(ip_info_dict)
        except:
            pass


# if __name__ == '__main__':                  # 测试代码
#     import time
#     kuai = KuaidailiCrawl()
#     for each_table in kuai.start_requests():
#         threads = []
#         for each_tr in each_table:
#             kuai.parse_ip_info(each_tr)
#         time.sleep(10)
