"""Facebook 热点适配器。

真实接入方式：
- 官方：**Meta Graph API**（developers.facebook.com），需应用审核 + 用户/页面授权；
  公共话题趋势无开放接口，页面_insights 仅能读已授权页面数据。
- 未授权时用新闻/行业报告二级信源。

合规：遵守 Meta 平台条款；不可抓取未授权用户数据。

密钥环境变量：HOTSPOT_FB_KEY。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class FacebookAdapter(BaseAdapter):
    name = "facebook"
    platform_label = "Facebook"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            return FetchResult(demo=True, extra={"reason": "未配置 HOTSPOT_FB_KEY，跳过"})
        raise NotImplementedError(
            "接入点：/{page-id}/insights?metric=page_engaged_users 等；公开热点无开放接口，"
            "建议作为二级信源补充。申请：https://developers.facebook.com/"
        )
