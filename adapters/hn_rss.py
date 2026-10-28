# -*- coding: utf-8 -*-
"""Hacker News 首页 RSS（US/英文/科技 3C 信号）。

公开 RSS：https://hnrss.org/frontpage
无 key，大陆可达（探针实测 200）。
"""
from __future__ import annotations

from datetime import datetime
from hashlib import md5

import feedparser

from ._util import http_get, AdapterResult, UA

NAME = "hn_rss"
LABEL = "Hacker News (US/tech)"
MARKET = "US"
URL = "https://hnrss.org/frontpage"


def fetch() -> AdapterResult:
    status, lat, body, err = http_get(URL, timeout=10)
    if err:
        return AdapterResult(ok=False, status_code=status, latency_ms=lat, error=err)
    if status != 200:
        return AdapterResult(ok=False, status_code=status, latency_ms=lat,
                             error=f"HTTP {status}")
    feed = feedparser.parse(body, response_headers={"Content-Type": "application/xml; charset=utf-8"})
    entries = feed.entries or []
    items = []
    now = datetime.now().isoformat(timespec="seconds")
    for i, e in enumerate(entries[:30]):
        title = (getattr(e, "title", "") or "").strip()
        if not title:
            continue
        link = getattr(e, "link", "") or ""
        # hnrss 自带 comments 链接；优先原文 link
        items.append({
            "id": "hn-" + md5((title + link).encode("utf-8")).hexdigest()[:12],
            "title": title,
            "title_zh": title,  # 英文原标题保留；summary_zh 留空
            "summary_zh": "",
            "source_platform": "Hacker News",
            "source_type": "news_rss",
            "source_url": link,
            "source_publisher": getattr(getattr(feed, "feed", {}), "title", "Hacker News"),
            "market": "US",
            "fetched_at": now,
            "rank_hint": i + 1,
            "heat_hint": 0,
        })
    return AdapterResult(ok=True, status_code=status, latency_ms=lat,
                         items=items, sample=items[0]["title"] if items else "")
