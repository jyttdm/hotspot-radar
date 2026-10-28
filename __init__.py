"""adapters：各数据源采集适配器。

真实接入一律走官方 API / 授权渠道；本骨架中的平台适配器多为 stub，
关键调用处抛 NotImplementedError 或返回 DEMO 样例，并在 docstring 写明申请入口。
"""
from .base import BaseAdapter, FetchResult  # noqa: F401
