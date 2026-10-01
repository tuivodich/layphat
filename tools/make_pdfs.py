#!/usr/bin/env python3
"""Tạo bản PDF cho từng bài viết (trang có class="post-end") vào public/pdf/<tên-trang>.pdf.
Chạy sau gen_site.py. Cần: pip install playwright && playwright install chromium"""
import os, sys, re, threading, functools, http.server
from playwright.sync_api import sync_playwright

PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
PUB = os.path.abspath(PUB)
OUT = os.path.join(PUB, "pdf"); os.makedirs(OUT, exist_ok=True)
pages = [f for f in sorted(os.listdir(PUB)) if f.endswith(".html") and 'class="post-end"' in open(os.path.join(PUB, f), encoding="utf-8").read()]

H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=PUB)
H.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
port = srv.server_address[1]

ok = 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for f in pages:
        try:
            pg = b.new_page()
            pg.goto(f"http://127.0.0.1:{port}/{f}", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.emulate_media(media="print")
            pg.pdf(path=os.path.join(OUT, f[:-5] + ".pdf"), format="A4", print_background=False,
                   margin=dict(top="16mm", bottom="16mm", left="14mm", right="14mm"))
            pg.close(); ok += 1; print("PDF:", f)
        except Exception as e:
            print(f"::warning::Không tạo được PDF cho {f}: {e}")
    b.close()
print(f"Đã tạo {ok}/{len(pages)} PDF")
