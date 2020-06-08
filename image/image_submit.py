#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务图片批量提交接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python image_submit.py
"""
__author__ = 'yidun-dev'
__date__ = '2019/11/27'
__version__ = '0.2-dev'

import hashlib
import time
import random
import urllib.request as urlrequest
import urllib.parse as urlparse
import json


class ImageSubmitAPIDemo(object):
    """图片批量提交接口"""

    API_URL = "http://as.dun.163.com/v1/image/submit"
    VERSION = "v1"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        return hashlib.md5(buff.encode("utf8")).hexdigest()

    def check(self, params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        params["signature"] = self.gen_signature(params)

        try:
            params = urlparse.urlencode(params).encode("utf8")
            request = urlrequest.Request(self.API_URL, params)
            content = urlrequest.urlopen(request, timeout=10).read()
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = ImageSubmitAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    # 私有请求参数
    images: list = []
    # dataId结构产品自行设计，用于唯一定位该图片数据
    image1 = {
        "name": "image1",
        "data": "https://nos.netease.com/yidun/2-0-0-a6133509763d4d6eac881a58f1791976.jpg",
        "level": "2"
        # "ip": "123.115.77.137"
        # "account": "python@163.com"
        # "deviceId": "deviceId"
        # "callbackUrl": "http://***"  # 主动回调地址url,如果设置了则走主动回调逻辑
    }
    image2 = {
        "name": "image2",
        "data": "http://dun.163.com/public/res/web/case/sexy_normal_2.jpg?dda0e793c500818028fc14f20f6b492a",
        "level": "0"
        # "ip": "123.115.77.137"
        # "account": "python@163.com"
        # "deviceId": "deviceId"
        # "callbackUrl": "http://***"  # 主动回调地址url,如果设置了则走主动回调逻辑
    }
    images.append(image1)
    images.append(image2)
    params = {
        "images": json.dumps(images)
    }

    ret = api.check(params)

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        resultArray: list = ret["result"]
        for result in resultArray:
            name: str = result["name"]
            taskId: str = result["taskId"]
            print("图片提交返回, name: %s, taskId: %s" % (name, taskId))

    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
