"""新闻/行业 RSS 适配器（本骨架里真实可跑的采集通道之一）。

接入方式：订阅零售/电商/行业媒体 RSS，用 feedparser 解析；无需密钥。
示例源（可按需扩充到 config.yaml）：
- Modern Retail、Retail Dive、TikTok Shop 官方卖家新闻室、
  NRF Press、eMarketer 博客、亿邦动力、跨境知道等。

RSS 内容遵守各站点 ToS；仅摘要引用 + 回链原文，不全文转载。
"""
from __future__ import annotations

from datetime import date
from typing import Any

from .base import BaseAdapter, FetchResult

DEFAULT_FEEDS: list[str] = [
    "https://nrf.com/press-releases/rss.xml",          # NRF 新闻稿（可能失效，失败进死信）
]


class NewsRSSAdapter(BaseAdapter):
    name = "news_rss"
    platform_label = "新闻/行业 RSS"

    def __init__(self, feed_urls: list[str] | None = None, **kw: Any) -> None:
        super().__init__(**kw)
        self.feed_urls = feed_urls or DEFAULT_FEEDS

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        try:
            import feedparser  # type: ignore
        except ImportError:
            return FetchResult(demo=True,
                               extra={"reason": "未安装 feedparser；pip install feedparser 后启用真实 RSS 抓取"})
        items: list[dict[str, Any]] = []
        today = date.today().isoformat()
        for url in self.feed_urls:
            self._throttle()
            feed = self.call_with_retry(lambda u=url: feedparser.parse(u), action=f"parse:{url}")
            for e in feed.entries[:20]:
                items.append({
                    "id": f"news-{abs(hash(e.link)) % 10**8:08d}",
                    "title": getattr(e, "title", ""),
                    "source_platform": "news / RSS",
                    "source_type": "news",
                    "source_url": getattr(e, "link", ""),
                    "source_title": getattr(e, "title", ""),
                    "source_publisher": getattr(getattr(feed, "feed", {}), "title", url),
                    "fetched_at": today,
                    "is_real": True,
                    "evidence_tier": "一级",
                    "summary_zh": getattr(e, "summary", "")[:200],
                })
        return FetchResult(demo=False, items=items)
