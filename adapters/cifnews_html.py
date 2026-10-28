# -*- coding: utf-8 -*-
"""雨果网首页 HTML 抓文章标题（跨境电商资讯中转，覆盖 US/ID/SA 等海外信号）。

探针实测：https://www.cifnews.com/  200 / 212KB / 大陆可达。
真正的 /rss XML 已 405 被 WAF 拦；改抓首页 HTML 标题列表。
合规：仅取标题 + 原文链接，摘要不搬运；标注"经国内资讯源中转"。
"""
from __future__ import annotations

import re
from datetime import datetime
from hashlib import md5

import requests

from ._util import UA

NAME = "cifnews_html"
LABEL = "雨果网跨境资讯（中转）"
MARKET = "BRIDGE"
URL = "https://www.cifnews.com/"

# <a href="https://www.cifnews.com/article/123" ...>inner text</a>
_RE_PAIR = re.compile(
    r'<a[^>]+href="(https?://www\.cifnews\.com/article/\d+)"[^>]*>(.*?)</a>',
    re.S,
)


def fetch():
    from ._util import AdapterResult
    import time
    t0 = time.time()
    try:
        r = requests.get(URL, headers={"User-Agent": UA}, timeout=10)
    except Exception as e:  # noqa: BLE001
        return AdapterResult(ok=False, status_code="ERR",
                             latency_ms=int((time.time() - t0) * 1000),
                             error=f"{type(e).__name__}: {e}")
    lat = int((time.time() - t0) * 1000)
    if r.status_code != 200:
        return AdapterResult(ok=False, status_code=r.status_code, latency_ms=lat,
                             error=f"HTTP {r.status_code}")
    r.encoding = "utf-8"
    html = r.text
    pairs = _RE_PAIR.findall(html)
    seen: set[str] = set()
    items = []
    now = datetime.now().isoformat(timespec="seconds")
    for url, inner in pairs:
        text = re.sub(r"<[^>]+>", "", inner).strip()
        text = re.sub(r"\s+", " ", text)
        text = text.replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if len(text) < 8 or url in seen:
            continue
        seen.add(url)
        items.append({
            "id": "cif-" + md5((url).encode("utf-8")).hexdigest()[:12],
            "title": text,
            "title_zh": text,
            "summary_zh": "",
            "source_platform": "雨果网",
            "source_type": "news_bridge",
            "source_url": url,
            "source_publisher": "雨果网（经国内资讯源中转）",
            "market": "BRIDGE",
            "fetched_at": now,
            "rank_hint": len(items) + 1,
            "heat_hint": 0,
        })
        if len(items) >= 30:
            break
    if not items:
        return AdapterResult(ok=False, status_code=r.status_code, latency_ms=lat,
                             error="no article links parsed")
    return AdapterResult(ok=True, status_code=r.status_code, latency_ms=lat,
                         items=items, sample=items[0]["title"])
