#!flask/bin/python
"""
Purpose: 提供有效的ip获取RESTful API接口
API-Example(127.0.0.1:5000):
    获取单个有效ip(有验证): 127.0.0.1:5000/ip_pool/api/v1.0/get_ip
    查看文件中所有ip(无验证): 127.0.0.1:5000/ip_pool/api/v1.0/get_ip_pool
    查看文件中指定ip(无验证): 127.0.0.1:5000/ip_pool/api/v1.0/get_a_ip/0
Author: YajunZheng
Created: 2018/10/29
"""

import json
from os.path import dirname, abspath

from flask import Flask, jsonify
from flask import abort

from pool import settings
from pool.core.tool_lib import get_valid_ip

app = Flask(__name__)
abs_path = dirname(abspath(__file__))
data_path = abs_path + "/data/" + settings.DATA_FILE_NAME


def load_json_file(data_path):
    """读取json文件"""
    with open(data_path, 'r') as fp:
        res = json.load(fp)
        fp.close()
    return res


@app.route('/ip_pool/api/v1.0/get_ip', methods=['GET'])
def get_ip():
    """获取单个ip，验证有效后返回该ip"""
    ip = get_valid_ip()
    if ip:
        return jsonify(ip)
    else:
        abort(404)


@app.route('/ip_pool/api/v1.0/get_ip_pool', methods=['GET'])
def get_all_ip():
    """获取整个ip池，不进行验证，返回json文件内容"""
    ip_pool = load_json_file(data_path=data_path)
    return jsonify({'get_ip_pool': ip_pool})


@app.route('/ip_pool/api/v1.0/get_ip/<int:ip_id>', methods=['GET'])
def get_a_ip(ip_id):
    """从json文件中获取指定ip,不进行验证，直接返回结果"""
    ip_pool = load_json_file(data_path=data_path)
    if ip_id > len(ip_pool):
        abort(404)
    else:
        return jsonify(ip_pool[ip_id])


if __name__ == '__main__':
    app.run(debug=True)
