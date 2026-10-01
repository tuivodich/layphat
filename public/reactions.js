// Bộ reactions dùng chung: Thích / Thả tim / Cười / Không thích.
// Cách dùng: đặt <div class="rx" data-rx="khoa-duy-nhat-cua-muc"></div> ở bất kỳ trang nào và nạp
//   <script type="module" src="reactions.js"></script>
// Khóa (data-rx) nên là tên file của bài, ví dụ "bai-viet-kho-dau-diet-kho". Mỗi khóa là một bộ đếm riêng.
// Với nội dung tạo động (danh sách lời cầu nguyện...), gọi: window.LayPhatReactions.mount(phanTu, khoa)
const V = '10.14.1';
const TYPES = [
  { id: 'like', icon: '👍', label: 'Thích' },
  { id: 'love', icon: '❤️', label: 'Thả tim' },
  { id: 'laugh', icon: '😄', label: 'Cười' },
  { id: 'dislike', icon: '👎', label: 'Không thích' }
];
const KEY_OK = /^[A-Za-z0-9._-]{1,100}$/;

let sdk = null, user = null;
const subs = new Set();   // các khối đang hiển thị, để cập nhật khi đăng nhập/đăng xuất

function ensureSdk() {
  if (sdk) return sdk;
  sdk = (async () => {
    let cfg = null;
    try { cfg = JSON.parse(localStorage.getItem('lp_fb_cfg') || 'null'); } catch (_) {}
    if (!cfg || !cfg.apiKey) { try { const r = await fetch('/__/firebase/init.json'); if (r.ok) cfg = await r.json(); } catch (_) {} }
    if (!cfg || !cfg.apiKey) throw new Error('no-config');
    const { initializeApp } = await import('https://www.gstatic.com/firebasejs/' + V + '/firebase-app.js');
    const A = await import('https://www.gstatic.com/firebasejs/' + V + '/firebase-auth.js');
    const F = await import('https://www.gstatic.com/firebasejs/' + V + '/firebase-firestore.js');
    const app = initializeApp(cfg), auth = A.getAuth(app), db = F.getFirestore(app);
    A.onAuthStateChanged(auth, u => { user = u && u.emailVerified ? u : null; subs.forEach(s => s.onUser()); });
    return { A, F, auth, db };
  })();
  sdk.catch(() => { sdk = null; });
  return sdk;
}

function mount(root, key) {
  if (!root || root.dataset.rxReady || !KEY_OK.test(key || '')) return;
  root.dataset.rxReady = '1';
  root.textContent = '';
  const row = document.createElement('div'); row.className = 'rx-row'; row.setAttribute('role', 'group'); row.setAttribute('aria-label', 'Cảm nhận của bạn');
  const info = document.createElement('div'); info.className = 'rx-info'; info.setAttribute('role', 'status');
  const btns = {};
  const counts = {}; TYPES.forEach(t => counts[t.id] = 0);
  let mine = null, busy = false, ok = false;

  TYPES.forEach(t => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'rx-btn'; b.dataset.type = t.id; b.setAttribute('aria-pressed', 'false');
    b.innerHTML = '<span class="rx-ic" aria-hidden="true"></span><span class="rx-lb"></span><span class="rx-n">0</span>';
    b.querySelector('.rx-ic').textContent = t.icon; b.querySelector('.rx-lb').textContent = t.label;
    b.title = t.label; b.onclick = () => choose(t.id);
    btns[t.id] = b; row.appendChild(b);
  });
  root.appendChild(row); root.appendChild(info);

  function paint() {
    TYPES.forEach(t => {
      const b = btns[t.id]; b.querySelector('.rx-n').textContent = counts[t.id];
      const on = mine === t.id; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.disabled = busy;
    });
    if (!ok) return;
    info.innerHTML = '';
    if (!user) {
      const s = document.createElement('span'); s.textContent = 'Đăng nhập để bày tỏ cảm nhận: ';
      const a = document.createElement('button'); a.type = 'button'; a.className = 'rx-login'; a.textContent = 'Đăng nhập với Google';
      a.onclick = async () => { try { const { A, auth } = await ensureSdk(); await A.signInWithPopup(auth, new A.GoogleAuthProvider()); } catch (e) { say('Đăng nhập không thành công.'); } };
      info.append(s, a);
    } else if (mine) info.textContent = 'Bạn đã chọn “' + TYPES.find(t => t.id === mine).label + '”. Bấm lại để bỏ chọn hoặc chọn loại khác để đổi.';
    else info.textContent = 'Hãy chọn một cảm nhận.';
  }
  const say = t => { info.textContent = t; };
  const docId = () => key + '__' + user.uid;

  async function loadCounts() {
    const { F, db } = await ensureSdk();
    const col = F.collection(db, 'reactions');
    const res = await Promise.all(TYPES.map(t => F.getCountFromServer(F.query(col, F.where('item', '==', key), F.where('type', '==', t.id)))));
    res.forEach((r, i) => counts[TYPES[i].id] = r.data().count);
  }
  async function loadMine() {
    mine = null;
    if (!user) return;
    const { F, db } = await ensureSdk();
    try { const s = await F.getDoc(F.doc(db, 'reactions', docId())); if (s.exists() && TYPES.some(t => t.id === s.data().type)) mine = s.data().type; } catch (e) { console.error(e); }
  }
  async function choose(type) {
    if (busy) return;
    if (!user) { say('Hãy đăng nhập bằng Google để bày tỏ cảm nhận.'); paint(); return; }
    busy = true; const prev = mine; paint();
    try {
      const { F, db } = await ensureSdk(); const ref = F.doc(db, 'reactions', docId());
      if (prev === type) { await F.deleteDoc(ref); counts[type] = Math.max(0, counts[type] - 1); mine = null; }
      else {
        await F.setDoc(ref, { item: key, type, updatedAt: F.serverTimestamp() });
        if (prev) counts[prev] = Math.max(0, counts[prev] - 1);
        counts[type]++; mine = type;
      }
    } catch (e) { console.error(e); busy = false; paint(); say('Không lưu được cảm nhận của bạn. Vui lòng thử lại.'); return; }
    busy = false; paint();
  }

  const sub = { onUser: async () => { await loadMine(); paint(); } };
  async function start() {
    try {
      await ensureSdk(); subs.add(sub);
      await Promise.all([loadCounts(), loadMine()]);
      ok = true; paint();
    } catch (e) { console.error(e); info.textContent = ''; root.hidden = true; }
  }
  paint();
  // chỉ tải Firebase khi khối reactions sắp hiện ra, để không làm chậm trang
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) { io.disconnect(); start(); } }, { rootMargin: '400px' });
    io.observe(root);
  } else start();
}

function scan() { document.querySelectorAll('[data-rx]').forEach(el => mount(el, el.dataset.rx)); }
window.LayPhatReactions = { mount, scan, TYPES };
scan();
