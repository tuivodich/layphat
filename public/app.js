// Bánh xe Pháp luân: 3 lớp quay ngược chiều nhau, chậm khi bình thường, nhanh khi rê chuột
(function () {
  var box = document.querySelector('.wheel-box');
  if (box) {
    var layers = [
      { el: document.getElementById('w1'), dir: 1,  base: 6,  a: 0 },
      { el: document.getElementById('w2'), dir: -1, base: 10, a: 0 },
      { el: document.getElementById('w3'), dir: 1,  base: 15, a: 0 }
    ];
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    // Luôn quay rất chậm khi bình thường; nếu hệ điều hành bật "giảm chuyển động" thì quay chậm hơn nữa
    var IDLE = reduce ? 0.5 : 1, FAST = reduce ? 6 : 10, factor = IDLE, target = IDLE, last = null;
    var fast = function () { target = FAST; }, slow = function () { target = IDLE; };
    box.addEventListener('mouseenter', fast);
    box.addEventListener('mouseleave', slow);
    box.addEventListener('touchstart', fast, { passive: true });
    box.addEventListener('touchend', slow);
    box.addEventListener('touchcancel', slow);
    function tick(t) {
      if (last === null) last = t;
      var dt = Math.min((t - last) / 1000, 0.1); last = t;
      factor += (target - factor) * Math.min(dt * 3, 1); // tăng/giảm tốc mượt
      layers.forEach(function (L) {
        if (!L.el) return;
        L.a = (L.a + L.dir * L.base * factor * dt) % 360;
        L.el.setAttribute('transform', 'rotate(' + L.a.toFixed(2) + ' 200 200)');
      });
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // Câu trích dẫn ngẫu nhiên (dữ liệu từ content/quote.txt, nhúng sẵn trong trang)
  var qBox = document.getElementById('quote'), qData = document.getElementById('quote-data');
  if (qBox && qData) {
    try {
      var qs = JSON.parse(qData.textContent);
      if (qs.length > 1) {
        var q = qs[Math.floor(Math.random() * qs.length)];
        var bq = qBox.querySelector('blockquote'), cap = qBox.querySelector('figcaption');
        bq.textContent = q.text;
        if (q.author) { cap.textContent = '— ' + q.author; cap.hidden = false; } else { cap.hidden = true; }
      }
    } catch (e) { /* giữ câu mặc định */ }
  }

  // Năm hiện tại ở chân trang
  var y = new Date().getFullYear();
  document.querySelectorAll('.yr').forEach(function (el) { el.textContent = y; });
  // Ngày và đồng hồ ở trang chủ (giờ của thiết bị người xem), định dạng dd/mm/yyyy và hh:mm:ss
  var dEl = document.getElementById('hs-date'), cEl = document.getElementById('hs-clock');
  if (dEl && cEl) {
    var p2 = function (n) { return (n < 10 ? '0' : '') + n; };
    var tick = function () {
      var n = new Date();
      dEl.textContent = p2(n.getDate()) + '/' + p2(n.getMonth() + 1) + '/' + n.getFullYear();
      cEl.textContent = p2(n.getHours()) + ':' + p2(n.getMinutes()) + ':' + p2(n.getSeconds());
    };
    tick(); setInterval(tick, 1000);
  }

  // Bỏ dấu, chữ thường, ký tự lạ -> khoảng trắng (tìm có dấu hay không dấu đều được)
  function plain(s) {
    return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'd').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }

  // Lọc thẻ trong trang chuyên mục
  var f = document.getElementById('filter');
  if (f) {
    var cards = document.querySelectorAll('#list .feature');
    f.addEventListener('input', function () {
      var q = f.value.trim().toLowerCase();
      var toks = plain(q).split(' ').filter(Boolean);
      cards.forEach(function (c) {
        var hay = c.dataset.search || plain(c.dataset.title || '');
        c.hidden = !toks.every(function (t) { return hay.indexOf(t) !== -1; });
      });
    });
  }
  // Ô tìm kiếm trang chủ: tạm chuyển đến trang bài viết
  var go = document.getElementById('go');
  var qIn = document.getElementById('q'), resBox = document.getElementById('search-results'), sData = document.getElementById('search-data');
  if (go && qIn && resBox && sData) {
    var items = [];
    try { items = JSON.parse(sData.textContent); } catch (e) {}
    var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
    var run = function () {
      var toks = plain(qIn.value).split(' ').filter(Boolean);
      if (!toks.length) { resBox.innerHTML = ''; return; }
      var hits = items.filter(function (it) { return toks.every(function (t) { return it.k.indexOf(t) !== -1; }); });
      resBox.innerHTML = hits.length
        ? '<p class="sr-count">Tìm thấy ' + hits.length + ' bài</p>' + hits.map(function (it) {
            return '<div class="latest-row"><a class="latest-title" href="' + it.f + '">' + esc(it.t) + '</a><span class="latest-date">' + it.l + ' · ' + it.d + '</span></div>';
          }).join('')
        : '<p class="sr-count">Không tìm thấy bài nào phù hợp.</p>';
    };
    go.addEventListener('click', run);
    qIn.addEventListener('input', run);
    qIn.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); run(); } });
  }

  // ---------- Chức năng cuối bài viết: In / Tải / Chia sẻ ----------
  var actions = document.querySelector('.post-actions');
  if (actions) {
    var toast = document.querySelector('.toast');
    var toastTimer;
    var say = function (msg) {
      if (!toast) return;
      toast.textContent = msg; toast.classList.add('show');
      clearTimeout(toastTimer); toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 2200);
    };
    var saveBlob = function (blob, name) {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = name;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 4000);
    };
    var fileBase = function () {
      var seg = location.pathname.split('/').pop().replace(/\.html?$/, '');
      return seg || 'lay-phat';
    };
    var toDataUrl = function (src) {
      return fetch(src).then(function (r) { return r.blob(); }).then(function (b) {
        return new Promise(function (res, rej) { var fr = new FileReader(); fr.onload = function () { res(fr.result); }; fr.onerror = rej; fr.readAsDataURL(b); });
      });
    };
    // Tải trang: một file .html tự đủ (CSS + ảnh nhúng sẵn), mở được cả khi không có mạng
    var downloadPage = function () {
      say('Đang chuẩn bị tệp...');
      // Ưu tiên bản PDF dựng sẵn khi deploy; nếu chưa có thì tải bản .html tự đủ
      var pdfUrl = 'pdf/' + fileBase() + '.pdf';
      fetch(pdfUrl, { method: 'HEAD' }).then(function (r) {
        var ct = r.headers.get('content-type') || '';
        if (!r.ok || ct.indexOf('pdf') === -1) throw new Error('nopdf');
        var a = document.createElement('a'); a.href = pdfUrl; a.download = fileBase() + '.pdf';
        document.body.appendChild(a); a.click(); a.remove();
        say('Đã tải bản PDF');
      }).catch(downloadHtml);
    };
    var downloadHtml = function () {
      var origImgs = Array.prototype.slice.call(document.querySelectorAll('img'));
      var origLinks = Array.prototype.slice.call(document.querySelectorAll('a[href]'));
      Promise.all([
        fetch('style.css').then(function (r) { if (!r.ok) throw new Error('css'); return r.text(); }),
        Promise.all(origImgs.map(function (im) { return toDataUrl(im.currentSrc || im.src); }))
      ]).then(function (res) {
        var css = res[0].replace(/url\((['"]?)images\//g, 'url($1' + new URL('images/', location.href).href);
        var clone = document.documentElement.cloneNode(true);
        clone.querySelectorAll('script, .post-actions, .toast, link[rel="stylesheet"][href="style.css"], link[rel*="icon"], link[rel="apple-touch-icon"]').forEach(function (n) { n.remove(); });
        var st = document.createElement('style'); st.textContent = css; clone.querySelector('head').appendChild(st);
        clone.setAttribute('data-bg', 'none');
        clone.querySelectorAll('img').forEach(function (im, i) { im.setAttribute('src', res[1][i]); im.removeAttribute('srcset'); });
        clone.querySelectorAll('a[href]').forEach(function (a, i) { if (origLinks[i]) a.setAttribute('href', origLinks[i].href); });
        var html = '<!doctype html>\n' + clone.outerHTML;
        saveBlob(new Blob([html], { type: 'text/html;charset=utf-8' }), fileBase() + '.html');
        say('Đã tải trang về máy');
      }).catch(function () {
        // Dự phòng: tải nội dung bài dạng văn bản thuần
        var body = document.querySelector('.post-body');
        var txt = (body ? body.innerText : document.body.innerText) + '\n\n' + location.href + '\n';
        saveBlob(new Blob([txt], { type: 'text/plain;charset=utf-8' }), fileBase() + '.txt');
        say('Đã tải nội dung bài (văn bản)');
      });
    };
    // Chia sẻ
    var menu = document.querySelector('.share-menu');
    var shareBtn = document.querySelector('[data-act="share"]');
    var closeMenu = function () { if (menu) { menu.hidden = true; shareBtn.setAttribute('aria-expanded', 'false'); } };
    var copyLink = function () {
      var url = location.href;
      var fallback = function () {
        var t = document.createElement('textarea'); t.value = url; t.style.position = 'fixed'; t.style.opacity = '0';
        document.body.appendChild(t); t.select();
        try { document.execCommand('copy'); say('Đã sao chép liên kết'); } catch (e) { say('Không sao chép được, hãy copy từ thanh địa chỉ'); }
        t.remove();
      };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(url).then(function () { say('Đã sao chép liên kết'); }, fallback);
      else fallback();
    };
    actions.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      var act = b.getAttribute('data-act'), sh = b.getAttribute('data-share');
      if (act === 'print') { window.print(); }
      else if (act === 'download') { downloadPage(); }
      else if (act === 'share') {
        // Hộp chia sẻ hệ thống chỉ dùng trên điện thoại/máy tính bảng; máy tính dùng menu riêng (hộp của Windows hay báo lỗi)
        var touch = window.matchMedia && window.matchMedia('(pointer:coarse)').matches;
        var showMenu = function () { var open = menu.hidden; menu.hidden = !open; b.setAttribute('aria-expanded', String(open)); };
        if (navigator.share && touch) {
          navigator.share({ title: document.title, url: location.href }).catch(function (err) { if (!err || err.name !== 'AbortError') showMenu(); });
        } else { showMenu(); }
      } else if (sh) {
        closeMenu();
        if (sh === 'copy') copyLink();
        else if (sh === 'facebook') window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(location.href), '_blank', 'noopener,noreferrer');
        else if (sh === 'email') window.location.href = 'mailto:?subject=' + encodeURIComponent(document.title) + '&body=' + encodeURIComponent(location.href);
      }
    });
    document.addEventListener('click', function (e) { if (menu && !menu.hidden && !e.target.closest('.share-wrap')) closeMenu(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMenu(); });
  }
})();
