"""Instagram 热点适配器。

真实接入方式：
- 官方：Meta 开发者平台（https://developers.facebook.com/），
  **Instagram Graph API**（需 Instagram 专业账号 + Facebook 页面绑定 + 用户授权），
  可读自己账号的媒体/评论；第三方公开话题热度无公开接口。
- 未授权时只能靠媒体报道与博主榜单（二级信源）。

合规红线：不得抓取非授权账号的隐私数据；遵守 Meta Platform Terms 与
Graph API 速率限制。

密钥环境变量：HOTSPOT_IG_KEY。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult


class InstagramAdapter(BaseAdapter):
    name = "instagram"
    platform_label = "Instagram"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        if not self.api_key:
            return FetchResult(demo=True, extra={"reason": "未配置 HOTSPOT_IG_KEY，跳过"})
        raise NotImplementedError(
            "Instagram Graph API 接入点：/me/media?fields=caption,like_count,timestamp；"
            "话题探索无公开 API，公开热度建议用二级信源补齐。申请：https://developers.facebook.com/"
        )
