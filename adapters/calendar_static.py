# -*- coding: utf-8 -*-
"""节日日历适配器：复用现有静态 calendar.json（确定性，无网络）。"""
import json, os, time


def fetch(cfg):
    t0 = time.time()
    path = cfg.get("calendar_path") or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "site", "data", "calendar.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        evts = data.get("events", [])
        return [], {"ok": True, "count": len(evts),
                    "elapsed_ms": int((time.time() - t0) * 1000),
                    "error": None, "last_ok": None,
                    "note": "节日日历（静态 %d 个节点）" % len(evts)}
    except Exception as e:  # noqa
        return [], {"ok": False, "count": 0,
                    "elapsed_ms": int((time.time() - t0) * 1000),
                    "error": str(e), "last_ok": None, "note": "节日日历"}
