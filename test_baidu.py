# -*- coding: utf-8 -*-
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"C:\Users\超级无敌鸡腿\Doubao\chats\2026-10-25\new-chat\hotspot-radar-cloud")
import adapters.baidu as bd
t=time.time()
items, st = bd.fetch({})
print("baidu:", st)
for it in items[:5]:
    print(" -", it["title"])
print("elapsed", round(time.time()-t,1), "s")
