"""适配器基类：统一抓取接口、限流钩子、重试钩子。

每个具体适配器负责一个数据源（TikTok / Amazon / 新闻 RSS …）。
真实接入时在子类 fetch() 里调用官方 API；未接入时返回带 DEMO 标记的样例，
**绝不伪造真实指标**（播放量/排名等一律标注 estimated / demo）。
"""
from __future__ import annotations

import abc
import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class FetchResult:
    """一次抓取的返回。

    cursor:  下一页/下一时间窗游标（不透传具体类型，由适配器自定义）
    items:   原始热点 dict 列表（结构对齐 RESEARCH_SCHEMA）
    extra:   附加元信息（榜单快照、抓取耗时等）
    demo:    True 表示本次返回的是离线样例，未真实联网
    """

    cursor: Any = None
    items: list[dict[str, Any]] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)
    demo: bool = True


class BaseAdapter(abc.ABC):
    """所有数据源适配器的抽象基类。"""

    name: str = "base"            # 与 config.data_sources 的 key 一致
    market: str = "GLOBAL"        # 默认覆盖市场，子类可覆写
    platform_label: str = "未命名平台"

    def __init__(self, api_key: str = "", enabled: bool = True,
                 rate_limit_per_min: int = 30,
                 retry_hook: Callable[[Callable, str], Any] | None = None) -> None:
        self.api_key = api_key
        self.enabled = enabled
        self.rate_limit_per_min = rate_limit_per_min
        self._retry_hook = retry_hook   # 由 reliability.retry 注入
        self._last_call_ts = 0.0

    # ---- 限流：保证两次外部调用间隔 >= 60/rate_limit_per_min 秒 ----
    def _throttle(self) -> None:
        gap = 60.0 / max(1, self.rate_limit_per_min)
        wait = gap - (time.time() - self._last_call_ts)
        if wait > 0:
            time.sleep(wait)
        self._last_call_ts = time.time()

    def call_with_retry(self, fn: Callable, action: str = "fetch") -> Any:
        """带重试钩子的调用；未注入钩子时直接执行。"""
        if self._retry_hook is not None:
            return self._retry_hook(fn, f"{self.name}:{action}")
        return fn()

    @abc.abstractmethod
    def fetch(self, session: Any = None, since: str = "",
              cursor: Any = None) -> FetchResult:
        """抓取 since（ISO 日期）之后的新信号，翻页游标 cursor 透传。"""
        raise NotImplementedError
