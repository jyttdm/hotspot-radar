import requests
import re
from dataclasses import dataclass
from typing import List, Optional


# 通用 HTTP 请求封装
def http_get(url: str, timeout: int = 10, headers: dict = None) -> Optional[str]:
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if headers:
        default_headers.update(headers)
    try:
        resp = requests.get(url, headers=default_headers, timeout=timeout)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
        return resp.text
    except Exception:
        return None


# 文本规范化（去多余空白、换行）
def normalize(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# 单条热点数据结构
@dataclass
class FetchResult:
    title: str
    url: str
    hot: str = ""
    rank: int = 0


# 适配器基类
class BaseAdapter:
    name = "base"
    url = ""

    def fetch(self) -> List[FetchResult]:
        raise NotImplementedError("子类必须实现 fetch 方法")
