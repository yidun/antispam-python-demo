## 网易易盾
http://dun.163.com
## 接口说明

- pyhton版本:3.7
- 文件说明

```
├── audio 语音接口演示
│   │── audio_callback.py 点播语音检测结果获取接口演示
│   │── audio_query.py 点播语音结果查询接口演示
│   │── audio_submit.py 点播语音检测提交接口演示
│   │── audio_check.py 点播语音在线检测接口演示
│   │── liveaudio_callback.py 直播语音检测结果获取接口演示
│   │── liveaudio_querymonitor.py 直播语音人审操作记录获取接口演示
│   │── liveaudio_querytask.py 直播语音结果获取接口演示
│   │── liveaudio_feedback.py 直播语音信息更新接口演示
│   │── liveaudio_queryextra.py 直播语音增值检测结果获取接口
│   └── liveaudio_check.py 直播语音在线检测提交接口演示
├── crawler 网站解决方案接口演示
│   │── crawler_callback.py 网站解决方案检测结果获取接口演示
│   │── crawler_submit.py 网站解决方案在线检测提交接口演示
│   └── crawler_job_submit.py 网站解决方案主站检测任务提交接口演示
├── filesolution 文档解决方案接口演示
│   │── filesolution_callback.py 文档解决方案检测结果获取接口演示
│   │── filesolution_query.py 文档解决方案结果查询接口演示
│   └── filesolution_submit.py 文档解决方案在线检测提交接口演示
├── image 图片接口演示
│   ├── image_callback.py 图片离线结果获取接口演示
│   ├── image_check.py 图片在线检测接口演示
│   ├── image_asynccheck.py 图片离线检测接口演示
│   ├── image_asyncresult.py 图片离线检测结果查询接口演示
│   ├── image_query.py 图片检测结果查询接口演示
│   ├── imagelist_delete.py 图片名单删除接口演示
│   ├── imagelist_query.py 图片名单查询接口演示
│   ├── imagelist_submit.py 图片名单添加接口演示
│   └── image_submit.py 图片批量提交接口演示
├── livevideosolution 直播音视频解决方案接口演示
│   │── livevideosolution_callback.py 直播音视频解决方案离线结果获取接口演示
│   │── livevideosolution_submit.py 直播音视频解决方案在线检测提交接口演示
│   │── livevideosolution_feedback.py 直播音视频解决方案信息更新接口演示
│   │── livevideosolution_queryaudio.py 直播音视频解决方案查询音频断句信息接口演示
│   │── livevideosolution_queryimage.py 直播音视频解决方案查询视频截图信息接口演示
│   └── livevideosolution_querymonitor.py 直播音视频解决方案人审操作记录获取接口演示
├── text 文本接口演示
│   │── text_callback.py 文本离线结果获取接口演示
│   │── text_check.py 文本在线检测接口演示
│   │── text_batch_check.py 文本批量在线检测接口演示
│   │── text_query.py 文本检测结果查询接口演示
│   └── text_submit.py 文本批量提交接口演示
├── video 视频接口演示
│   ├── livevideo_callback.py 直播流检测结果获取接口演示
│   ├── livevideo_query.py 直播视频结果查询接口演示
│   ├── liveimage_query.py 直播视频截图结果查询接口演示
│   ├── livevideo_submit.py 直播视频信息提交接口演示
│   ├── livevideo_feedback.py 直播视频信息更新接口演示
│   ├── livewall_callback.py 直播电视墙检测结果获取接口演示
│   ├── livewall_querymonitor.py 直播电视墙人审操作记录获取接口演示
│   ├── livewall_submit.py 直播电视墙信息提交接口演示
│   ├── video_callback.py 视频点播检测结果获取接口演示
│   ├── video_query.py 视频点播结果查询接口演示
│   ├── videoimage_query.py 视频点播截图结果查询接口演示
│   └── video_submit.py 视频点播信息提交接口演示
├── videosolution 点播音视频解决方案接口演示
│   │── videosolution_callback.py 点播音视频解决方案检测结果获取接口演示
│   │── videosolution_query.py 点播音视频解决方案结果查询接口演示
│   └── videosolution_submit.py 点播音视频解决方案在线检测提交接口演示
├── mediasolution 融媒体解决方案接口演示
│   │── mediasolution_callback.py 融媒体解决方案离线结果获取接口演示
│   │── mediasolution_submit.py 融媒体解决方案在线检测提交接口演示
│   └── mediasolution_query.py 融媒体解决方案结果查询接口演示
├── keyword 敏感词接口演示
│   │── keyword_submit.py 敏感词提交接口演示
│   │── keyword_delete.py 敏感词删除接口演示
│   └── keyword_query.py 敏感词查询接口演示
├── list 名单接口演示
│   │── list_submit.py 名单提交接口演示
│   │── list_delete.py 名单删除接口演示
│   │── list_query.py 名单查询接口演示
│   └── list_update.py 名单修改接口演示
├── digital 数字阅读解决方案接口演示
│   │── digital_callback.py 数字阅读解决方案结果获取接口演示
│   │── digital_submit.py 数字阅读解决方案检测提交接口演示
│   └── digital_query.py 数字阅读解决方案结果查询接口演示
├── report 投诉举报解决方案接口演示
│   │── report_callback.py 投诉举报解决方案结果获取接口演示
│   │── report_submit.py 投诉举报解决方案检测提交接口演示
│   └── report_query.py 投诉举报解决方案结果查询接口演示
└── README.md

```

## 使用说明
- demo仅做接口演示使用，生产环境接入请根据实际情况增加异常处理逻辑。
