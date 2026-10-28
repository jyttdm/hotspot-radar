# -*- coding: utf-8 -*-
"""pytrends 关键词兴趣度验证（增强信号，CI 中 429/404 优雅降级不阻断）。

免费源无官方热度数值，这里用 interest_over_time 给关键词打分；
失败/限流即跳过，不影响主链路。趋势信号可由 Google News RSS 多源复现替代。
"""
import time, os


def fetch(cfg):
    t0 = time.time()
    kw = cfg.get("trend_keywords", ["black friday 2026", "skincare trend", "11.11 sale"])
    try:
        from pytrends.request import TrendReq
        pt = TrendReq(hl="en-US", tz=360, retries=1, backoff_factor=0.5)
        out = {}
        for k in kw[:5]:
            try:
                pt.build_payload([k], timeframe="now 7-d")
                df = pt.interest_over_time()
                if not df.empty and "isPartial" in df.columns:
                    s = df[k].dropna()
                    if len(s) >= 2:
                        out[k] = {"latest": int(s.iloc[-1]), "delta": int(s.iloc[-1] - s.iloc[0])}
            except Exception:
                continue
            time.sleep(0.5)
        if not out:
            return [], {"ok": True, "count": 0,
                        "elapsed_ms": int((time.time() - t0) * 1000),
                        "error": "pytrends 429/不可用，已优雅降级", "last_ok": None,
                        "note": "Google Trends（pytrends）— 已降级"}
        return [], {"ok": True, "count": len(out),
                    "elapsed_ms": int((time.time() - t0) * 1000),
                    "error": None, "last_ok": None,
                    "note": "pytrends 关键词兴趣：%s" % ",".join(out.keys())}
    except Exception as e:  # noqa
        return [], {"ok": True, "count": 0,
                    "elapsed_ms": int((time.time() - t0) * 1000),
                    "error": "pytrends 不可用：%s" % e, "last_ok": None,
                    "note": "Google Trends（pytrends）— 已降级"}
