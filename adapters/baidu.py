# -*- coding: utf-8 -*-
"""百度热搜实时榜（CN 市场）。

公开接口：https://top.baidu.com/api/board?platform=pc&tab=realtime
字段：data.cards[0].content[]  -> word / rawUrl / desc / hotScore / hotTag / index
"""
from __future__ import annotations

import json
import time
from datetime import datetime
from hashlib import md5

from ._util import http_get, AdapterResult

NAME = "baidu_realtime"
LABEL = "百度热搜实时榜"
MARKET = "CN"
URL = "https://top.baidu.com/api/board?platform=pc&tab=realtime"


def fetch() -> AdapterResult:
    status, lat, body, err = http_get(URL, timeout=8)
    if err:
        return AdapterResult(ok=False, status_code=status, latency_ms=lat, error=err)
    if status != 200:
        return AdapterResult(ok=False, status_code=status, latency_ms=lat,
                             error=f"HTTP {status}")
    try:
        j = json.loads(body.decode("utf-8", errors="replace"))
    except Exception as e:  # noqa: BLE001
        return AdapterResult(ok=False, status_code=status, latency_ms=lat,
                             error=f"JSON decode: {e}")
    cards = (j.get("data") or {}).get("cards") or []
    if not cards:
        return AdapterResult(ok=False, status_code=status, latency_ms=lat,
                             error="no cards in response")
    content = cards[0].get("content") or []
    items = []
    now = datetime.now().isoformat(timespec="seconds")
    for i, c in enumerate(content[:50]):
        word = (c.get("word") or "").strip()
        if not word:
            continue
        url = c.get("rawUrl") or c.get("appUrl") or c.get("url") or \
            f"https://www.baidu.com/s?wd={word}"
        hot_score = c.get("hotScore") or 0
        try:
            hot_score = int(hot_score)
        except Exception:
            hot_score = 0
        items.append({
            "id": "bd-" + md5(word.encode("utf-8")).hexdigest()[:12],
            "title": word,
            "title_zh": word,
            "summary_zh": (c.get("desc") or "")[:240],
            "source_platform": "百度热搜",
            "source_type": "hotsearch",
            "source_url": url,
            "source_publisher": "百度",
            "market": "CN",
            "fetched_at": now,
            "rank_hint": i + 1,
            "heat_hint": hot_score,
            "hot_tag": c.get("hotTag") or "",
        })
    return AdapterResult(ok=True, status_code=status, latency_ms=lat,
                         items=items, sample=items[0]["title"] if items else "")
