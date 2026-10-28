# -*- coding: utf-8 -*-
"""每日抓取主编排：
1. 调各 adapter 抓真实条目；
2. 评分映射到六维；
3. 合并手工深度快照（6 个 playbook 保留）；
4. 产出 site/data/app-data.js + 数据源健康状态；
5. 单源失败不阻断，全部失败才报错。
"""
import os, sys, json, time, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import adapters.google_news as an_news
import adapters.baidu as an_baidu
import adapters.youtube_rss as an_yt
import adapters.calendar_static as an_cal
import adapters.pytrends_signal as an_pt
import adapters.domestic as an_dom
import adapters.restricted as an_res
import scoring

SITE = os.path.join(HERE, "site")
DATA = os.path.join(SITE, "data")

MANUAL_DIR = os.path.join(HERE, "manual")  # 手工快照目录（可选）


def load_json(p, default):
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def main():
    t0 = time.time()
    cfg = {"markets": ["US", "ID", "VN", "SA"],
           "categories": ["beauty", "home", "3c", "outdoor"]}

    health = []
    live_items = []

    adapters_list = [
        ("Google News RSS", an_news.fetch),
        ("百度热搜", an_baidu.fetch),
        ("YouTube RSS", an_yt.fetch),
        ("节日日历", an_cal.fetch),
        ("Google Trends(pytrends)", an_pt.fetch),
        ("国内源(默认关)", an_dom.fetch),
        ("受限平台(Key骨架)", an_res.fetch),
    ]

    for name, fn in adapters_list:
        try:
            items, st = fn(cfg)
        except Exception as e:  # noqa
            items, st = [], {"ok": False, "count": 0, "elapsed_ms": 0,
                             "error": str(e), "last_ok": None, "note": name}
        st["name"] = name
        health.append(st)
        if st.get("ok"):
            live_items.extend(items)
        print("[%-24s] ok=%s count=%d err=%s" % (name, st.get("ok"), st.get("count"), st.get("error")))

    # 全部失败判定
    any_ok = any(h.get("ok") for h in health)
    if not live_items and not any_ok:
        print("FATAL: 全部源失败", file=sys.stderr)
        sys.exit(1)

    # 去重（按 url）
    seen = set(); uniq = []
    for it in live_items:
        k = it.get("source_url") or it["id"]
        if k in seen:
            continue
        seen.add(k); uniq.append(it)

    # 评分
    scored = [scoring.score_item(it, uniq) for it in uniq]
    scored.sort(key=lambda x: -x["hot_score"])

    # 合并手工快照（如有）
    manual = load_json(os.path.join(MANUAL_DIR, "hotspots.json"), [])
    manual_pb = load_json(os.path.join(MANUAL_DIR, "content.json"), {"playbooks": {}})
    for h in manual:
        h.setdefault("is_manual", True)
    all_hotspots = scored + manual

    # sources 台账
    sources = [{
        "id": h["id"], "source_platform": h.get("source_platform"),
        "source_url": h.get("source_url"), "source_title": h.get("title_zh"),
        "source_publisher": h.get("source_publisher"),
        "evidence_tier": h.get("evidence_tier", 2),
        "fetched_at": h.get("fetched_at"), "is_real": h.get("is_real", True),
        "metrics_verifiable": h.get("trend_estimated") is not True,
    } for h in all_hotspots]

    # report
    sellable_n = sum(1 for h in all_hotspots if h.get("sellable"))
    high_n = sum(1 for h in all_hotspots if h.get("risk_level") == "高")
    report = {
        "report_date": datetime.date.today().isoformat(),
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "summary_stats": {"total": len(all_hotspots), "sellable": sellable_n,
                          "risk_high": high_n},
        "top_opportunities": [h["id"] for h in scored[:8]],
        "ignore_list": [{"id": h["id"], "reason": h.get("sellable_reason", "")}
                        for h in all_hotspots if not h.get("sellable")][:6],
        "next_actions": [{"priority": "P1", "action": "人工复核 Top 8 实时热点并生成深度方案"}],
        "coverage_note": "实时条目为模板化初稿，深度内容待人工；手工 6 方案标注人工深度版",
    }

    # config
    config = load_json(os.path.join(MANUAL_DIR, "config.json"), {
        "categories": [{"key": "beauty", "label": "美妆"}, {"key": "home", "label": "家居"},
                       {"key": "3c", "label": "3C配件"}, {"key": "outdoor", "label": "户外"}],
        "markets": [{"key": "US", "label": "美国"}, {"key": "CN", "label": "国内"},
                    {"key": "ID", "label": "印尼"}, {"key": "VN", "label": "越南"},
                    {"key": "SA", "label": "沙特/中东"}],
        "data_sources": [{"key": h["name"], "label": h["name"], "adapter": h["name"],
                          "enabled": bool(h.get("ok"))} for h in health],
        "score_threshold": 45,
    })

    calendar = load_json(os.path.join(DATA, "calendar.json"), {"events": []})

    data = {
        "meta": {"generated_at": report["generated_at"],
                 "next_run": "每日 09:00 / 21:00 (北京时间)",
                 "auto": True, "live_count": len(scored), "manual_count": len(manual)},
        "hotspots": all_hotspots,
        "content": {"version": "cloud", "count": len(manual_pb.get("playbooks", {})),
                    "playbooks": manual_pb.get("playbooks", {})},
        "calendar": calendar,
        "report": report,
        "sources": sources,
        "config": config,
        "health": health,
    }

    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "app-data.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("window.RADAR_DATA = " + json.dumps(data, ensure_ascii=False) + ";")
    with open(os.path.join(DATA, "health.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"generated_at": report["generated_at"], "sources": health},
                  f, ensure_ascii=False, indent=2)

    print("\nDONE: %d live + %d manual = %d hotspots in %dms"
          % (len(scored), len(manual), len(all_hotspots), int((time.time() - t0) * 1000)))


if __name__ == "__main__":
    main()
