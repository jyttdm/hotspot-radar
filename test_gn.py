# -*- coding: utf-8 -*-
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"C:\Users\超级无敌鸡腿\Doubao\chats\2026-10-25\new-chat\hotspot-radar-cloud")
import adapters.google_news as gn
t=time.time()
items, st = gn.fetch({"markets":["US"], "categories":["beauty"]})
print("gnews:", st)
for it in items[:5]:
    print(" -", it["title"][:80])
print("elapsed", round(time.time()-t,1), "s")
