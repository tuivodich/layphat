// Lọc thẻ trong trang chuyên mục
(function () {
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
