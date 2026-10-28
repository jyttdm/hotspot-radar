# -*- coding: utf-8 -*-
"""HTTP 工具与标准化条目结构。

合规：仅用官方 RSS / 公开 API，不绕风控、不模拟登录、不破解签名。
所有请求带 UA、超时、简单退避；只抓摘要/标题并回链原文，不全文转载。
"""
import time, hashlib, datetime, json, urllib.parse

import requests

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
TIMEOUT = 10


def http_get(url, params=None, headers=None, retries=2):
    h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
    if headers:
        h.update(headers)
    last = None
    for i in range(retries + 1):
        try:
            r = requests.get(url, params=params, headers=h, timeout=TIMEOUT)
            if r.status_code == 200:
                return r
            last = "HTTP %s" % r.status_code
        except Exception as e:  # noqa
            last = str(e)
        time.sleep(1.5 * (i + 1))
    raise RuntimeError(last or "request failed")


def stable_id(platform, url, title):
    raw = (platform + "|" + url + "|" + title).encode("utf-8")
    return "rt-" + hashlib.md5(raw).hexdigest()[:10]


def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def today_str():
    return datetime.date.today().isoformat()


def normalize(*, platform, url, title, source_publisher, published, market, category,
              summary="", raw_signals=None, evidence_tier=2):
    """产出与现有 schema 对齐的最小条目（评分在 scoring.py 里补全）。"""
    return {
        "id": stable_id(platform, url, title),
        "title": title,
        "title_zh": title,
        "market": market,
        "category": category,
        "source_platform": platform,
        "source_type": "rss" if "news" in platform or "youtube" in platform else "board",
        "source_url": url,
        "source_title": title,
        "source_publisher": source_publisher,
        "evidence_tier": evidence_tier,  # 1=官方/榜单, 2=聚合/新闻
        "fetched_at": now_iso(),
        "is_real": True,
        "summary_zh": summary,
        "published": published,
        "raw_signals": raw_signals or {},
        "is_live": True,  # 实时抓取条目，区别于手工快照
    }
