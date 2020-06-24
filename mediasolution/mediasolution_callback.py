#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务融媒体解决方案结果获取接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY 为对应申请到的值
    2. $ python mediasolution_callback.py
"""
__author__ = 'yidun-dev'
__date__ = '2020/06/24'
__version__ = '0.2-dev'

import hashlib
import time
import random
import urllib.request as urlrequest
import urllib.parse as urlparse
import json


class MediaSolutionCallbackAPIDemo(object):
    """融媒体解决方案结果获取接口"""

    API_URL = "http://as.dun.163.com/v1/mediasolution/callback/results"
    VERSION = "v1"

    def __init__(self, secret_id, secret_key):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
        """
        self.secret_id = secret_id
        self.secret_key = secret_key

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

    def check(self):
        """请求易盾接口
        Returns:
            请求结果，json格式
        """
        params = {}
        params["secretId"] = self.secret_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random()*100000000)
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
    api = MediaSolutionCallbackAPIDemo(SECRET_ID, SECRET_KEY)
    
    ret = api.check()

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        resultArray: list = ret["result"]
        if resultArray is None or len(resultArray) == 0:
            print("暂时没有结果需要获取，请稍后重试！")
        else:
            for resultItem in resultArray:
                dataId: str = resultItem["dataId"]
                taskId: str = resultItem["taskId"]
                callback: str = resultItem["callback"] if resultItem["callback"] is None else ""
                checkStatus: int = resultItem["checkStatus"]
                result: int = resultItem["result"]
                if resultItem["evidences"] is not None:
                    evidences: dict = resultItem["evidences"]
                    if evidences["texts"] is not None:
                        texts: list = evidences["texts"]
                        for text in texts:
                            print("文本信息, dataId:%s, 检测结果:%s", text["dataId"], text["action"])
                    elif evidences["images"] is not None:
                        images: list = evidences["images"]
                        for image in images:
                            print("图片信息, dataId:%s, 检测状态:%s, 检测结果:%s", image["dataId"], image["status"],
                                  image["action"])
                    elif evidences["audios"] is not None:
                        audios: list = evidences["audios"]
                        for audio in audios:
                            print("语音信息, dataId:%s, 检测状态:%s, 检测结果:%s", audio["dataId"], audio["asrStatus"],
                                  audio["action"])
                    elif evidences["videos"] is not None:
                        videos: list = evidences["videos"]
                        for video in videos:
                            print("视频信息, dataId:%s, 检测状态:%s, 检测结果:%s", video["dataId"], video["status"],
                                  video["level"])
                    elif evidences["audiovideos"] is not None:
                        audiovideos: list = evidences["audiovideos"]
                        for audiovideo in audiovideos:
                            print("音视频信息, dataId:%s, 检测结果:%s", audiovideo["dataId"], audiovideo["result"])
                    elif evidences["files"] is not None:
                        files: list = evidences["files"]
                        for file in files:
                            print("文档信息, dataId:%s, 检测结果:%s", file["dataId"], file["result"])
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
