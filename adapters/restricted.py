# -*- coding: utf-8 -*-
"""受限平台适配器骨架：TikTok/IG/FB/Amazon/Shopee/TikTok Shop/AliExpress。

统一从环境变量读密钥；未配置则优雅跳过，UI 显示"未配置 Key"。
合规：仅官方 API，不绕风控、不模拟登录、不破解签名。
"""
import os, time

# 平台 -> (需要的环境变量, 申请入口提示)
PLATFORM_KEYS = {
    "TikTok": (["TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET"],
               "https://developers.tiktok.com/"),
    "Meta(IG/FB)": (["META_ACCESS_TOKEN"],
                    "https://developers.facebook.com/"),
    "Amazon PA-API": (["AMAZON_PA_ACCESS_KEY", "AMAZON_PA_SECRET_KEY"],
                      "https://affiliate-program.amazon.gov/"),
    "EchoTik(TikTok)": (["ECHOTIK_API_KEY"], "https://www.echotik.live/"),
    "FastMoss(TikTok)": (["FASTMOSS_API_KEY"], "https://www.fastmoss.com/"),
    "Shopee Open API": (["SHOPEE_API_KEY", "SHOPEE_API_SECRET"],
                        "https://open.shopee.com/"),
    "YouTube Data API": (["YOUTUBE_API_KEY"], "https://console.cloud.google.com/"),
}


def fetch(cfg):
    t0 = time.time()
    configured = []
    for plat, (keys, _url) in PLATFORM_KEYS.items():
        if all(os.environ.get(k) for k in keys):
            configured.append(plat)
    if not configured:
        return [], {"ok": True, "count": 0,
                    "elapsed_ms": int((time.time() - t0) * 1000),
                    "error": None, "last_ok": None,
                    "note": "受限平台：未配置任何 Key（7 个平台待接入）"}
    # 已配置 Key 的平台在这里走官方 API；当前为骨架，返回空+说明
    return [], {"ok": True, "count": 0,
                "elapsed_ms": int((time.time() - t0) * 1000),
                "error": None, "last_ok": None,
                "note": "已检测到 Key：%s（适配器待对接官方 API）" % ", ".join(configured)}
