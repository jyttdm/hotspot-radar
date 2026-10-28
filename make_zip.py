# -*- coding: utf-8 -*-
import os, zipfile, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
root = r"C:\Users\超级无敌鸡腿\Doubao\chats\2026-10-25\new-chat\hotspot-radar-cloud"
out = r"C:\Users\超级无敌鸡腿\Doubao\chats\2026-10-25\new-chat\hotspot-radar-cloud.zip"
skip_dirs = {"work", "_shots", "__pycache__", ".git"}
skip_ext = {".pyc"}
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in skip_dirs]
        for fn in fns:
            if os.path.splitext(fn)[1] in skip_ext: continue
            if fn in ("run.log",): continue
            p = os.path.join(dp, fn)
            arc = "hotspot-radar-cloud/" + os.path.relpath(p, root).replace("\\", "/")
            z.write(p, arc); n += 1
print("zip entries:", n, "size KB:", round(os.path.getsize(out)/1024,1))
