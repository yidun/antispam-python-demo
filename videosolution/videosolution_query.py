#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务点播音视频解决方案结果查询接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY 为对应申请到的值
    2. $ python videosolution_query.py
"""
__author__ = 'yidun-dev'
__date__ = '2019/11/27'
__version__ = '0.2-dev'

import hashlib
import time
import random
import urllib3
from urllib.parse import urlencode
import json
from gmssl import sm3, func


class VideoSolutionQueryAPIDemo(object):
    """点播音视频解决方案结果查询接口示例代码"""

    API_URL = "http://as.dun.163.com/v2/videosolution/query/task"
    VERSION = "v2"

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
                timeout=urllib3.Timeout(connect=10, read=10)
            )
            content = response.data
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    api = VideoSolutionQueryAPIDemo(SECRET_ID, SECRET_KEY)

    taskIds: list = ['hvzrbqcl2zrr53inegdsh5tg02009x8w']  # 查询参数taskIds
    dataIds: list = ['dataId85480']  # 查询参数dataIds
    params = {
        "taskIds": taskIds,
        "dataIds": dataIds
    }

    ret = api.check(params)

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        resultArray: list = ret["result"]
        if len(resultArray) == 0:
            print("暂时没有结果需要获取, 请稍后重试!")
        else:
            for resultItem in resultArray:
                taskId: str = resultItem["taskId"] if "taskId" in resultItem else ''
                status: int = resultItem["status"]
                dataId = resultItem["dataId"] if "dataId" in resultItem else ''
                print("点播音视频 taskId:%s, dataId:%s, 数据状态%s" % (taskId, dataId, status))
                if status == 0:
                    if "antispam" in resultItem:
                        antispam: dict = resultItem["antispam"]
                        antispamTaskId: str = antispam["taskId"]
                        callback: str = antispam["callback"] if "callback" in antispam else ''
                        suggestion: int = antispam["suggestion"]
                        status: int = antispam["status"]
                        resultType: int = antispam["resultType"]
                        censorRound: int = antispam["censorRound"] if "censorRound" in antispam else 1
                        checkTime: int = antispam["checkTime"]
                        censorTime: int = antispam["censorTime"]
                        duration: int = antispam["duration"]
                        print("点播音视频反垃圾结果, taskId:%s, callback:%s, 检测状态:%s, 检测结果:%s" % (
                            antispamTaskId, callback, status, suggestion))
                        if "evidences" in antispam:
                            evidences: dict = antispam["evidences"]
                            if "text" in evidences:
                                textItem: dict = evidences["text"]
                                print("文本信息, dataId:%s, 检测结果:%s" % (textItem["dataId"], textItem["suggestion"]))
                            if "images" in evidences:
                                images: list = evidences["images"]
                                for imageItem in images:
                                    print("图片信息, taskId:%s, 检测状态:%s, 检测结果:%s" % (imageItem["taskId"],
                                          imageItem["status"], imageItem["suggestion"]))
                            if "audio" in evidences:
                                audioItem: dict = evidences["audio"]
                                print("语音信息, taskId:%s, 检测状态:%s, 检测结果:%s" % (audioItem["taskId"],
                                      audioItem["status"], audioItem["suggestion"]))
                            if "video" in evidences:
                                videoItem: dict = evidences["video"]
                                print("视频信息, taskId:%s, 检测状态:%s, 检测结果:%s" % (videoItem["taskId"],
                                      videoItem["status"], videoItem["suggestion"]))
                        elif "reviewEvidences" in antispam:
                            reviewEvidences: dict = antispam["reviewEvidences"]
                            description: str = reviewEvidences[
                                "description"] if "description" in reviewEvidences else ''
                            detail: str = reviewEvidences["detail"] if "detail" in reviewEvidences else ''
                            spamType: int = reviewEvidences["spamType"] if "spamType" in reviewEvidences else -1
                            texts: list = reviewEvidences["texts"] if "texts" in reviewEvidences else []
                            images: list = reviewEvidences["images"] if "images" in reviewEvidences else []
                            audios: list = reviewEvidences["audios"] if "audios" in reviewEvidences else []
                            videos: list = reviewEvidences["videos"] if "videos" in reviewEvidences else []
                            print("人审证据信息，备注%s, 垃圾类型%s, 文本证据%s, 图片证据%s, 音频证据%s, 视频证据%s" %
                                  (description, spamType, texts, images, audios, videos))
                    if "language" in resultItem:
                        language: dict = resultItem["language"]
                        languageDetails: list = language["details"] if "details" in language else []
                        print("语种检测结果详情:", languageDetails)
                    if "voice" in resultItem:
                        voice: dict = resultItem["voice"]
                        voiceDetails: list = voice["details"] if "details" in voice else []
                        print("人声属性检测结果详情:", voiceDetails)
                    if "asr" in resultItem:
                        asr: dict = resultItem["asr"]
                        asrDetails: list = asr["details"] if "details" in asr else []
                        print("语音识别检测结果详情:", asrDetails)
                elif status == 1:
                    print("点播音视频, taskId:%s, 数据非7天内" % taskId)
                elif status == 2:
                    print("点播音视频, taskId:%s, 数据不存在" % taskId)
                elif status == 3:
                    print("点播音视频, taskId:%s, 检测中" % taskId)
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
