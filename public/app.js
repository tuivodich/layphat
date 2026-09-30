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

  // Lọc thẻ trong trang chuyên mục
  var f = document.getElementById('filter');
  if (f) {
    var cards = document.querySelectorAll('#list .feature');
    f.addEventListener('input', function () {
      var q = f.value.trim().toLowerCase();
      cards.forEach(function (c) { c.hidden = q && c.dataset.title.indexOf(q) === -1; });
    });
  }
  // Ô tìm kiếm trang chủ: tạm chuyển đến trang bài viết
  var go = document.getElementById('go');
  if (go) go.addEventListener('click', function () { window.location.href = 'bai-viet.html'; });
})();
