"""YouTube 热点适配器。

真实接入方式：
- 官方：**YouTube Data API v3**（Google Cloud 项目启用，API Key 即可，无需企业审核），
  可用 search.list / videos.list / videoCategories.list 拿趋势视频与播放量。
  申请入口：https://console.cloud.google.com/（启用 YouTube Data API v3）。
- 趋势榜单：YouTube 官方 Trending 页面无官方 JSON 接口，可用第三方合规趋势接口或二级信源。

合规：遵守 Google API Services User Data Policy；每日配额默认 10k 单位，需规划批次。

密钥环境变量：HOTSPOT_YT_KEY。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class YouTubeAdapter(BaseAdapter):
    name = "youtube"
    platform_label = "YouTube"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            return FetchResult(demo=True, extra={"reason": "未配置 HOTSPOT_YT_KEY，跳过"})
        raise NotImplementedError(
            "接入点：youtube/v3/search.list?chart=mostPopular&regionCode=US 与 "
            "videos.list?part=snippet,statistics；密钥在 Google Cloud Console 启用 YouTube Data API v3 获得。"
        )
