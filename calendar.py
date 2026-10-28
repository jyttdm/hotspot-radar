"""节日营销日历适配器（确定性、零外部依赖、真实可用）。

日期固定节日不依赖任何 API；大促节点的"当年营销活动"需另行用新闻信源补充。
口径见 SCORING_SPEC 第九节。
"""
from __future__ import annotations

from .base import BaseAdapter, FetchResult
from ..models import CalendarEvent

# 基准 2026-10-25；节日日期为公历固定节点
BUILTIN_EVENTS: list[CalendarEvent] = [
    CalendarEvent(id="cal-halloween", name="万圣节 Halloween", date="2026-10-31",
                  markets=["US", "CN"], categories=["home", "beauty"],
                  content_window="2026-10-15~2026-10-30",
                  fulfillment_note="美国站履约尾窗约 10/27 前，之后仅数字内容/同城",
                  category_angles=["万圣主题家居装饰", "彩妆", "派对用品"]),
    CalendarEvent(id="cal-thanksgiving", name="美国感恩节", date="2026-11-26",
                  markets=["US"], categories=["home"],
                  content_window="2026-11-15~2026-11-26",
                  category_angles=["节日餐桌装饰", "家居氛围"]),
    CalendarEvent(id="cal-blackfriday", name="黑五 Black Friday", date="2026-11-27",
                  markets=["US"], categories=["3c", "home"],
                  content_window="2026-11-20~2026-11-27",
                  category_angles=["3C 配件折扣", "家居好物"]),
    CalendarEvent(id="cal-cybermonday", name="网一 Cyber Monday", date="2026-11-30",
                  markets=["US"], categories=["3c"],
                  content_window="2026-11-27~2026-11-30",
                  category_angles=["线上 3C 配件"]),
    CalendarEvent(id="cal-double11", name="双十一 11.11", date="2026-11-11",
                  markets=["CN", "SEA"], categories=["home", "beauty", "3c"],
                  content_window="2026-10-25~2026-11-11",
                  category_angles=["全品类大促"]),
    CalendarEvent(id="cal-shopee1111", name="Shopee/Lazada 11.11", date="2026-11-11",
                  markets=["SEA", "ID", "VN"], categories=["home", "beauty"],
                  content_window="2026-10-25~2026-11-11",
                  category_angles=["东南亚大促"]),
    CalendarEvent(id="cal-whitefriday", name="中东白色星期五 White Friday",
                  date="2026-11 下旬（各零售商不同）", markets=["SA"],
                  categories=["home", "3c"],
                  content_window="2026-11 中下旬",
                  fulfillment_note="Noon/Amazon.ae 起始日各年不同，需信源确认",
                  note="无法验证确切日期时按规范写'2026-11 下旬'"),
    CalendarEvent(id="cal-double12", name="双十二", date="2026-12-12",
                  markets=["CN"], categories=["home"],
                  content_window="2026-12-01~2026-12-12"),
    CalendarEvent(id="cal-christmas", name="圣诞备货 Christmas", date="2026-12-25",
                  markets=["US", "SA"], categories=["home", "beauty"],
                  content_window="2026-11-01~2026-12-15",
                  fulfillment_note="圣诞备货窗口在 11 月，12 月中旬后履约紧张"),
]


class CalendarAdapter(BaseAdapter):
    name = "calendar"
    platform_label = "节日营销日历"

    def fetch(self, session=None, since: str = "", cursor=None) -> FetchResult:
        items = [{
            "id": e.id, "title": e.name, "source_platform": "calendar",
            "source_type": "calendar", "date": e.date,
            "markets": e.markets, "categories": e.categories,
            "content_window": e.content_window,
            "fulfillment_note": e.fulfillment_note,
            "category_angles": e.category_angles,
            "is_real": True, "fetched_at": "2026-10-25",
        } for e in BUILTIN_EVENTS]
        return FetchResult(demo=False, items=items)
