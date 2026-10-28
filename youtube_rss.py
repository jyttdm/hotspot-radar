# -*- coding: utf-8 -*-
"""YouTube 频道 RSS（免 Key）。

URL: https://www.youtube.com/feeds/videos.xml?channel_id={ID}
频道 ID 清单放 config.yaml / 环境变量，由用户维护。
"""
import time, datetime
import feedparser
from .base import http_get, normalize

# 默认订阅的带货/测评频道（用户可在配置里增删）
DEFAULT_CHANNELS = {
    "US": [
        # 示例占位频道 ID，用户自行替换为真实带货/测评频道
        # "UCxxxxxxxxxxxxxxxxxxxxxx",
    ],
    "ID": [],
    "VN": [],
}


def fetch(cfg):
    t0 = time.time()
    items = []
    channels = cfg.get("youtube_channels", DEFAULT_CHANNELS)
    for mkt, ids in channels.items():
        for cid in ids:
            try:
                url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + cid
                r = http_get(url)
                feed = feedparser.parse(r.content)
                for e in feed.entries[:5]:
                    vid = e.get("videoid") or e.get("yt_videoid") or ""
                    link = e.get("link") or ("https://www.youtube.com/watch?v=" + vid)
                    title = (e.get("title", "") or "").strip()
                    if not title:
                        continue
                    pub = ""
                    tp = e.get("published_parsed")
                    if tp:
                        pub = datetime.datetime(*tp[:6]).isoformat()
                    items.append(normalize(
                        platform="YouTube", url=link, title=title,
                        source_publisher=e.get("author", "YouTube"),
                        published=pub, market=mkt, category="3c",
                        summary=(e.get("summary", "") or "")[:240],
                        raw_signals={"channel_id": cid, "video_id": vid, "source": "yt_rss"},
                        evidence_tier=2,
                    ))
            except Exception:
                continue
            time.sleep(0.3)
    if not items and not any(channels.values()):
        return items, {"ok": True, "count": 0,
                       "elapsed_ms": int((time.time() - t0) * 1000),
                       "error": None, "last_ok": None,
                       "note": "YouTube RSS：未配置频道 ID（在 config 里订阅）"}
    return items, {"ok": True, "count": len(items),
                   "elapsed_ms": int((time.time() - t0) * 1000),
                   "error": None, "last_ok": _now() if items else None,
                   "note": "YouTube 频道 RSS"}


def _now():
    import datetime
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")
