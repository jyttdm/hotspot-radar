# -*- coding: utf-8 -*-
"""B站热门视频（CN 市场，年轻向 3C/美妆/生活/游戏）。

公开接口：https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1
字段：data.list[] -> title / short_link_v2 / tname / owner.name / stat.view / pubdate
"""
from __future__ import annotations

import json
from datetime import datetime
from hashlib import md5

from ._util import http_get, AdapterResult

NAME = "bilibili_popular"
LABEL = "B站热门视频"
MARKET = "CN"
URL = "https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1"


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
    if j.get("code") != 0:
        return AdapterResult(ok=False, status_code=status, latency_ms=lat,
                             error=f"bili code={j.get('code')} {j.get('message')}")
    lst = (j.get("data") or {}).get("list") or []
    items = []
    now = datetime.now().isoformat(timespec="seconds")
    for i, v in enumerate(lst[:20]):
        title = (v.get("title") or "").strip()
        if not title:
            continue
        owner = (v.get("owner") or {}).get("name", "")
        stat = v.get("stat") or {}
        items.append({
            "id": "bl-" + md5((title + owner).encode("utf-8")).hexdigest()[:12],
            "title": title,
            "title_zh": title,
            "summary_zh": (v.get("desc") or "")[:240],
            "source_platform": "B站热门",
            "source_type": "video",
            "source_url": v.get("short_link_v2") or f"https://www.bilibili.com/video/{v.get('bvid','')}",
            "source_publisher": owner,
            "market": "CN",
            "fetched_at": now,
            "rank_hint": i + 1,
            "heat_hint": int(stat.get("view") or 0),
            "tname": v.get("tname") or "",
        })
    return AdapterResult(ok=True, status_code=status, latency_ms=lat,
                         items=items, sample=items[0]["title"] if items else "")
