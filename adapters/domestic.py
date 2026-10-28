# -*- coding: utf-8 -*-
"""国内源（微博/知乎/抖音聚合）——海外 CI 默认关闭。

原因：weibo.com/ajax/side/hotSearch 海外 403；知乎 hot-lists 401；
第三方抖音聚合 iamwawa 404。代码保留，本地国内网络运行时把
ENABLE_DOMESTIC=1 即可启用。
"""
import os, time
from .base import http_get


def fetch(cfg):
    t0 = time.time()
    enabled = os.environ.get("ENABLE_DOMESTIC", "") == "1"
    if not enabled:
        return [], {"ok": True, "count": 0,
                    "elapsed_ms": int((time.time() - t0) * 1000),
                    "error": None, "last_ok": None,
                    "note": "国内源（微博/知乎/抖音聚合）默认关闭，海外 IP 403/401/404；本地运行设 ENABLE_DOMESTIC=1"}
    items = []
    # 微博
    try:
        r = http_get("https://weibo.com/ajax/side/hotSearch")
        for w in r.json().get("data", {}).get("realtime", [])[:15]:
            items.append({**w, "_src": "weibo"})
    except Exception as e:  # noqa
        return items, {"ok": False, "count": len(items),
                       "elapsed_ms": int((time.time() - t0) * 1000),
                       "error": "微博失败：%s" % e, "last_ok": None,
                       "note": "国内源"}
    return items, {"ok": True, "count": len(items),
                   "elapsed_ms": int((time.time() - t0) * 1000),
                   "error": None, "last_ok": None, "note": "国内源"}
