"""AliExpress 适配器。

真实接入方式：
- 官方：**AliExpress Open Platform / Affiliate 联盟开放接口**
  （https://openservice.aliexpress.com/），需开发者注册；商品/选品榜接口按权限开通。
- 无公开 C 端热搜 API；热度以联盟选品榜 + 行业报道为准。

密钥环境变量：HOTSPOT_AE_KEY。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class AliExpressAdapter(BaseAdapter):
    name = "aliexpress"
    platform_label = "AliExpress"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            return FetchResult(demo=True, extra={"reason": "未配置 AliExpress Open Platform 凭证"})
        raise NotImplementedError(
            "接入点：aliexpress.affiliate.product.* 系列（需 app_key + sign）；"
            "申请：https://openservice.aliexpress.com/"
        )
