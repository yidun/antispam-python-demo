#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务直播电视墙离线结果获取接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python livewall_callback.py
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
from gmssl import sm3, func


class LiveWallCallbackAPIDemo(object):
    """直播电视墙离线结果获取接口示例代码"""

    API_URL = "http://as.dun.163.com/v2/livewall/callback/results"
    VERSION = "v2"

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
        if "signatureMethod" in params.keys() and params["signatureMethod"] == "SM3":
            return sm3.sm3_hash(func.bytes_to_list(bytes(buff, encoding='utf8')))
        else:
            return hashlib.md5(buff.encode("utf8")).hexdigest()

    def check(self):
        """请求易盾接口
        Returns:
            请求结果，json格式
        """
        params = {}
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        # params["signatureMethod"] = "SM3"  # 签名方法，默认MD5，支持SM3
        params["signature"] = self.gen_signature(params)

        try:
            params = urlparse.urlencode(params).encode("utf8")
            request = urlrequest.Request(self.API_URL, params)
            content = urlrequest.urlopen(request, timeout=10).read()
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))

    def parse_machine(self, evidences, taskId):
        """机审信息"""
        print("=== 机审信息 ===")
        evidence: dict = evidences["evidence"]
        labels: list = evidences["labels"]
        types: int = evidence["type"]
        url: str = evidence["url"]
        begin_time: int = evidence["beginTime"]
        end_time: int = evidence["endTime"]

        for label_item in labels:
            label: int = label_item["label"]
            level: int = label_item["level"]
            rate: float = label_item["rate"]
            subLabels: list = label_item["subLabels"]
        print("Machine Evidence: %s" % evidence)
        print("Machine Labels: %s" % labels)
        print("================")

    def parse_human(self, review_evidences, taskId):
        """人审信息"""
        print("=== 人审信息 ===")
        action: int = review_evidences["action"]
        action_time: int = review_evidences["actionTime"]
        label: int = review_evidences["label"]
        detail: str = review_evidences["detail"]
        warn_count: int = review_evidences["warnCount"]
        evidence: list = review_evidences["evidence"]

        if action == 2:
            print("警告, taskId:%s, 警告次数:%s, 证据信息:%s" % (taskId, warn_count, evidence))
        elif action == 3:
            print("断流, taskId:%s, 警告次数:%s, 证据信息:%s" % (taskId, warn_count, evidence))
        else:
            print("人审信息：%s" % review_evidences)
        print("================")


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密list钥，服务端生成签名信息使用，请严格保管，避免泄露
    BUSINESS_ID = "your_business_id"  # 业务ID，易盾根据产品业务特点分配
    api = LiveWallCallbackAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    ret = api.check()

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        resultArray: list = ret["result"]
        if resultArray is None or len(resultArray) == 0:
            print("暂时没有结果需要获取，请稍后重试!")
        else:
            for result in resultArray:
                taskId: str = result["taskId"]
                dataId: str = result["dataId"]
                callback: str = result["callback"]
                status: int = result["status"]
                print("taskId:%s, dataId:%s, callback:%s, status:%s" % (taskId, dataId, callback, status))

                evidences: dict = result["evidences"]
                reviewEvidences: dict = result["reviewEvidences"]
                if evidences is not None:
                    api.parse_machine(evidences, taskId)
                elif reviewEvidences is not None:
                    api.parse_human(reviewEvidences, taskId)
                else:
                    print("Invalid Result: %s" % result)
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
