#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务查询点播语音结果接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY,BUSINESS_ID 为对应申请到的值
    2. $ python audio_query.py
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


class AudioQueryByTaskIdsDemo(object):
    """易盾图片离线查询结果获取接口示例代码"""

    API_URL = "http://as.dun.163.com/v1/audio/query/task"
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
        if "signatureMethod" in params.keys() and params["signatureMethod"] == "SM3":
            return sm3.sm3_hash(func.bytes_to_list(bytes(buff, encoding='utf8')))
        else:
            return hashlib.md5(buff.encode("utf8")).hexdigest()

    def query(self, params):
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
    api = AudioQueryByTaskIdsDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

    # 私有请求参数
    taskIds: list = ['202b1d65f5854cecadcb24382b681c1a', '0f0345933b05489c9b60635b0c8cc721']  # 查询参数taskIds
    params = {
        "taskIds": taskIds
    }

    ret = api.query(params)

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        antispamArray: list = ret["antispam"]
        if antispamArray is None or len(antispamArray) == 0:
            print("暂无审核回调数据")
        else:
            for result in antispamArray:
                status: int = result["status"]
                taskId: str = result["taskId"]
                if status == 30:
                    print("antispam callback taskId=%s，结果：数据不存在" % taskId)
                else:
                    action: int = result["action"]
                    labelArray: list = result["labels"]
                    if action == 0:
                        print("callback taskId=%s，结果：通过" % taskId)
                    elif action == 2:
                        for labelInfo in labelArray:
                            label: int = labelInfo["label"]
                            level: int = labelInfo["level"]
                            details: dict = labelInfo["details"]
                            hintArray: list = details["hint"]
                            subLabels: list = labelInfo["subLabels"]
                        print("callback=%s，结果：不通过，分类信息如下：%s" % (taskId, labelArray))
        languageArray: list = ret["language"]
        if languageArray is None or len(languageArray) == 0:
            print("暂无语种检测数据")
        else:
            for result in languageArray:
                status: int = result["status"]
                taskId: str = result["taskId"]
                if status == 30:
                    print("language callback taskId=%s，结果：数据不存在" % taskId)
                else:
                    detailsArray: list = result["details"]
                    if detailsArray is not None and len(detailsArray) > 0:
                        for language in detailsArray:
                            typeLan: str = language["type"]
                            segmentsArray: list = language["segments"]
                            if segmentsArray is not None and len(segmentsArray) > 0:
                                for segment in segmentsArray:
                                    print("taskId=%s，语种类型=%s，开始时间=%s秒，结束时间=%s秒" % (taskId, typeLan, segment["startTime"], segment["endTime"]))
        asrArray: list = ret["asr"]
        if asrArray is None or len(asrArray) == 0:
            print("暂无语音翻译数据")
        else:
            for result in asrArray:
                status: int = result["status"]
                taskId: str = result["taskId"]
                if status == 30:
                    print("asr callback taskId=%s，结果：数据不存在" % taskId)
                else:
                    detailsArray: list = result["details"]
                    if detailsArray is not None and len(detailsArray) > 0:
                        for asr in detailsArray:
                            startTime: int = asr["startTime"]
                            endTime: int = asr["endTime"]
                            content: str = asr["content"]
                            print("taskId=%s，文字翻译结果=%s，开始时间=%s秒，结束时间=%s秒" % (taskId, content, startTime, endTime))
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
