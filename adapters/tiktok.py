"""TikTok 热点适配器。

真实接入方式（合规路径）：
- 官方开放平台：TikTok for Developers（https://developers.tiktok.com/），
  产品选型 **Research API**（需审核，面向学术/研究机构）或
  **Display API / Content Posting API**（面向品牌与开发者，需企业资质审核）。
- 电商侧：**TikTok Shop Open Platform**（见 tiktok_shop.py），需店铺与类目授权。
- 未获授权时：通过新闻稿、行业博客（如 Curatsy、Ocean Engine 复盘）等二级信源观察，
  对应本工程 research_*.json 里 evidence_tier="二级" 的条目。

合规红线：不得绕过 TikTok 反爬/登录态抓取用户隐私数据；遵守平台
Programmable Content 条款与当地数据法（GDPR / PDP 等）。

密钥环境变量：HOTSPOT_TIKTOK_KEY。
"""
from __future__ import annotations

from ..models import RawSignals
from .base import BaseAdapter, FetchResult


class TikTokAdapter(BaseAdapter):
    name = "tiktok"
    platform_label = "TikTok"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            # 未配置密钥：明确降级，不伪造播放量
            return FetchResult(demo=True, extra={"reason": "未配置 HOTSPOT_TIKTOK_KEY，跳过真实抓取"})
        # —— 真实接入位置 ——
        # resp = self.call_with_retry(
        #     lambda: session.get("https://open.tiktokapis.com/v2/research/video/query/",
        #                         headers={"Authorization": f"Bearer {self.api_key}"},
        #                         json={"query": {"and": [{"operation": "IN", "field_name": "region_code",
        #                                                  "values": ["US"]}]}, "start_date": since}),
        #     action="research_query")
        # items = [_normalize(v) for v in resp.json()["data"]["videos"]]
        raise NotImplementedError(
            "TikTok Research/Display API 已具备密钥骨架，正式接入时在此补全请求与字段映射；"
            "申请入口：https://developers.tiktok.com/ （Research API 需机构审核）。"
        )
