# -*- coding: utf-8 -*-
"""百度热搜 PC 版（国内市场信号，免 Key）。

URL: https://top.baidu.com/api/board?platform=pc&tab=realtime
JSON: data.cards[0].content[].word
"""
import time, json
from .base import http_get, normalize, today_str


def fetch(cfg):
    t0 = time.time()
    items = []
    try:
        r = http_get("https://top.baidu.com/api/board?platform=pc&tab=realtime")
        data = r.json()
        contents = data.get("data", {}).get("cards", [{}])[0].get("content", [])
        for c in contents[:30]:
            word = c.get("word") or c.get("query") or ""
            if not word:
                continue
            url = c.get("url") or ("https://www.baidu.com/s?wd=" + word)
            items.append(normalize(
                platform="百度热搜", url=url, title=word,
                source_publisher="百度", published=today_str(),
                market="CN", category=_guess_category(word),
                summary=(c.get("desc") or "")[:200],
                raw_signals={"hot_score_baidu": c.get("hotScore"), "source": "baidu_board"},
                evidence_tier=1,
            ))
    except Exception as e:  # noqa
        return items, {"ok": False, "count": len(items),
                       "elapsed_ms": int((time.time() - t0) * 1000),
                       "error": str(e), "last_ok": None,
                       "note": "百度热搜 PC 版"}
    return items, {"ok": True, "count": len(items),
                   "elapsed_ms": int((time.time() - t0) * 1000),
                   "error": None, "last_ok": _now(), "note": "百度热搜 PC 版"}


def _now():
    import datetime
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def _guess_category(word):
    w = word
    for kw, cat in [("美妆", "beauty"), ("护肤", "beauty"), ("化妆品", "beauty"),
                    ("家居", "home"), ("家电", "home"), ("手机", "3c"), ("耳机", "3c"),
                    ("充电", "3c"), ("户外", "outdoor"), ("露营", "outdoor")]:
        if kw in w:
            return cat
    return "other"
