"""Google Trends 适配器。

真实接入方式：
- Google 无官方公开 JSON Trends API。合规途径：
  1) 第三方官方授权/趋势数据服务商（如 SerpApi Trends 节点、DataForSEO）——按其 ToS；
  2) 开源库 pytrends（非官方，受 Google 限流与 ToS 约束，高频抓取有被封风险，仅适合低频抽检）。
- 本工程默认走"二级信源"：媒体对搜索趋势的报道（evidence_tier="二级"）。

合规：不得高频绕过 Google 反爬；第三方接口的字段口径需在 notes 标注估算来源。

密钥环境变量：HOTSPOT_GT_KEY（第三方趋势服务 key，可空）。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class GoogleTrendsAdapter(BaseAdapter):
    name = "google_trends"
    platform_label = "Google Trends"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        # 演示样例：明确标注 estimated，不伪造真实指数
        demo_items = [{
            "id": "demo-gtrends-001",
            "title": "demo: candle warmer lamp trend interest",
            "source_platform": "Google Trends（示意）",
            "source_type": "search",
            "source_url": "",
            "is_real": False,
            "notes": "演示占位：真实接入时替换为第三方趋势接口返回的搜索指数序列。",
        }]
        return FetchResult(demo=True, items=demo_items,
                           extra={"reason": "Google 无官方公开 API；演示样例仅为结构占位"})
