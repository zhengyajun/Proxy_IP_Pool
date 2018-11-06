"""定义获取ip的数据格式"""

class IpDataFormat(object):
    '''抓取的ip储存对象'''
    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        self.__dict__.pop(key)

    ip_ = None
    port = None
    type = None         # http/ https/ sockets
    # city = None        # ip归属地
    # status = None     # 周期时间内，0为过期待验证，1为已验证