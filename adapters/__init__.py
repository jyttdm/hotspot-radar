"""adapters — 各数据源适配器，统一输出标准化条目。

每个适配器是一个函数，接收 config dict，返回 (items, status)。
items: list[dict]，字段见 adapters/base.py::normalize
status: dict {ok, count, elapsed_ms, error, last_ok, note}
"""
