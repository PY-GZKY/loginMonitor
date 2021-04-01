# loginMonitor
![loginMonitor](https://img.shields.io/badge/Python-3.7-green)
![loginMonitor](https://img.shields.io/badge/Celery-5.0.5-blue)
![loginMonitor](https://img.shields.io/badge/Redis-3.5.3-red)
![loginMonitor](https://img.shields.io/badge/pyppeteer-0.2.2-yellow)


`Pyppeteer` 自动保持登陆状态。

> 适用于一般平台的自动化登陆流程(目前以某东为例)

## 实现

使用 Celery 分布式任务队列，监听启动爬虫时的登陆状态, 如果登陆状态为 `False` 则执行自动登陆脚本,一个平台可以由有个店铺组成,传入店铺ID即可登陆对应店铺获取对应`Cookie`。

自动化登陆脚本可以在启动项目 `cookie` 失效时唤醒，也可以在 `web` 端唤醒, 得到的平台 `cookie` 以hash形式写入 `redis` 队列并命名为该店铺ID,方便调用。


> 365 天都让你的爬虫项目保持活跃的登陆状态，一直到现在。

## Celery

以下面的示例启动 `Celery` 来监听爬虫服务

```shell
celery -A tasks beat -l INFO
celery -A tasks worker -l INFO -c 2
```

## 使用

- 拉取本仓库到本地，应用于你想触发的场景
- 欢迎 `fork` 让它更强大


