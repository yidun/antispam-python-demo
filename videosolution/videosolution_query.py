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
import urllib.request as urlrequest
import urllib.parse as urlparse
import json


class VideoSolutionQueryAPIDemo(object):
    """点播音视频解决方案结果查询接口示例代码"""

    API_URL = "http://as.dun.163.com/v1/videosolution/query/task"
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

    def check(self, params):
        """请求易盾接口
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
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
    api = VideoSolutionQueryAPIDemo(SECRET_ID, SECRET_KEY)

    taskIds: list = ['202b1d65f5854cecadcb24382b681c1a', '0f0345933b05489c9b60635b0c8cc721']  # 查询参数taskIds
    params = {
        "taskIds": taskIds
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
                taskId: str = resultItem["taskId"]
                status: int = resultItem["status"]
                if status == 0:
                    result: int = resultItem["result"]
                    print("点播音视频, taskId:%s, 检测结果:%s" % (taskId, result))
                    if resultItem["evidences"] is not None:
                        evidences: dict = resultItem["evidences"]
                        if evidences["texts"] is not None:
                            texts: list = evidences["texts"]
                            for textItem in texts:
                                print("文本信息, dataId:%s, 检测结果:%s", textItem["dataId"], textItem["action"])
                        elif evidences["images"] is not None:
                            images: list = evidences["images"]
                            for imageItem in images:
                                print("图片信息, dataId:%s, 检测状态:%s, 检测结果:%s", imageItem["dataId"], imageItem["status"],
                                      imageItem["action"])
                        elif evidences["audios"] is not None:
                            audios: list = evidences["audios"]
                            for audioItem in audios:
                                print("语音信息, dataId:%s, 检测状态:%s, 检测结果:%s", audioItem["dataId"], audioItem["asrStatus"],
                                      audioItem["action"])
                        elif evidences["videos"] is not None:
                            videos: list = evidences["videos"]
                            for videoItem in videos:
                                print("视频信息, dataId:%s, 检测状态:%s, 检测结果:%s", videoItem["dataId"], videoItem["status"],
                                      videoItem["level"])
                    elif resultItem["reviewEvidences"] is not None:
                        reviewEvidences: dict = resultItem["reviewEvidences"]
                        reason: str = reviewEvidences["reason"]
                        detail: dict = reviewEvidences["detail"]
                        text: list = reviewEvidences["text"]
                        image: list = reviewEvidences["image"]
                        audio: list = reviewEvidences["audio"]
                        video: list = reviewEvidences["video"]
                elif status == 20:
                    print("点播音视频, taskId:%s, 数据非7天内", taskId)
                elif status == 30:
                    print("点播音视频, taskId:%s, 数据不存在", taskId)
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
