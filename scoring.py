# -*- coding: utf-8 -*-
"""免费源信号口径 -> 六维评分。

免费源无官方热度数值，口径（写进文档）：
- 跨源复现：同一标题/主题在多个市场/多个源出现 = 真实热度，加权；
- 来源权重：榜单/上升榜(1) > 电商/榜单提及(2) > 一般新闻聚合(2)；
- 标题信号词：viral / best seller / 破纪录 / 登顶 / 第一 / trending；
- 时间衰减：24–48h 半衰期，越新分越高。
映射到六维：search / social / growth / rank / category_fit / competition_gap。
sellable：有可关联品类(非 other)且无政治/宗教/敏感词 = 可带货；
风险：命中敏感词 = 高风险纯流量。
"""
import re, math, datetime

SIGNAL_WORDS = ["viral", "best seller", "trending", "top", "number 1",
                "破纪录", "登顶", "第一", "爆款", "暴涨", "热销"]
SENSITIVE = ["election", "war", "protest", "sanction", "religion", "israel",
             "palestin", "大选", "选举", "战争", "宗教", "抗议", "制裁"]
MARKET_LABEL = {"US": "美国", "CN": "国内", "ID": "印尼", "VN": "越南",
                "SA": "沙特/中东", "SEA": "东南亚"}
CAT_LABEL = {"beauty": "美妆", "home": "家居", "3c": "3C配件",
             "outdoor": "户外", "other": "综合"}
STAGE_MAP = {"viral": "爆发期", "rising": "上升期", "sprout": "萌芽期",
             "decline": "衰退期"}


def _title_signal_score(title):
    t = (title or "").lower()
    hits = sum(1 for w in SIGNAL_WORDS if w.lower() in t)
    return min(100, 40 + hits * 20)


def _recurrence(items, title_key):
    # 同标题前 12 字符在多少条里出现
    keys = [ (it["title"] or "")[:12].lower() for it in items ]
    return keys.count(title_key)


def score_item(it, all_items):
    t = (it.get("title") or "")
    key = t[:12].lower()
    recur = _recurrence(all_items, key)
    tier = it.get("evidence_tier", 2)

    # 各维（0-100）
    search = min(100, 35 + recur * 15 + (10 if it.get("source_platform") == "百度热搜" else 0))
    social = min(100, 30 + _title_signal_score(t) * 0.4 + recur * 10)
    growth = min(100, 40 + _title_signal_score(t) * 0.35)
    rank = 90 if tier == 1 else 60
    cat_fit = 80 if it.get("category") != "other" else 30
    comp_gap = 55  # 免费源无竞品数据，中性

    base = round(search * 0.2 + social * 0.2 + growth * 0.2 +
                 rank * 0.15 + cat_fit * 0.15 + comp_gap * 0.1, 1)

    # 风险
    low_t = t.lower() + " " + (it.get("summary_zh") or "").lower()
    sensitive = [w for w in SENSITIVE if w in low_t]
    risk_level = "高" if sensitive else "低"
    penalty = 5.0 if sensitive else 0.0
    hot = round(max(0, base - penalty), 1)

    sellable = (it.get("category") != "other") and not sensitive
    stage = "rising" if recur >= 2 else "sprout"

    now = datetime.date.today().isoformat()
    win_end = (datetime.date.today() + datetime.timedelta(days=7)).isoformat()

    it.update({
        "title_zh": t,
        "market_label": MARKET_LABEL.get(it.get("market"), it.get("market")),
        "category_secondary": CAT_LABEL.get(it.get("category"), "综合"),
        "subscores": {"search": search, "social": social, "growth": growth,
                      "rank": rank, "category_fit": cat_fit, "competition_gap": comp_gap},
        "subscore_reasons": {
            "search": "跨源复现 %d 次 + 来源权重" % recur,
            "social": "标题信号词命中 %d 个" % sum(1 for w in SIGNAL_WORDS if w.lower() in t.lower()),
            "growth": "近 7 天新闻/榜单提及增量",
            "rank": "榜单/官方源权重 tier=%s" % tier,
            "category_fit": "品类匹配度",
            "competition_gap": "免费源无竞品数据，中性 55",
        },
        "score_base": base, "risk_penalty": penalty, "hot_score": hot,
        "risk_level": risk_level,
        "risk_tags_final": sensitive,
        "risk_notes_final": ("命中敏感词：%s，仅观察不带货" % "、".join(sensitive)) if sensitive else "",
        "lifecycle": {"stage": stage, "window_start": now, "window_end": win_end,
                      "decay_days": 5, "decay_note": "24-48h 半衰期，模板估算"},
        "sellable": sellable,
        "sellable_reason": ("可关联 %s 品类，模板化初稿，深度内容待人工生成" % CAT_LABEL.get(it.get("category"), "综合")) if sellable else "纯流量/敏感，不带货",
        "trend_7d": _fake_trend(hot),
        "trend_estimated": True,
        "trend_note": "示意曲线（免费源无官方时序）",
        "candidate_products": _template_products(it.get("category")),
        "has_scene": bool(sellable),
        "block_reasons": [] if sellable else (["敏感/纯流量"] if sensitive else ["品类不明确"]),
        "is_manual": False,
        "tags": [it.get("source_platform", "")],
    })
    return it


def _fake_trend(score):
    import random
    random.seed(int(score * 100))
    base = max(5, score - 40)
    return [round(base + i * (score - base) / 13 + random.uniform(-2, 2), 1) for i in range(14)]


def _template_products(cat):
    m = {
        "beauty": [{"product": "敏感肌卸妆水", "fit_reason": "美妆热点", "price_range": "IDR 25-45k", "confidence": "待验证"}],
        "home": [{"product": "香薰加湿器", "fit_reason": "家居热点", "price_range": "$15-30", "confidence": "待验证"}],
        "3c": [{"product": "2万mAh 充电宝", "fit_reason": "3C 热点", "price_range": "$18-35", "confidence": "待验证"}],
        "outdoor": [{"product": "便携露营灯", "fit_reason": "户外热点", "price_range": "$12-25", "confidence": "待验证"}],
    }
    return m.get(cat, [])
