#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务直播音视频解决方案查询音频断句信息接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY 为对应申请到的值
    2. $ python livevideosolution_queryaudio.py
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


class LiveVideoSolutionQueryAudioAPIDemo(object):
    """直播音视频解决方案人审查询音频断句信息接口示例代码"""

    API_URL = "http://as.dun.163yun.com/v1/livewallsolution/query/audio/task"
    VERSION = "v1.0"

    def __init__(self, secret_id, secret_key):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
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
    api = LiveVideoSolutionQueryAudioAPIDemo(SECRET_ID, SECRET_KEY)

    # 私有请求参数
    params = {
        "taskId": "xxxx",
        "startTime": "1578326400000",
        "endTime": "1578327000000"
    }
    ret = api.check(params)

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        resultArray: list = ret["result"]
        if len(resultArray) == 0:
            print("没有结果")
        else:
            for result in resultArray:
                taskId: str = result["taskId"]
                action: int = result["action"]
                startTime: int = result["startTime"]
                endTime: int = result["endTime"]
                segment_array: list = result["segments"]
                if action == 0:
                    print("taskId=%s，结果：通过，时间区间【%s-%s】，证据信息如下：%s" % (taskId, startTime, endTime, segment_array))
                elif action == 1 or action == 2:
                    for segment_item in segment_array:
                        label: int = segment_item["label"]
                        level: int = segment_item["level"]
                    print("taskId=%s，结果：%s，时间区间【%s-%s】，证据信息如下：%s" % (taskId, "不确定" if action == 1 else "不通过",
                                                                     startTime, endTime, segment_array))
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
