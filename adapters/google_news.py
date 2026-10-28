# -*- coding: utf-8 -*-
"""Google News RSS 适配器（核心管线，四语种全通，免 Key）。

URL: https://news.google.com/rss/search?q={关键词}&hl=..&gl=..&ceid=..
按 品类×市场语言 关键词矩阵抓取，feedparser 解析。
"""
import time, os, datetime
import feedparser

from .base import http_get, normalize

# 市场语言参数（已在海外 CI 实测）
MARKET_LOCALE = {
    "US": {"hl": "en-US", "gl": "US", "ceid": "US:en", "label": "美国"},
    "ID": {"hl": "id-ID", "gl": "ID", "ceid": "ID:id", "label": "印尼"},
    "VN": {"hl": "vi-VN", "gl": "VN", "ceid": "VN:vi", "label": "越南"},
    "SA": {"hl": "ar", "gl": "SA", "ceid": "SA:ar", "label": "中东"},
}

# 品类关键词矩阵（英文为主，Google News 英文召回最稳）
CATEGORY_QUERIES = {
    "beauty": ["beauty ecommerce", "skincare trending", "makeup best seller"],
    "home": ["home decor trend", "home gadgets viral", "kitchen amazon best"],
    "3c": ["tech gadget launch", "phone accessory trending", "amazon gadget deal"],
    "outdoor": ["outdoor gear trend", "camping gadget viral", "portable charger deal"],
}

# 营销节点词（按季节叠加）
CAMPAIGN_TERMS = ["black friday", "cyber monday", "11.11 sale", "white friday"]


def _parse_time(entry):
    tt = entry.get("published_parsed") or entry.get("updated_parsed")
    if tt:
        return datetime.datetime(*tt[:6]).isoformat()
    return ""


def fetch(cfg):
    t0 = time.time()
    items = []
    seen = set()
    markets = cfg.get("markets", ["US", "ID", "VN", "SA"])
    cats = cfg.get("categories", ["beauty", "home", "3c", "outdoor"])

    for mkt in markets:
        loc = MARKET_LOCALE.get(mkt)
        if not loc:
            continue
        for cat in cats:
            qs = CATEGORY_QUERIES.get(cat, [])
            # 本地/快速验证用 RND_MAX_Q=1 限制每品类查询数；CI 可不设跑全量
            cap = int(os.environ.get("RND_MAX_Q", "0"))
            if cap > 0:
                qs = qs[:cap]
            for kw in qs:
                q = urllib_parse_quote(kw)
                url = ("https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s"
                       % (q, loc["hl"], loc["gl"], loc["ceid"]))
                try:
                    r = http_get(url)
                    feed = feedparser.parse(r.content)
                    for e in feed.entries[:5]:
                        link = e.get("link", "")
                        title = (e.get("title", "") or "").strip()
                        if not link or not title or link in seen:
                            continue
                        seen.add(link)
                        pub = _parse_time(e)
                        items.append(normalize(
                            platform="Google News",
                            url=link, title=title,
                            source_publisher=e.get("source", {}).get("title", "Google News"),
                            published=pub, market=mkt, category=_cat_key(cat),
                            summary=(e.get("summary", "") or "")[:240],
                            raw_signals={"query": kw, "source": "news_rss"},
                            evidence_tier=2,
                        ))
                except Exception:
                    continue
                time.sleep(0.3)  # 礼貌限速

    ok = True
    err = None
    if not items:
        ok, err = False, "no items parsed"
    return items, {
        "ok": ok, "count": len(items),
        "elapsed_ms": int((time.time() - t0) * 1000),
        "error": err, "last_ok": None if not ok else _now(),
        "note": "Google News RSS 四语种",
    }


def _now():
    import datetime
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def _cat_key(cat):
    return {"beauty": "beauty", "home": "home", "3c": "3c", "outdoor": "outdoor"}.get(cat, "other")


def urllib_parse_quote(s):
    import urllib.parse
    return urllib.parse.quote(s)
