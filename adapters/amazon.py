"""Amazon 榜单/热度适配器。

真实接入方式：
- 官方：**Amazon Product Advertising API (PA-API 5.0)**（需 Associates 账号并产生过合规销售，
  否则拿不到权限）；**Brand Analytics**（仅品牌注册卖家）。
- 榜单（Movers & Shakers / Best Sellers）无官方免费 JSON 接口；合规途径为
  官方新闻稿与行业报告（二级信源）。
- 严禁：绕过 robots/登录态批量抓 Amazon 前台（违反其 Conditions of Use）。

密钥环境变量：HOTSPOT_AMZ_KEY（PA-API access key / tag）。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class AmazonAdapter(BaseAdapter):
    name = "amazon"
    platform_label = "Amazon"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            return FetchResult(demo=True, extra={"reason": "未配置 PA-API 凭证；榜单走二级信源"})
        raise NotImplementedError(
            "接入点：PA-API5 GetItems / GetBrowseNodes；Best Sellers 无官方接口，"
            "建议用新闻稿+行业复盘补齐。申请：https://affiliate-program.amazon.com/"
        )
