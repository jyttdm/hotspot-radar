"""Shopee 适配器（东南亚：ID/VN 等）。

真实接入方式：
- 官方：**Shopee Open Platform**（https://open.shopee.com/），需开发者注册 +
  店铺授权（Partner），可用 Item/Publication 等开放接口；类目热搜榜需对应权限。
- 大促节点（11.11 等）以 Shopee 官方卖家中心公告与新闻稿为准。

合规：仅抓取已授权店铺/公开商品接口数据；遵守 Shopee Open Platform 协议。

密钥环境变量：HOTSPOT_SHOPEE_KEY。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class ShopeeAdapter(BaseAdapter):
    name = "shopee"
    platform_label = "Shopee"
    market = "ID"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            return FetchResult(demo=True, extra={"reason": "未配置 Shopee Open Platform 凭证"})
        raise NotImplementedError(
            "接入点：/api/v2/item/get_list 等（需 shopid + sign 签名）；"
            "申请：https://open.shopee.com/ （开发者注册 + 店铺授权）。"
        )
