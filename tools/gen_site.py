import os, html
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
}

SECTIONS = {
 "bai-viet": dict(file="bai-viet.html", title="Bài viết về Phật giáo", accent="var(--c1)", tag="Bài viết",
   lede="Những bài viết giới thiệu giáo lý, lịch sử và đời sống tu tập, trình bày rõ ràng, dễ đọc cho người mới bắt đầu.",
   items=[("Khổ đau và con đường để diệt trừ khổ","Đức Phật như vị thầy thuốc giỏi: biết bệnh, biết nguyên nhân, biết thuốc chữa và biết bệnh đã khỏi.","bai-viet-kho-dau-diet-kho.html"),
          ("Bát chánh đạo","Con đường tám nhánh hướng đến an lạc và giải thoát."),
          ("Ngũ giới cho người tại gia","Năm điều học giúp đời sống thanh tịnh, hài hòa."),
          ("Từ, bi, hỷ, xả","Bốn tâm vô lượng và cách vun trồng trong đời thường."),
          ("Thiền cho người mới bắt đầu","Những bước đầu tiên để ngồi thiền và quan sát hơi thở."),
          ("Ý nghĩa ngày rằm và mùng một","Vì sao nhiều người đi chùa, ăn chay vào những ngày này.")]),
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
      <span class="copyright">© 2024 - <span class="yr">2026</span> Bản quyền thuộc <a class="fb-link" href="https://facebook.com/layphatvn" target="_blank" rel="noopener noreferrer"><svg class="fb-ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M22 12a10 10 0 10-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0022 12z"/></svg>Lạy Phật</a></span>
      <span class="dim" aria-hidden="true">Nam mô A Di Đà Phật</span>
    </div>
  </footer>
</div>
<script src="app.js"></script>
</body>
</html>
'''

def card(key, s, item):
    t, d = item[0], item[1]
    href = item[2] if len(item) > 2 else None
    if href:
        return f'''    <a class="feature link" href="{href}" style="--accent:{s["accent"]}" data-title="{html.escape(t.lower())}"><span class="tag">{s["tag"]}</span>
      <div class="badge">{icon(key)}</div>
      <h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></a>
'''
    return f'''    <article class="feature" style="--accent:{s["accent"]}" data-title="{html.escape(t.lower())}"><span class="tag">{s["tag"]} · Mẫu</span>
      <div class="badge">{icon(key)}</div>
      <h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></article>
'''


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

def index():
    wheel = '<g stroke="#dcae67" stroke-width=".8" opacity=".5">' + "".join(
      f'<line x1="200" y1="200" x2="{x}" y2="{y}"/>' for x,y in
      [(350,200),(306,94),(200,50),(94,94),(50,200),(94,306),(200,350),(306,306)]) + '</g>'
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x,y,r,c in
      [(350,200,3.6,"#f1d49c"),(306,94,3.4,"#a78bfa"),(200,50,4.5,"#f1d49c"),(94,94,3.4,"#f2989a"),(50,200,3.6,"#f1d49c"),(94,306,3.4,"#5fd6ae"),(200,350,4.5,"#f1d49c"),(306,306,3.4,"#7cd0f2")])
    cards = ""
    for k,s in SECTIONS.items():
        cards += f'''    <a class="feature link" href="{s["file"]}" style="--accent:{s["accent"]}"><span class="tag">{len(s["items"])} bài</span>
      <div class="badge">{icon(k)}</div>
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
          <div class="hero-stat"><b>24</b><span>bài mẫu ban đầu</span></div>
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

def section(key, s):
    cards = "".join(card(key, s, it) for it in s["items"])
    body = f'''
  <section class="page-hero">
    <div class="eyebrow">Chuyên mục</div>
    <h1>{s["title"]}</h1>
    <p class="lede">{html.escape(s["lede"])}</p>
    <div class="filter"><input id="filter" placeholder="Lọc trong chuyên mục..." aria-label="Lọc"></div>
  </section>
  <div class="grid" id="list">
{cards}  </div>
  <p class="note">Đây là các thẻ mẫu để dựng khung giao diện. Nội dung thật sẽ được bổ sung sau.</p>
'''
    return head(s["title"]+" · Lạy Phật", s["lede"], s["file"]) + body + FOOT


def post_footer(date_iso):
    y,m,d = date_iso.split("-")
    return f"""
      <footer class="post-end">
        <p class="post-date">Đăng ngày <time datetime="{date_iso}">{d}/{m}/{y}</time></p>
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

# ---------------- Bài viết chi tiết ----------------
SITE = "https://layphatvn.web.app"
ARTICLE = dict(
  file="bai-viet-kho-dau-diet-kho.html", date="2026-10-01",
  title="🌸 KHỔ ĐAU VÀ CON ĐƯỜNG ĐỂ DIỆT TRỪ KHỔ 🌸",
  plain="Khổ đau và con đường để diệt trừ khổ",
  img="images/kho-dau-diet-kho.jpg", og="images/kho-dau-diet-kho-og.jpg",
  alt="Tượng Phật bằng đá trắng dưới ánh nắng xuyên qua tán lá, hai bàn tay ngửa mở ra",
  paras=[
    "🌿 Tại tịnh xá, Đức Phật ôn tồn nhìn chư Tăng rồi đặt một câu hỏi: \"Này các Tỳ-kheo, vị bác sĩ giỏi là vị bác sĩ thế nào?\".",
    "Một đệ tử liền chắp tay bạch: \"Bạch Đức Thế Tôn, là người biết rõ bệnh, biết nguyên nhân gây bệnh, biết phương thuốc chữa và biết bệnh đã chữa khỏi hẳn\".",
    "Đức Phật gật đầu khen ngợi: \"Đúng vậy. Như Lai cũng như thế: Biết rõ Khổ, biết Nguyên nhân của khổ, biết Sự chấm dứt khổ và chỉ ra Con đường dẫn đến hết khổ\".",
    "Lời so sánh giản dị mà sâu sắc ấy đã giúp các đệ tử thấu hiểu sứ mệnh cứu độ chúng sinh cao cả của bậc Đạo sư.",
    "🌿 Ví như vị Y vương đại tài, Đức Phật không chỉ chẩn đoán căn bệnh khổ đau phiền não của kiếp người mà còn chỉ dạy phương thuốc điều trị triệt để.",
    "Tứ Diệu Đế giúp chỉ rõ thực trạng Khổ đau, vạch ra Nguyên nhân khổ do tham sân si và chỉ dạy Con đường thực hành Bát Chánh Đạo để diệt khổ.",
    "Mọi nỗi đau trong cuộc đời đều có thể được chữa lành nhờ ánh sáng trí tuệ của việc thực hành Bát Chánh Đạo.",
    "🌿 Mỗi chúng ta hãy chủ động làm vị bác sĩ cho chính tâm trí mình. Thay vì trốn chạy hay oán trách nghịch cảnh, hãy dũng cảm quay về nhận diện Tứ Diệu Đế và kiên trì thực hành Bát Chánh Đạo qua từng suy nghĩ, lời nói, hành động.",
    "Việc siêng năng tu tập Chánh kiến, Chánh niệm và Chánh định mỗi ngày sẽ giúp ta loại bỏ gốc rễ mầm mống của khổ đau, nuôi dưỡng sự bình an nội tại và tiến tới giác ngộ giải thoát trọn vẹn!",
  ],
  signoff="❤️ Trang Lạy Phật: Lan tỏa Từ Bi - Sống đời Tỉnh Thức ❤️",
  tags="#PhatPhap #Buddhism #Compassion #Mindfulness #Awakening #佛教教義 #仏教の教え #불교가르침 #EnseignementsBouddhistes",
  related="https://www.facebook.com/share/p/1JouUGk8Em/",
)

def article_page():
    a = ARTICLE
    og = (f'<meta property="og:type" content="article">\n<meta property="og:title" content="{html.escape(a["plain"])} · Lạy Phật">\n'
          f'<meta property="og:description" content="{html.escape(a["paras"][0][:160])}">\n'
          f'<meta property="og:image" content="{SITE}/{a["og"]}">\n<meta property="og:url" content="{SITE}/{a["file"]}">\n'
          f'<meta name="twitter:card" content="summary_large_image">\n')
    paras = "".join(f"<p>{html.escape(x)}</p>\n" for x in a["paras"])
    body = f"""
  <p class="crumb"><a href="bai-viet.html">← Bài viết Phật giáo</a></p>
  <article class="post">
    <figure class="post-cover"><img src="{a["img"]}" alt="{html.escape(a["alt"])}" width="900" height="1348" decoding="async"></figure>
    <div class="post-body">
      <div class="eyebrow">Bài viết Phật giáo</div>
      <h1>{html.escape(a["title"])}</h1>
      <div class="prose">
{paras}      </div>
      <p class="signoff">{html.escape(a["signoff"])}</p>
      <p class="hashtags">{html.escape(a["tags"])}</p>
      <aside class="related">
        <h2>Bài liên quan</h2>
        <a class="related-link" href="{a["related"]}" target="_blank" rel="noopener noreferrer">{html.escape(a["title"])} <span aria-hidden="true">↗</span></a>
      </aside>
{post_footer(a["date"])}    </div>
  </article>
"""
    return head(a["plain"]+" · Lạy Phật", a["paras"][0][:160], "bai-viet.html", og) + body + FOOT


# ---------------- Trang Món chay ----------------
def placeholder_cover(key, accent):
    return f'<figure class="post-cover ph" style="--accent:{accent}"><div class="ph-art">{icon(key)}</div></figure>'

RECIPE = dict(
  file="mon-chay-tom-dau-hu-kho-ca-chua.html", date="2026-10-01", title="Tôm đậu hũ kho cà chua",
  intro="Món kho đậm đà, dễ nấu, hợp cho bữa cơm chay gia đình.",
  ingredients=["1 bịch tôm chay","4 miếng đậu hũ chiên sẵn (cắt khối)","3 trái cà chua (cắt hạt lựu)","2 - 3 muỗng dầu hào","Dầu ăn","Mè"],
  steps=["Cho dầu ăn vào xào mềm cà chua.","Sau đó cho dầu hào vào đảo đều.","Thêm tôm và đậu hũ vào. Đậy nắp kho chừng 10 phút. Nếu bạn thích sốt sệt nước thì thêm nước.","Rắc mè và thưởng thức."],
  source="Sưu tầm", img=None,
)
def recipe_page():
    r=RECIPE; s=SECTIONS["mon-chay"]
    cover = f'<figure class="post-cover"><img src="{r["img"]}" alt="{html.escape(r["title"])}" decoding="async"></figure>' if r["img"] else placeholder_cover("mon-chay", s["accent"])
    ing="".join(f"<li>{html.escape(x)}</li>" for x in r["ingredients"])
    stp="".join(f"<li>{html.escape(x)}</li>" for x in r["steps"])
    body=f"""
  <p class="crumb"><a href="mon-chay.html">← Món chay</a></p>
  <article class="post">
    {cover}
    <div class="post-body">
      <div class="eyebrow">Món chay</div>
      <h1>{html.escape(r["title"])}</h1>
      <p class="lede">{html.escape(r["intro"])}</p>
      <section class="recipe-block"><h2>Nguyên liệu</h2><ul class="ingredients">{ing}</ul></section>
      <section class="recipe-block"><h2>Cách làm</h2><ol class="steps">{stp}</ol></section>
      <p class="source">Nguồn: {html.escape(r["source"])}</p>
{post_footer(r["date"])}    </div>
  </article>
"""
    return head(r["title"]+" · Món chay · Lạy Phật", r["intro"], "mon-chay.html") + body + FOOT

# ---------------- Trang Kinh Nhật tụng ----------------
KINH = dict(
  file="kinh-nhat-tung.html", date="2026-10-01", title="Kinh Nhật tụng",
  summary="Đây là nghi thức niệm phật hàng ngày. Y phục ngay thẳng đứng hướng về bàn thờ Phật. Nếu nhà không có nơi thờ phượng có thể xoay mặt về hướng Tây (hướng mặt trời lặn).",
  sections=[
    ("1. ĐẢNH LỄ", [("p","Chí tâm đảnh lễ: Nam mô tận hư không biến pháp giới quá, hiện, vị lai thập phương chư Phật, Tôn Pháp Hiền Thánh Tăng thường trụ Tam Bảo. (1 lạy)"),
                    ("p","Chí tâm đảnh lễ: Nam mô Ta Bà Giáo Chủ Bổn Sư Thích Ca Mâu Ni Phật, Đương Lai Hạ Sanh Di Lặc Tôn Phật, Đại Trí Văn Thù Sư Lợi Bồ Tát, Đại Hạnh Phổ Hiền Bồ Tát, Hộ Pháp Chư Tôn Bồ Tát, Linh Sơn Hội Thượng Phật Bồ Tát. (1 lạy)"),
                    ("p","Chí tâm đảnh lễ: Nam mô Tây Phương Cực Lạc Thế Giới Đại Từ Đại Bi A Di Đà Phật, Đại Bi Quán Thế Âm Bồ Tát, Đại Thế Chí Bồ Tát, Đại Nguyện Địa Tạng Vương Bồ Tát, Thanh Tịnh Đại Hải Chúng Bồ Tát. (1 lạy)")]),
    ("2. TÁN PHẬT", [("verse",["Phật A Di Đà thân kim sắc","Tướng tốt quang minh tự trang nghiêm","Năm Tu Di uyển chuyển bạch hào","Bốn biển lớn trong ngần mắt biếc","Trong hào quang hóa vô số Phật","Vô số Bồ Tát hiện ở trong","Bốn mươi tám nguyện độ chúng sanh","Chín phẩm sen vàng lên giải thoát"]),
                     ("p","Nam-mô Tây phương Cực lạc thế giới đại từ đại bi A Di Đà Phật.")]),
    ("3. NIỆM PHẬT", [("lines",["Nam-mô A Di Đà Phật hoặc A Di Đà Phật (Tùy niệm càng nhiều càng tốt)","Nam-mô Quán Thế Âm Bồ Tát (3 lần)","Nam-mô Đại Thế Chí Bồ Tát (3 lần)","Nam-mô Địa Tạng Vương Bồ Tát (3 lần)","Nam-mô Thanh Tịnh Đại Hải Chúng Bồ Tát (3 lần)"])]),
    ("4. SÁM HỐI", [("verse",["Con xưa đã tạo bao ác nghiệp","Đều do vô thủy tham sân si","Bởi thân khẩu ý phát sinh ra","Hết thảy con nay nguyện sám hối. (3 lần)"]),
                    ("p","Rồi đứng lên lạy xuống, thường thường là 108 lạy hoặc càng nhiều càng tốt, nếu bận bịu công việc thì có thể lạy ít nhất là 50 lạy.")]),
    ("5. PHÁT NGUYỆN", [("verse",["Nguyện sanh Tịnh Độ ở Tây Phương","Chín phẩm hoa sen là cha mẹ","Hoa nở thấy Phật chứng vô sanh","Bồ Tát bất thối là bạn lữ."])]),
    ("6. TAM TỰ QUY Y", [("p","Tự quy y Phật. Nguyện cho chúng sanh hiểu sâu đạo cả, phát tâm vô thượng.(1 lạy)"),
                         ("p","Tự quy y Pháp. Nguyện cho chúng sanh thấu rõ kinh tạng, trí tuệ như biển.(1 lạy)"),
                         ("p","Tự quy y Tăng. Nguyện cho chúng sanh tâm ý hòa hợp, biết thương mến nhau.(1 lạy)")]),
    ("7. HỒI HƯỚNG", [("verse",["Nguyện đem công đức này","Trang nghiêm Phật Tịnh Độ","Trên đền bốn ân nặng","Dưới cứu khổ ba đường","Nếu có ai thấy nghe","Đều phát lòng bồ đề","Hết một báo thân này","Đồng sanh cõi Cực Lạc."])]),
    ("LỜI DẶN THÊM", [("p","A Di Đà Phật. Mọi người nếu bận rộn có ít thời gian niệm Phật thì nên áp dụng phương pháp niệm 10 danh hiệu A Di Đà Phật này, lợi ích nhất vẫn là buổi tối khi kết thúc mọi việc nên làm theo nghi thức ở trên."),
                      ("p","Phương pháp niệm 10 danh hiệu A-Di-Đà Phật là phương pháp đơn giản, lợi ích thiết thực trong việc hành trì pháp môn niệm Phật. Đặc biệt thích hợp với những người ít có thời gian tu tập. Hành trì theo phương pháp này sẽ giúp cho chúng ta nhất tâm chánh niệm A-Di-Đà Phật và giúp cho chúng ta an lạc thanh thản ngay trong giây phút hiện tại."),
                      ("p","Thời khóa hành trì được bắt đầu khi chúng ta thức giấc vào sáng sớm. Chúng ta ngồi thẳng người và niệm rõ ràng danh hiệu A-Di-Đà Phật 10 lần với tâm chánh niệm, niệm lớn tiếng hay niệm thầm tùy theo ý muốn từng người. Chúng ta lặp lại công phu này 8 lần nữa trong một ngày. Như vậy, chúng ta công phu theo phương pháp nầy 9 lần trong mỗi ngày. Thời gian tùy ta sắp xếp sao cho phù hợp."),
                      ("p","Quan trọng nhất là hành trì đều đặn. Sự gián đoạn, không kiên nhẫn khi hành trì sẽ làm giảm hiệu lực tác dụng. Nếu hành trì liên tục, tinh cần thì người tu sẽ thấy càng ngày thân tâm càng gia tăng niềm an lạc."),
                      ("p","Tinh tấn hành trì phương pháp niệm 10 danh hiệu A-Di-Đà Phật kết hợp với niềm tin và bản nguyện chân chính không thay đổi, chắc chắn bảo đảm tâm nguyện vãng sinh cõi Tây phương Cực Lạc, cõi Vô lượng thọ, Vô lượng quang sẽ được thành tựu.")]),
  ],
  source="Sưu tầm", img=None,
)
def kinh_page():
    k=KINH; s=SECTIONS["kinh-ke"]
    cover = f'<figure class="post-cover"><img src="{k["img"]}" alt="{html.escape(k["title"])}" decoding="async"></figure>' if k["img"] else placeholder_cover("cau-nguyen", s["accent"])
    toc="".join(f'<a href="#muc-{i}">{html.escape(h)}</a>' for i,(h,_) in enumerate(k["sections"]))
    secs=""
    for i,(h,blocks) in enumerate(k["sections"]):
        inner=""
        for kind,val in blocks:
            if kind=="p": inner+=f"<p>{html.escape(val)}</p>\n"
            elif kind=="lines": inner+='<ul class="chant">'+"".join(f"<li>{html.escape(x)}</li>" for x in val)+"</ul>\n"
            else: inner+='<p class="verse">'+"<br>\n".join(html.escape(x) for x in val)+"</p>\n"
        secs+=f'<section class="kinh-sec" id="muc-{i}"><h2>{html.escape(h)}</h2>\n{inner}</section>\n'
    body=f"""
  <p class="crumb"><a href="kinh-ke.html">← Bài kinh - kệ</a></p>
  <article class="post">
    {cover}
    <div class="post-body">
      <div class="eyebrow">Bài kinh - kệ</div>
      <h1>{html.escape(k["title"])}</h1>
      <p class="summary">{html.escape(k["summary"])}</p>
      <nav class="toc" aria-label="Mục lục">{toc}</nav>
      <div class="prose kinh">
{secs}      </div>
      <p class="source">Nguồn: {html.escape(k["source"])}</p>
{post_footer(k["date"])}    </div>
  </article>
"""
    return head(k["title"]+" · Lạy Phật", k["summary"], "kinh-ke.html") + body + FOOT

os.makedirs(OUT, exist_ok=True)
open(f"{OUT}/index.html","w",encoding="utf-8").write(index())
for k,s in SECTIONS.items():
    open(f"{OUT}/{s['file']}","w",encoding="utf-8").write(section(k,s))
open(f"{OUT}/{ARTICLE['file']}","w",encoding="utf-8").write(article_page())
open(f"{OUT}/{RECIPE['file']}","w",encoding="utf-8").write(recipe_page())
open(f"{OUT}/{KINH['file']}","w",encoding="utf-8").write(kinh_page())
print("ok")
