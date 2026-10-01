import os, re, html, sys, shutil, unicodedata, datetime
import os as _os
OUT = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "public")  # chạy: python3 tools/gen_site.py

NAV = [
  ("index.html","Trang chủ"),
  ("bai-viet.html","Bài viết Phật giáo"),
  ("kinh-ke.html","Bài kinh - kệ"),
  ("cau-nguyen.html","Lời chúc - Cầu nguyện"),
  ("mon-chay.html","Món chay"),
]

ICON = {
 "bai-viet":'<path d="M12 2.5c.6 3.2 5.6 4.6 6.6 9.2a6.6 6.6 0 01-13.2 0c1-4.6 6-6 6.6-9.2z"/><path d="M12 7v13.5"/><path d="M12 12l3-2M12 15l-3-2"/>',
 "kinh-ke":'<path d="M7 4h10a2 2 0 012 2v12a2 2 0 01-2 2H7a2 2 0 01-2-2V6a2 2 0 012-2z"/><path d="M9 9h6M9 12.5h6M9 16h3"/>',
 "cau-nguyen":'<path d="M12 4.5c2.2 2.6 2.7 5.4 0 9.5-2.7-4.1-2.2-6.9 0-9.5z"/><path d="M12 14c-3.2-.4-6.8-2.6-7.4-6.4 3.2 0 6.2 1.6 7.4 4.4"/><path d="M12 14c3.2-.4 6.8-2.6 7.4-6.4-3.2 0-6.2 1.6-7.4 4.4"/><path d="M5 17.5c4.2 3 9.8 3 14 0"/>',
 "mon-chay":'<path d="M4 12h16a8 8 0 01-16 0z"/><path d="M12 3.5c2.4 1 3.2 3.4 2 5.6-2.4-1-3.2-3.4-2-5.6z"/><path d="M8.5 5.5c-.8 1-.8 2 0 3"/>',
 # biểu tượng danh mục
 "enso":'<path d="M18.2 6.1A8.2 8.2 0 1 0 20.2 12.6"/><path d="M19.4 4.6l-1.4 1.8"/>',
 "lotus":'<path d="M12 4.5c2.2 2.6 2.7 5.4 0 9.5-2.7-4.1-2.2-6.9 0-9.5z"/><path d="M12 14c-3.2-.4-6.8-2.6-7.4-6.4 3.2 0 6.2 1.6 7.4 4.4"/><path d="M12 14c3.2-.4 6.8-2.6 7.4-6.4-3.2 0-6.2 1.6-7.4 4.4"/><path d="M5 17.5c4.2 3 9.8 3 14 0"/>',
 "mandala":'<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.4"/><path d="M12 3.5v5.1M12 15.4v5.1M3.5 12h5.1M15.4 12h5.1M6 6l3.1 3.1M14.9 14.9L18 18M18 6l-3.1 3.1M9.1 14.9L6 18"/>',
 "stupa":'<path d="M12 2.5v2.2"/><path d="M9.8 4.7h4.4"/><path d="M8.5 8.3c0-2.2 1.5-3.6 3.5-3.6s3.5 1.4 3.5 3.6"/><path d="M6 12.3c0-2.6 2.6-4 6-4s6 1.4 6 4"/><path d="M4.5 12.3h15"/><path d="M5.5 12.3V20M18.5 12.3V20M3.5 20h17"/><path d="M10 20v-3.2a2 2 0 014 0V20"/>',
 "boat":'<path d="M3 15.5h18l-2.6 4.5H5.6z"/><path d="M12 3.5v12"/><path d="M12 4.6c3.2 1.6 5.2 4.8 5.2 8.9H12"/><path d="M12 7c-2.2 1.2-3.8 3.7-3.8 6.5H12"/>',
 "vajra":'<ellipse cx="12" cy="12" rx="2" ry="2.6"/><path d="M12 9.4V5M12 14.6V19"/><path d="M12 5c-3 0-4.6 2-4.6 4.2M12 5c3 0 4.6 2 4.6 4.2M12 19c-3 0-4.6-2-4.6-4.2M12 19c3 0 4.6-2 4.6-4.2"/><path d="M12 5V2.8M12 19v2.2"/>',
}

SECTIONS = {
 "bai-viet": dict(file="bai-viet.html", title="Bài viết về Phật giáo", accent="var(--c1)", tag="Bài viết",
   lede="Những bài viết giới thiệu giáo lý, lịch sử và đời sống tu tập, trình bày rõ ràng, dễ đọc cho người mới bắt đầu.",
   items=[("Khổ đau và con đường để diệt trừ khổ","Đức Phật như vị thầy thuốc giỏi: biết bệnh, biết nguyên nhân, biết thuốc chữa và biết bệnh đã khỏi.","bai-viet-kho-dau-diet-kho.html"),
          ("Bát chánh đạo","Con đường tám nhánh hướng đến an lạc và giải thoát."),
          ("Ngũ giới cho người tại gia","Năm điều học giúp đời sống thanh tịnh, hài hòa."),
          ("Từ, bi, hỷ, xả","Bốn tâm vô lượng và cách vun trồng trong đời thường."),
          ("Thiền cho người mới bắt đầu","Những bước đầu tiên để ngồi thiền và quan sát hơi thở."),
          ("Ý nghĩa ngày rằm và mùng một","Vì sao nhiều người đi chùa, ăn chay vào những ngày này."),
          ("Tứ diệu đế","Bốn chân lý cao quý: khổ, nguyên nhân của khổ, sự diệt khổ và con đường diệt khổ."),
          ("Nhân quả và nghiệp","Hiểu đúng về nhân quả để sống có trách nhiệm với từng việc làm."),
          ("Quy y Tam bảo","Ý nghĩa của việc nương tựa Phật, Pháp, Tăng trong đời sống.")]),
 "kinh-ke": dict(file="kinh-ke.html", title="Bài kinh - kệ", accent="var(--c2)", tag="Kinh kệ",
   lede="Tuyển tập các bài kinh, kệ, chú thường tụng, kèm phần chú giải ngắn gọn. Văn bản sẽ được bổ sung từ nguồn dịch được phép sử dụng.",
   items=[("Kinh Nhật tụng","Nghi thức niệm Phật hằng ngày: đảnh lễ, tán Phật, niệm Phật, sám hối, phát nguyện, quy y, hồi hướng.","kinh-nhat-tung.html"),
          ("Kinh Kim Cang","Kinh Đại thừa về trí tuệ Bát nhã."),
          ("Kinh A Di Đà","Kinh nền tảng của pháp môn Tịnh độ."),
          ("Kinh Pháp Cú","Những bài kệ ngắn về đạo đức và tu tập."),
          ("Phẩm Phổ Môn","Phẩm nói về Bồ Tát Quán Thế Âm."),
          ("Kinh Vu Lan Báo Hiếu","Bài kinh về lòng hiếu thảo với cha mẹ.")]),
 "cau-nguyen": dict(file="cau-nguyen.html", title="Lời chúc - Cầu nguyện", accent="var(--c3)", tag="Cầu nguyện",
   lede="Những lời chúc và bài văn khấn, cầu nguyện cho các dịp lễ, giúp bạn gửi lời thăm hỏi trang nghiêm, ấm áp.",
   items=[("Lời chúc mừng Phật đản","Gửi đến người thân, bạn bè nhân ngày Đản sanh."),
          ("Lời chúc mùa Vu Lan","Lời tri ân cha mẹ và báo hiếu."),
          ("Lời chúc đầu năm","Chúc an lạc, bình an cho cả gia đình."),
          ("Văn khấn ngày rằm","Bài khấn đơn giản khi lễ Phật tại nhà."),
          ("Lời nguyện hồi hướng","Hồi hướng công đức đến muôn loài."),
          ("Lời chúc thăm bệnh","Lời động viên an ủi người đang ốm đau.")]),
 "mon-chay": dict(file="mon-chay.html", title="Món chay", accent="var(--c4)", tag="Món chay",
   lede="Công thức món chay thanh đạm, dễ nấu, phù hợp cho ngày rằm, mùng một và bữa cơm gia đình.",
   items=[("Tôm đậu hũ kho cà chua","Món kho đậm đà với tôm chay, đậu hũ chiên và cà chua, nấu trong khoảng 10 phút.","mon-chay-tom-dau-hu-kho-ca-chua.html"),
          ("Canh nấm rơm","Canh thanh nhẹ, vị ngọt tự nhiên từ nấm."),
          ("Gỏi cuốn chay","Cuốn rau củ, chấm tương hoặc nước chấm chay."),
          ("Bún riêu chay","Nước dùng từ cà chua, đậu hũ, nấm."),
          ("Cà tím kho tộ","Cà tím mềm, thấm sốt đậm đà."),
          ("Cháo đậu xanh","Món cháo ấm bụng, hợp cho buổi sáng.")]),
}

def icon(k, extra=""):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}>{ICON[k]}</svg>'

BG = "anhsang"
DEFAULT_OG = '<meta property="og:type" content="website">\n<meta property="og:title" content="{t}">\n<meta property="og:description" content="{d}">\n<meta property="og:image" content="https://layphatvn.web.app/images/og-default.jpg">\n<meta name="twitter:card" content="summary_large_image">\n'

def head(title, desc, active, extra=''):
    nav = "".join(f'<a href="{f}"{" class=active" if f==active else ""}>{html.escape(t)}</a>' for f,t in NAV)
    return f'''<!doctype html>
<html lang="vi" data-theme="sen" data-bg="{BG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" sizes="32x32" type="image/png">
<link rel="shortcut icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta name="theme-color" content="#07130f">
<link rel="stylesheet" href="style.css">
{extra or DEFAULT_OG.format(t=html.escape(title), d=html.escape(desc))}</head>
<body>
<div class="wrap">
  <header class="topbar">
    <a class="brand" href="index.html">
      <svg class="brand-mark" viewBox="0 0 40 40" fill="none"><circle cx="20" cy="20" r="18" stroke="var(--gold)" stroke-width="1.4"/><circle cx="20" cy="20" r="6" stroke="var(--gold)" stroke-width="1.2"/><circle cx="20" cy="20" r="2.2" fill="var(--gold)"/><g stroke="var(--gold)" stroke-width="1.3" stroke-linecap="round"><line x1="20" y1="4" x2="20" y2="14"/><line x1="20" y1="26" x2="20" y2="36"/><line x1="4" y1="20" x2="14" y2="20"/><line x1="26" y1="20" x2="36" y2="20"/><line x1="8.7" y1="8.7" x2="15.8" y2="15.8"/><line x1="24.2" y1="24.2" x2="31.3" y2="31.3"/><line x1="31.3" y1="8.7" x2="24.2" y2="15.8"/><line x1="15.8" y1="24.2" x2="8.7" y2="31.3"/></g></svg>
      Lạy&nbsp;Phật
    </a>
  </header>
  <nav class="navbar"><div class="navlist">{nav}</div></nav>
'''

FOOT = '''
  <footer>
    <div class="foot-links">
      <a href="bai-viet.html">Bài viết Phật giáo</a><a href="kinh-ke.html">Bài kinh - kệ</a><a href="cau-nguyen.html">Lời chúc - Cầu nguyện</a><a href="mon-chay.html">Món chay</a>
    </div>
    <div class="foot-bottom">
      <span class="copyright">© 2024 - <span class="yr">2026</span> Bản quyền thuộc <a class="fb-link" href="https://facebook.com/layphatvn" target="_blank" rel="noopener noreferrer"><svg class="fb-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M22 12a10 10 0 10-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0022 12z"/></svg><span class="fb-sep">/</span>Lạy Phật</a>. Nếu sao chép hay trích dẫn nội dung của trang xin vui lòng ghi rõ nguồn và chỉ sử dụng với mục đích phi thương mại.</span>
      <span class="dim" aria-hidden="true">Nam mô A Di Đà Phật</span>
    </div>
  </footer>
</div>
<script src="app.js"></script>
</body>
</html>
'''


SAMPLES = {k: [it for it in s["items"] if len(it) == 2] for k, s in SECTIONS.items()}
LABEL = {"bai-viet": "Bài viết Phật giáo", "kinh-ke": "Bài kinh - kệ", "cau-nguyen": "Lời chúc - Cầu nguyện", "mon-chay": "Món chay"}
PREFIX = {"bai-viet": "bai-viet-", "kinh-ke": "kinh-", "cau-nguyen": "cau-nguyen-", "mon-chay": "mon-chay-"}
PH_ICON = {"bai-viet": "bai-viet", "kinh-ke": "cau-nguyen", "cau-nguyen": "cau-nguyen", "mon-chay": "mon-chay"}
SITE = "https://layphatvn.web.app"
ROOT = _os.path.abspath(_os.path.join(OUT, ".."))
CONTENT = _os.path.join(ROOT, "content")

# Danh mục của trang "Bài viết Phật giáo": (slug, tên, biểu tượng, màu, mô tả ngắn)
CATS = [
  ("thien-tong", "Thiền Tông", "enso", "var(--c1)", "Truyền thống nhấn mạnh tu tập thiền định, trực nhận bản tâm."),
  ("tinh-do-tong", "Tịnh Độ Tông", "lotus", "var(--c3)", "Pháp môn niệm danh hiệu Đức Phật A Di Đà, nguyện vãng sanh cõi Tây phương Cực Lạc."),
  ("mat-tong", "Mật Tông", "mandala", "var(--c2)", "Truyền thống tu tập với thần chú, thủ ấn và quán tưởng."),
  ("nguyen-thuy", "Phật giáo Nguyên Thủy", "stupa", "var(--c4)", "Truyền thống lưu giữ lời dạy sớm nhất của Đức Phật, gắn với Tam tạng Pali."),
  ("dai-thua", "Phật giáo Đại Thừa", "boat", "var(--c2)", "Truyền thống nhấn mạnh con đường Bồ Tát, hạnh từ bi và trí tuệ Bát nhã."),
  ("kim-cuong-thua", "Kim Cương Thừa", "vajra", "var(--c1)", "Truyền thống Mật thừa, phổ biến ở Tây Tạng và vùng Himalaya."),
]

import math
def rot(k, inner, n=8):
    return f'<g transform="rotate({k*360/n:.3f} 200 200)">{inner}</g>'
def build_wheel():
    l1 = '<circle cx="200" cy="200" r="176" class="w-line" stroke-width="1.4"/><circle cx="200" cy="200" r="160" class="w-line" stroke-width="1" opacity=".6"/>'
    l1 += "".join(rot(k,'<line x1="200" y1="24" x2="200" y2="40" class="w-line" stroke-width="1" opacity=".7"/>',24) for k in range(24))
    l1 += "".join(rot(k,'<circle cx="200" cy="168" r="5.2" class="w-fill"/>') for k in range(8))
    l2 = '<circle cx="200" cy="200" r="126" class="w-line" stroke-width="1.6"/><circle cx="200" cy="200" r="114" class="w-line" stroke-width="1" stroke-dasharray="2 5" opacity=".7"/>'
    l2 += "".join(rot(k,'<line x1="200" y1="86" x2="200" y2="150" class="w-line" stroke-width="3.2" stroke-linecap="round"/><circle cx="200" cy="80" r="7" fill="var(--c%d)"/>' % (k%4+1)) for k in range(8))
    petal = '<path d="M200 180C189 168 191 155 200 148C209 155 211 168 200 180Z" class="w-petal"/>'
    l3 = '<circle cx="200" cy="200" r="54" class="w-line" stroke-width="1.4"/>' + "".join(rot(k,petal) for k in range(8))
    hub = '<circle cx="200" cy="200" r="15" class="w-fill"/><circle cx="200" cy="200" r="7" fill="var(--bg)"/><circle cx="200" cy="200" r="2.6" class="w-fill"/>'
    stars = '<circle cx="60" cy="60" r="1.6" fill="#fff" opacity=".45"/><circle cx="345" cy="52" r="1.4" fill="#fff" opacity=".4"/><circle cx="40" cy="340" r="1.4" fill="#fff" opacity=".4"/><circle cx="360" cy="350" r="1.8" fill="#fff" opacity=".45"/>'
    return f'<svg viewBox="0 0 400 400" fill="none" role="img" aria-label="Bánh xe Pháp luân"><g id="w1">{l1}</g><g id="w2">{l2}</g><g id="w3">{l3}</g>{hub}</svg>'
WHEEL = build_wheel()
def post_footer(date_iso, display):
    return f"""
      <footer class="post-end">
        <p class="post-date">Đăng ngày <time datetime="{date_iso}">{display}</time></p>
        <div class="post-actions" role="group" aria-label="Chức năng bài viết">
          <button type="button" class="act" data-act="print"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9V3h12v6"/><rect x="4" y="9" width="16" height="8" rx="2"/><path d="M7 14h10v7H7z"/></svg>In trang này</button>
          <button type="button" class="act" data-act="download"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="M7 11l5 5 5-5"/><path d="M4 20h16"/></svg>Tải trang này</button>
          <div class="share-wrap">
            <button type="button" class="act" data-act="share" aria-haspopup="true" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="5" r="2.6"/><circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="19" r="2.6"/><path d="M8.3 10.8l7.4-4.4M8.3 13.2l7.4 4.4"/></svg>Chia sẻ trang</button>
            <div class="share-menu" role="menu" hidden>
              <button type="button" role="menuitem" data-share="copy">Sao chép liên kết</button>
              <button type="button" role="menuitem" data-share="facebook">Chia sẻ lên Facebook</button>
              <button type="button" role="menuitem" data-share="email">Gửi qua email</button>
            </div>
          </div>
        </div>
        <div class="toast" role="status" aria-live="polite"></div>
      </footer>
"""


# =====================================================================
#  ĐỌC NỘI DUNG TỪ THƯ MỤC content/  (file .txt / .md)
# =====================================================================
def fold(s):
    s = unicodedata.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", s.lower())

def slugify(s):
    s = unicodedata.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

TYPE_MAP = {"baiviet": "bai-viet", "baivietphatgiao": "bai-viet", "kinhke": "kinh-ke", "baikinhke": "kinh-ke", "kinh": "kinh-ke",
            "caunguyen": "cau-nguyen", "loichuc": "cau-nguyen", "loichuccaunguyen": "cau-nguyen", "monchay": "mon-chay"}
KEY_MAP = {"loai": "type", "danhmuc": "cat", "tieude": "title", "tenngan": "short", "ngay": "date", "anh": "image", "motaanh": "alt",
           "nguon": "source", "tomtat": "summary", "loiket": "signoff", "hashtag": "tags", "bailienquan": "related"}
CAT_BY_KEY = {}
for _slug, _name, *_ in CATS:
    for _k in {fold(_slug), fold(_name), fold(_name).replace("phatgiao", "")}:
        CAT_BY_KEY[_k] = _slug

WARNINGS = []
def warn(path, msg):
    rel = _os.path.relpath(path, ROOT)
    WARNINGS.append(f"{rel}: {msg}")
    print(f"::warning file={rel}::{msg}")

def parse_date(s):
    s = s.strip()
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T](\d{1,2}):(\d{2}))?$", s) or None
    if m:
        y, mo, d, h, mi = m.groups()
    else:
        m2 = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})(?:\s+(\d{1,2}):(\d{2}))?$", s)
        if not m2: return None, False
        d, mo, y, h, mi = m2.groups()
    try:
        return datetime.datetime(int(y), int(mo), int(d), int(h or 0), int(mi or 0)), bool(h)
    except ValueError:
        return None, False

def parse_body(text):
    items = []
    for blk in re.split(r"\n\s*\n", text.strip()):
        lines = [l.rstrip() for l in blk.split("\n") if l.strip()]
        while lines and lines[0].startswith("## "):
            items.append(("h2", lines.pop(0)[3:].strip()))
        if not lines: continue
        if all(l.startswith("> ") or l == ">" for l in lines): items.append(("verse", [l[2:] if l.startswith("> ") else "" for l in lines]))
        elif all(l.startswith("- ") for l in lines): items.append(("ul", [l[2:].strip() for l in lines]))
        elif all(re.match(r"^\d+[.)]\s+", l) for l in lines): items.append(("ol", [re.sub(r"^\d+[.)]\s+", "", l) for l in lines]))
        else: items.append(("p", " ".join(l.strip() for l in lines)))
    return items

def load_posts():
    posts, used = [], set()
    if not _os.path.isdir(CONTENT): return posts
    for dp, _dn, fns in _os.walk(CONTENT):
        for fn in sorted(fns):
            stem, ext = _os.path.splitext(fn)
            if ext.lower() not in (".txt", ".md") or stem.startswith("_") or fold(stem).startswith("huongdan"): continue
            path = _os.path.join(dp, fn)
            raw = open(path, encoding="utf-8-sig").read().replace("\r\n", "\n").replace("\r", "\n")
            parts = re.split(r"^\s*---\s*$", raw, maxsplit=1, flags=re.M)
            if len(parts) != 2: warn(path, "thiếu dòng '---' ngăn giữa phần thông tin và nội dung bài. Bỏ qua file này."); continue
            meta = {}
            for line in parts[0].split("\n"):
                if ":" not in line: continue
                k, v = line.split(":", 1)
                key = KEY_MAP.get(fold(k))
                if key: meta[key] = v.strip()
            ptype = TYPE_MAP.get(fold(meta.get("type", "")))
            if not ptype: warn(path, "thiếu hoặc sai dòng 'Loại:' (bai-viet, kinh-ke, cau-nguyen hoặc mon-chay). Bỏ qua file này."); continue
            if not meta.get("title"): warn(path, "thiếu dòng 'Tiêu đề:'. Bỏ qua file này."); continue
            dt, has_time = parse_date(meta.get("date", ""))
            if not dt: warn(path, "thiếu hoặc sai dòng 'Ngày:' (ví dụ 2026-10-05 hoặc 05/10/2026). Bỏ qua file này."); continue
            slug = slugify(stem)
            if slug.startswith(PREFIX[ptype]): slug = slug[len(PREFIX[ptype]):]
            fname = PREFIX[ptype] + slug + ".html"
            if fname in used: warn(path, f"trùng tên trang {fname} với một bài khác. Bỏ qua file này."); continue
            used.add(fname)
            cat = None
            if meta.get("cat"):
                cat = CAT_BY_KEY.get(fold(meta["cat"]))
                if not cat: warn(path, f"danh mục '{meta['cat']}' không có trong danh sách (Thiền Tông, Tịnh Độ Tông, Mật Tông, Phật giáo Nguyên Thủy, Phật giáo Đại Thừa, Kim Cương Thừa).")
            title = meta["title"]
            short = meta.get("short") or re.sub(r"^[^\w]+|[^\w)\]\"”]+$", "", title, flags=re.U).strip() or title
            rel_url, rel_text = None, None
            if meta.get("related"):
                bits = [b.strip() for b in meta["related"].split("|", 1)]
                rel_url = bits[0]; rel_text = bits[1] if len(bits) > 1 and bits[1] else title
            body = parse_body(parts[1])
            first_p = next((v for k, v in body if k == "p"), "")
            posts.append(dict(type=ptype, cat=cat, title=title, short=short, dt=dt, has_time=has_time, slug=slug, file=fname,
                              image=meta.get("image"), alt=meta.get("alt") or short, source=meta.get("source"),
                              summary=meta.get("summary") or first_p[:160], signoff=meta.get("signoff"), tags=meta.get("tags"),
                              related=(rel_url, rel_text), body=body, path=path))
    posts.sort(key=lambda p: (p["dt"], p["title"]), reverse=True)
    return posts

# ---------------- Ảnh ----------------
def process_image(p):
    p["img"] = p["og"] = p["size"] = None
    if not p["image"]: return
    src = _os.path.join(CONTENT, "images", p["image"])
    if not _os.path.isfile(src):
        warn(p["path"], f"không thấy ảnh '{p['image']}' trong content/images/. Bài sẽ dùng khung ảnh trang trí."); return
    from PIL import Image
    im = Image.open(src).convert("RGB")
    w = min(900, im.width); h = round(im.height * w / im.width)
    out = _os.path.join(OUT, "images"); _os.makedirs(out, exist_ok=True)
    main_rel, og_rel = f"images/{p['slug']}.jpg", f"images/{p['slug']}-og.jpg"
    if _os.path.abspath(src) != _os.path.abspath(_os.path.join(OUT, main_rel)):
        im.resize((w, h), Image.LANCZOS).save(_os.path.join(OUT, main_rel), quality=82, optimize=True, progressive=True)
    og_src = _os.path.join(CONTENT, "images", _os.path.splitext(p["image"])[0] + "-og.jpg")
    if _os.path.isfile(og_src):
        if _os.path.abspath(og_src) != _os.path.abspath(_os.path.join(OUT, og_rel)): shutil.copyfile(og_src, _os.path.join(OUT, og_rel))
    else:
        cw, ch = im.width, round(im.width * 630 / 1200)
        im.crop((0, 0, cw, min(ch, im.height))).resize((1200, 630), Image.LANCZOS).save(_os.path.join(OUT, og_rel), quality=82, optimize=True)
    p["img"], p["og"], p["size"] = main_rel, og_rel, (w, h)

# =====================================================================
#  TẠO TRANG
# =====================================================================
def fmt_date(p):
    d = p["dt"]
    s = f"{d.day:02d}/{d.month:02d}/{d.year}"
    return s + (f" lúc {d.hour:02d}:{d.minute:02d}" if p["has_time"] else "")

def real_card(p):
    s = SECTIONS[p["type"]]
    return f'''    <a class="feature link" href="{p["file"]}" style="--accent:{s["accent"]}" data-title="{html.escape(p["short"].lower())}"><span class="tag">{s["tag"]}</span>
      <div class="badge">{icon(PH_ICON[p["type"]] if p["type"] != "bai-viet" else "bai-viet")}</div>
      <h3>{html.escape(p["short"])}</h3><p>{html.escape(p["summary"])}</p></a>
'''

def sample_card(key, s, item):
    t, d = item
    return f'''    <article class="feature" style="--accent:{s["accent"]}" data-title="{html.escape(t.lower())}"><span class="tag">{s["tag"]} · Mẫu</span>
      <div class="badge">{icon(PH_ICON[key])}</div>
      <h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>
'''

def post_page(p):
    t = p["type"]; s = SECTIONS[t]
    if p["img"]:
        wd, ht = p["size"]
        cover = f'<figure class="post-cover"><img src="{p["img"]}" alt="{html.escape(p["alt"])}" width="{wd}" height="{ht}" decoding="async"></figure>'
    else:
        cover = f'<figure class="post-cover ph" style="--accent:{s["accent"]}"><div class="ph-art">{icon(PH_ICON[t])}</div></figure>'
    # nội dung
    heads = [v for k, v in p["body"] if k == "h2"]
    toc = ""
    if len(heads) >= 3:
        toc = '<nav class="toc" aria-label="Mục lục">' + "".join(f'<a href="#muc-{i}">{html.escape(h)}</a>' for i, h in enumerate(heads)) + "</nav>"
    out, sec_open, si, recipe = [], False, -1, False
    for kind, val in p["body"]:
        if kind == "h2":
            if sec_open: out.append("</section>")
            si += 1; hf = fold(val)
            recipe = hf.startswith("nguyenlieu") or hf.startswith("cachlam")
            out.append(f'<section class="{"recipe-block" if recipe else "kinh-sec"}" id="muc-{si}"><h2>{html.escape(val)}</h2>'); sec_open = True
        elif kind == "p": out.append(f"<p>{html.escape(val)}</p>")
        elif kind == "verse": out.append('<p class="verse">' + "<br>\n".join(html.escape(x) for x in val) + "</p>")
        elif kind == "ul": out.append(f'<ul class="{"ingredients" if recipe else "chant"}">' + "".join(f"<li>{html.escape(x)}</li>" for x in val) + "</ul>")
        elif kind == "ol": out.append('<ol class="steps">' + "".join(f"<li>{html.escape(x)}</li>" for x in val) + "</ol>")
    if sec_open: out.append("</section>")
    prose = "\n".join(out)
    eyebrow = LABEL[t] + (" · " + next(c[1] for c in CATS if c[0] == p["cat"]) if p["cat"] else "")
    intro = ""
    if t == "mon-chay" and p["summary"]: intro = f'<p class="lede">{html.escape(p["summary"])}</p>'
    elif t in ("kinh-ke", "cau-nguyen") and p["summary"]: intro = f'<p class="summary">{html.escape(p["summary"])}</p>'
    extra_end = ""
    if p["signoff"]: extra_end += f'<p class="signoff">{html.escape(p["signoff"])}</p>\n'
    if p["tags"]: extra_end += f'<p class="hashtags">{html.escape(p["tags"])}</p>\n'
    if p["source"]: extra_end += f'<p class="source">Nguồn: {html.escape(p["source"])}</p>\n'
    if p["related"][0]:
        extra_end += f'''<aside class="related"><h2>Bài liên quan</h2><a class="related-link" href="{html.escape(p["related"][0])}" target="_blank" rel="noopener noreferrer">{html.escape(p["related"][1])} <span aria-hidden="true">↗</span></a></aside>\n'''
    iso = p["dt"].strftime("%Y-%m-%d")
    body = f"""
  <p class="crumb"><a href="{s["file"]}">← {LABEL[t]}</a></p>
  <article class="post">
    {cover}
    <div class="post-body">
      <div class="eyebrow">{html.escape(eyebrow)}</div>
      <h1>{html.escape(p["title"])}</h1>
      {intro}
      {toc}
      <div class="prose">
{prose}
      </div>
{extra_end}{post_footer(iso, fmt_date(p))}    </div>
  </article>
"""
    if p["og"]:
        og = (f'<meta property="og:type" content="article">\n<meta property="og:title" content="{html.escape(p["short"])} · Lạy Phật">\n'
              f'<meta property="og:description" content="{html.escape(p["summary"][:160])}">\n<meta property="og:image" content="{SITE}/{p["og"]}">\n'
              f'<meta property="og:url" content="{SITE}/{p["file"]}">\n<meta name="twitter:card" content="summary_large_image">\n')
    else:
        og = ""
    return head(p["short"] + " · Lạy Phật", p["summary"][:160], s["file"], og) + body + FOOT

def list_page(title, eyebrow, lede, posts, key, active, extra_top="", extra_bottom=""):
    s = SECTIONS[key]
    cap = 9 if key == "bai-viet" else 6
    posts = posts[:cap]
    cards = "".join(real_card(p) for p in posts)
    n_sample = 0
    if key and len(posts) < cap:
        fill = SAMPLES[key][: cap - len(posts)]
        cards += "".join(sample_card(key, s, it) for it in fill); n_sample = len(fill)
    note = '<p class="note">Các thẻ có nhãn "Mẫu" chỉ để giữ bố cục, sẽ tự biến mất khi có đủ bài thật.</p>' if n_sample else ""
    empty = '<p class="empty-note">Chưa có bài viết trong danh mục này. Bài mới sẽ xuất hiện ở đây.</p>' if (not posts and not n_sample) else ""
    body = f'''
  <section class="page-hero">
    <div class="eyebrow">{html.escape(eyebrow)}</div>
    <h1>{html.escape(title)}</h1>
    <p class="lede">{html.escape(lede)}</p>
    <div class="filter"><input id="filter" placeholder="Lọc trong chuyên mục..." aria-label="Lọc"></div>
  </section>
{extra_top}  <div class="grid" id="list">
{cards}  </div>
  {empty}{note}
{extra_bottom}'''
    return head(title + " · Lạy Phật", lede, active) + body + FOOT

def cat_grid(posts):
    latest = {}
    for p in posts:
        if p["type"] == "bai-viet" and p["cat"] and p["cat"] not in latest: latest[p["cat"]] = p
    cards = ""
    for slug, name, ic, color, desc in CATS:
        p = latest.get(slug)
        if p:
            title = f'<p class="cat-title">{html.escape(p["short"])}</p>'
            summ = f'<p class="cat-sum">{html.escape(p["summary"])}</p>'
        else:
            title = '<p class="cat-title empty">Chưa có bài viết</p>'
            summ = '<p class="cat-sum empty">Bài viết mới nhất của danh mục này sẽ hiển thị tại đây.</p>'
        cards += f'''    <a class="cat-card" href="danh-muc-{slug}.html" style="--accent:{color}">
      <div class="cat-head"><span class="cat-ico">{icon(ic)}</span><h3>{html.escape(name)}</h3></div>
      {title}
      {summ}
    </a>
'''
    return f'''  <section class="cat-zone">
    <div class="section-head"><h2>Danh mục</h2><span>6 danh mục</span></div>
    <div class="cat-grid">
{cards}    </div>
  </section>
'''

def category_page(slug, name, ic, color, desc, posts):
    mine = [p for p in posts if p["type"] == "bai-viet" and p["cat"] == slug]
    cards = "".join(real_card(p) for p in mine)
    empty = '<p class="empty-note">Chưa có bài viết trong danh mục này. Bài mới sẽ xuất hiện ở đây.</p>' if not mine else ""
    body = f'''
  <p class="crumb"><a href="bai-viet.html">← Bài viết Phật giáo</a></p>
  <section class="page-hero">
    <div class="eyebrow">Danh mục</div>
    <h1 class="cat-h1"><span class="cat-ico big" style="--accent:{color}">{icon(ic)}</span>{html.escape(name)}</h1>
    <p class="lede">{html.escape(desc)}</p>
  </section>
  <div class="grid" id="list">
{cards}  </div>
  {empty}
'''
    return head(name + " · Lạy Phật", desc, "bai-viet.html") + body + FOOT

def index_page(posts):
    counts = {k: sum(1 for p in posts if p["type"] == k) for k in SECTIONS}
    cards = ""
    for k, s in SECTIONS.items():
        n = counts[k]
        cards += f'''    <a class="feature link" href="{s["file"]}" style="--accent:{s["accent"]}"><span class="tag">{f"{n} bài" if n else "Sắp có bài"}</span>
      <div class="badge">{icon(PH_ICON[k] if k != "bai-viet" else "bai-viet")}</div>
      <h3>{s["title"]}</h3><p>{html.escape(s["lede"])}</p></a>
'''
    body = f'''
  <section class="hero">
    <div class="hero-grid">
      <div>
        <div class="eyebrow">Bài viết · Kinh kệ · Cầu nguyện · Món chay</div>
        <h1>Một chốn <em>an yên</em> cho tâm hồn.</h1>
        <p class="lede">Nơi chia sẻ những bài viết về Phật giáo, kinh kệ, lời chúc, lời cầu nguyện và món chay thanh đạm, trình bày rõ ràng, dễ đọc mỗi ngày.</p>
        <div class="hero-stats">
          <div class="hero-stat"><b>4</b><span>chuyên mục</span></div>
          <div class="hero-stat"><b>{len(posts)}</b><span>bài đã đăng</span></div>
          <div class="hero-stat"><b>VI</b><span>tiếng Việt</span></div>
        </div>
      </div>
      <div class="wheel-box">
        {WHEEL}
      </div>
    </div>
    <form class="card search-card" onsubmit="return false">
      <h2>Tìm bài viết</h2>
      <p class="sub">Nhập từ khóa để tìm trong các chuyên mục (tính năng tìm kiếm sẽ được nối với dữ liệu thật ở bước sau).</p>
      <div class="field-row one">
        <div class="field"><label>Từ khóa</label><input id="q" placeholder="Ví dụ: thiền, Vu Lan, đậu hũ..." /></div>
      </div>
      <div class="cta-row"><button class="btn-primary" type="button" id="go">Tìm kiếm</button><span class="cta-note">Miễn phí · Không cần đăng nhập</span></div>
    </form>
    <div class="quote-strip"><span>“Nội dung trích dẫn sẽ được thay bằng lời dạy có nguồn rõ ràng.”</span><span class="mark">— Ô mẫu</span></div>
  </section>
  <section class="section-head"><h2>Các chuyên mục</h2><span>4 chuyên mục</span></section>
  <div class="grid four">
{cards}  </div>
'''
    return head("Lạy Phật", "Trang chia sẻ bài viết Phật giáo, kinh kệ, lời chúc cầu nguyện và món chay.", "index.html") + body + FOOT

def write(name, content):
    open(_os.path.join(OUT, name), "w", encoding="utf-8").write(content)

def main():
    _os.makedirs(OUT, exist_ok=True)
    posts = load_posts()
    for p in posts: process_image(p)
    write("index.html", index_page(posts))
    for key, s in SECTIONS.items():
        mine = [p for p in posts if p["type"] == key]
        top = '  <section class="section-head tight"><h2>Tất cả bài viết</h2><span>9 bài mới nhất</span></section>\n' if key == "bai-viet" else ""
        bottom = cat_grid(posts) if key == "bai-viet" else ""
        write(s["file"], list_page(s["title"], "Chuyên mục", s["lede"], mine, key, s["file"], extra_top=top, extra_bottom=bottom))
    for c in CATS:
        write(f"danh-muc-{c[0]}.html", category_page(*c, posts))
    for p in posts:
        write(p["file"], post_page(p))
    print(f"Đã tạo {len(posts)} bài, {len(WARNINGS)} cảnh báo.")

if __name__ == "__main__":
    main()
