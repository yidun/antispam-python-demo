#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务直播音视频信息更新接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY 为对应申请到的值
    2. $ python livevideo_feedback.py
"""
__author__ = 'yidun-dev'
__date__ = '2020/10/29'
__version__ = '0.2-dev'

import hashlib
import time
import random
import urllib3
from urllib.parse import urlencode
import json
from gmssl import sm3, func


class LiveVideoFeedbackAPIDemo(object):
    """直播音视频解决方案信息更新接口示例代码"""

    API_URL = "http://as.dun.163.com/v1/livevideo/feedback"
    VERSION = "v1.0"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id
        self.http = urllib3.PoolManager()  # 初始化连接池

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
        if "signatureMethod" in params.keys() and params["signatureMethod"] == "SM3":
            return sm3.sm3_hash(func.bytes_to_list(bytes(buff, encoding='utf8')))
        else:
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
        # params["signatureMethod"] = "SM3"  # 签名方法，默认MD5，支持SM3
        params["signature"] = self.gen_signature(params)

        try:
            encoded_params = urlencode(params).encode("utf8")
            response = self.http.request(
                'POST',
                self.API_URL,
                body=encoded_params,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                timeout=urllib3.Timeout(connect=1.0, read=1.0)
            )
            content = response.data
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = LiveVideoFeedbackAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    # 私有请求参数
    realTimeInfos: list = []
    realTimeInfo = {
        "taskId": "****",
        "status": "100"
    }
    realTimeInfos.append(realTimeInfo)
    params = {
        "realTimeInfoList": json.dumps(realTimeInfos)
    }
    ret = api.check(params)

    code: int = ret["code"]
    msg: str = ret["msg"]
    resultArray: list = ret["result"]
    if code == 200:
        for result in resultArray:
            taskId: str = result["taskId"]
            r: int = result["result"]
            if r == 0:
                print("SUCCESS, taskId=%s" % taskId)
            elif r == 2:
                print("NOT EXISTS, taskId=%s" % taskId)
            elif r == 1:
                print("SERVER ERROR, taskId=%s" % taskId)

    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
