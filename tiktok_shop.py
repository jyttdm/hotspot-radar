"""TikTok Shop 适配器（东南亚/美区电商侧）。

真实接入方式：
- 官方：**TikTok Shop Open Platform**（https://partner.tiktokshop.com/），
  需店铺/达人资质、应用审核与授权；可拉商品表现、趋势榜单（部分市场开放）。
- 与 tiktok.py（内容侧 Research API）是两套资质，勿混用。

合规：遵守 TikTok Shop Partner Network 协议与数据出境规则。

密钥环境变量：HOTSPOT_TTS_KEY。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class TikTokShopAdapter(BaseAdapter):
    name = "tiktok_shop"
    platform_label = "TikTok Shop"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            return FetchResult(demo=True, extra={"reason": "未配置 TikTok Shop 凭证"})
        raise NotImplementedError(
            "接入点：/product/202309/products/search、/performance/ 等（需 shop_cipher + sign）；"
            "申请：https://partner.tiktokshop.com/ "
        )
