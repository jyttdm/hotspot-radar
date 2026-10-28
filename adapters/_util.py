# -*- coding: utf-8 -*-
"""适配器公共工具：HTTP session、UA、错误归一化。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
import time

import requests

from ..config import SETTINGS

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


@dataclass
class AdapterResult:
    ok: bool
    status_code: int | str = ""
    latency_ms: int = 0
    items: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""
    sample: str = ""


def http_get(url: str, *, timeout: int = 8, headers: dict | None = None) -> tuple[int, float, bytes, str | None]:
    """GET 并返回 (status, latency_ms, content, error)。"""
    h = {"User-Agent": UA, "Accept": "*/*",
         "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
    if headers:
        h.update(headers)
    t0 = time.time()
    try:
        r = requests.get(url, headers=h, timeout=timeout, proxies=SETTINGS.proxies)
        return r.status_code, int((time.time() - t0) * 1000), r.content, None
    except Exception as e:  # noqa: BLE001
        return "ERR", int((time.time() - t0) * 1000), b"", f"{type(e).__name__}: {e}"
