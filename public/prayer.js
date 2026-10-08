// Trang "Gửi lời cầu nguyện": đăng nhập Google, gửi lời (chờ duyệt), xem lời đã được duyệt.
const $ = id => document.getElementById(id);
const V = '10.14.1';
const MAX_LEN = 500;
let db, F, A, auth, user = null, settings = null;
const ADMINS = ['xinloi@gmail.com', 'bachoc@gmail.com'];
const isAdmin = () => !!user && ADMINS.includes((user.email || '').toLowerCase());

const say = (t, cls) => { const m = $('pr-msg'); m.textContent = t || ''; m.className = 'pr-msg ' + (cls || ''); };

// Số ngày theo giờ Việt Nam (UTC+7), ví dụ 20261001 — phải khớp với luật bảo mật
function today() {
  const d = new Date(Date.now() + 7 * 3600 * 1000);
  return d.getUTCFullYear() * 10000 + (d.getUTCMonth() + 1) * 100 + d.getUTCDate();
}

// Che các từ admin cấm: khớp không phân biệt hoa/thường, đúng dấu, theo ranh giới từ. Thay bằng ***.
function maskWords(text, words) {
  const isW = ch => !!ch && /[\p{L}\p{N}]/u.test(ch);
  const low = text.toLowerCase();
  const ranges = [];
  for (const raw of words || []) {
    const w = String(raw).trim().toLowerCase();
    if (!w) continue;
    let from = 0, i;
    while ((i = low.indexOf(w, from)) !== -1) {
      const before = low[i - 1], after = low[i + w.length];
      if (!isW(before) && !isW(after)) ranges.push([i, i + w.length]);
      from = i + 1;
    }
  }
  if (!ranges.length) return text;
  ranges.sort((a, b) => a[0] - b[0]);
  const merged = [ranges[0].slice()];
  for (const r of ranges.slice(1)) { const l = merged[merged.length - 1]; if (r[0] <= l[1]) l[1] = Math.max(l[1], r[1]); else merged.push(r.slice()); }
  let out = '', pos = 0;
  for (const [a, b] of merged) { out += text.slice(pos, a) + '***'; pos = b; }
  return out + text.slice(pos);
}

const fmtDate = ts => { try { const d = ts.toDate(); return d.toLocaleDateString('vi-VN') + ' ' + d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }); } catch (_) { return ''; } };
const safePhoto = u => (typeof u === 'string' && u.startsWith('https://')) ? u : '';

const LOTUS = '<svg viewBox="0 0 64 40" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M32 4c6 6 8 14 0 28-8-14-6-22 0-28z"/><path d="M32 32C22 30 14 22 12 12c10 0 18 6 20 20z"/><path d="M32 32c10-2 18-10 20-20-10 0-18 6-20 20z"/></svg>';

function card(item, words, rxKey) {
  const c = document.createElement('article'); c.className = 'pr-card';
  const by = document.createElement('div'); by.className = 'pr-by';
  const av = document.createElement('span'); av.className = 'pr-av';
  const who = document.createElement('div'); who.className = 'pr-who2';
  const n = document.createElement('span'); n.className = 'pr-name';
  if (!item.anonymous && item.name) {
    const ph = safePhoto(item.photo);
    if (ph) { const im = document.createElement('img'); im.src = ph; im.alt = ''; im.width = 40; im.height = 40; im.loading = 'lazy'; im.referrerPolicy = 'no-referrer'; av.appendChild(im); }
    else av.textContent = (item.name.trim()[0] || '🙏').toUpperCase();
    n.textContent = item.name;
  } else { av.innerHTML = LOTUS; av.classList.add('anon-av'); n.textContent = 'Một người ẩn danh'; n.classList.add('pr-anon'); }
  const t = document.createElement('time'); t.textContent = fmtDate(item.createdAt);
  who.append(n, t); by.append(av, who); c.appendChild(by);
  const p = document.createElement('p'); p.className = 'pr-text'; p.textContent = maskWords(item.text || '', words); c.appendChild(p);
  if (rxKey) { const rx = document.createElement('div'); rx.className = 'rx rx-mini'; rx.dataset.rx = rxKey; c.appendChild(rx); }
  return c;
}

async function loadPublic() {
  const box = $('pr-list');
  try {
    const q = F.query(F.collection(db, 'publicPrayers'), F.orderBy('createdAt', 'desc'), F.limit(30));
    const snap = await F.getDocs(q);
    box.textContent = '';
    if (snap.empty) { box.textContent = 'Chưa có lời cầu nguyện nào được đăng. Hãy là người đầu tiên.'; return; }
    snap.forEach(d => box.appendChild(card(d.data(), settings && settings.badWords, 'loi-' + d.id)));
    // reactions dùng chung (reactions.js): mỗi lời cầu nguyện có bộ đếm riêng, khóa "loi-<id>"
    await import('./reactions.js'); window.LayPhatReactions.scan();
  } catch (e) { box.textContent = 'Không tải được danh sách lời cầu nguyện.'; console.error(e); }
}

const STATUS = { pending: 'Đang chờ duyệt', approved: 'Đã được đăng', rejected: 'Không được đăng', removed: 'Đã gỡ' };

async function loadMine() {
  if (!user) { $('pr-mine-box').hidden = true; return; }
  try {
    const snap = await F.getDocs(F.query(F.collection(db, 'prayers'), F.where('uid', '==', user.uid)));
    const items = []; snap.forEach(d => items.push(d.data()));
    items.sort((a, b) => (b.createdAt && b.createdAt.seconds || 0) - (a.createdAt && a.createdAt.seconds || 0));
    const box = $('pr-mine'); box.textContent = '';
    $('pr-mine-box').hidden = !items.length;
    items.slice(0, 20).forEach(it => {
      const c = card(it, settings && settings.badWords);
      const s = document.createElement('div'); s.className = 'pr-status ' + it.status; s.textContent = STATUS[it.status] || it.status;
      c.insertBefore(s, c.firstChild); box.appendChild(c);
    });
  } catch (e) { console.error(e); }
}

async function quota() {
  if (isAdmin()) { $('pr-quota').textContent = 'Quản trị viên: không giới hạn, lời cầu nguyện được đăng ngay.'; $('pr-send').disabled = false; return 0; }
  if (!user || !settings) return;
  let used = 0;
  try { const s = await F.getDoc(F.doc(db, 'prayerCounts', user.uid)); if (s.exists() && s.data().day === today()) used = s.data().count; } catch (_) {}
  const left = Math.max(0, settings.maxPerDay - used);
  $('pr-quota').textContent = 'Hôm nay bạn đã gửi ' + used + '/' + settings.maxPerDay + ' lời' + (left ? '' : ' (đã hết lượt, mời bạn quay lại ngày mai)');
  $('pr-send').disabled = left === 0;
  return used;
}

function render() {
  const signed = !!user;
  $('pr-state').hidden = true;
  $('pr-login').hidden = signed;
  $('pr-form').hidden = !signed || (!settings && !isAdmin());
  if (signed && !settings && !isAdmin()) { $('pr-state').hidden = false; $('pr-state').textContent = 'Chức năng gửi lời cầu nguyện hiện chưa được bật.'; }
  if (signed) { $('pr-me-name').textContent = user.displayName || user.email; const ph = safePhoto(user.photoURL); $('pr-me-photo').hidden = !ph; if (ph) $('pr-me-photo').src = ph; quota(); }
  loadMine();
}

async function submit(ev) {
  ev.preventDefault();
  if (!user || (!settings && !isAdmin())) return;
  let text = $('pr-text').value.replace(/\s+\n/g, '\n').trim();
  if (text.length < 3) { say('Hãy viết lời cầu nguyện (ít nhất 3 ký tự).', 'err'); return; }
  if (text.length > MAX_LEN) { say('Lời cầu nguyện tối đa ' + MAX_LEN + ' ký tự.', 'err'); return; }
  const anon = document.querySelector('input[name="pr-show"]:checked').value === 'anon';
  text = maskWords(text, settings ? settings.badWords : []);
  $('pr-send').disabled = true; say('Đang gửi…');
  try {
    const day = today();
    const pref = F.doc(F.collection(db, 'prayers'));
    const batch = F.writeBatch(db);
    const base = {
      uid: user.uid, email: user.email, text, anonymous: anon,
      name: anon ? '' : (user.displayName || '').slice(0, 100),
      photo: anon ? '' : safePhoto(user.photoURL).slice(0, 500),
      day, createdAt: F.serverTimestamp()
    };
    if (isAdmin()) {
      // Quản trị viên: đăng thẳng, không cần duyệt, không tính lượt
      const pub = F.doc(F.collection(db, 'publicPrayers'));
      batch.set(pub, { text, anonymous: anon, name: base.name, photo: base.photo, createdAt: F.serverTimestamp() });
      batch.set(pref, { ...base, status: 'approved', publicId: pub.id });
    } else {
      const cref = F.doc(db, 'prayerCounts', user.uid);
      const cs = await F.getDoc(cref);
      const used = cs.exists() && cs.data().day === day ? cs.data().count : 0;
      if (used >= settings.maxPerDay) { say('Hôm nay bạn đã dùng hết ' + settings.maxPerDay + ' lượt gửi.', 'err'); await quota(); return; }
      batch.set(cref, { uid: user.uid, day, count: used + 1, lastId: pref.id });
      batch.set(pref, { ...base, status: 'pending' });
    }
    await batch.commit();
    $('pr-text').value = '';
    say(isAdmin() ? 'Đã đăng lời cầu nguyện.' : 'Cảm ơn bạn. Lời cầu nguyện đã được gửi và đang chờ duyệt.', 'ok');
    await quota(); loadMine(); if (isAdmin()) loadPublic();
  } catch (e) {
    console.error(e);
    say(e.code === 'permission-denied' ? 'Không gửi được: có thể bạn đã hết lượt hôm nay hoặc tài khoản đang bị hạn chế.' : 'Không gửi được: ' + (e.code || e.message), 'err');
    quota();
  } finally { if ($('pr-send').disabled && (settings || isAdmin())) quota(); }
}

async function boot() {
  let cfg = null;
  try { cfg = JSON.parse(localStorage.getItem('lp_fb_cfg') || 'null'); } catch (_) {}
  if (!cfg || !cfg.apiKey) { try { const r = await fetch('/__/firebase/init.json'); if (r.ok) cfg = await r.json(); } catch (_) {} }
  if (!cfg || !cfg.apiKey) { $('pr-state').textContent = 'Chưa thể kết nối. Vui lòng thử lại sau.'; $('pr-list').textContent = ''; return; }
  const { initializeApp } = await import('https://www.gstatic.com/firebasejs/' + V + '/firebase-app.js');
  A = await import('https://www.gstatic.com/firebasejs/' + V + '/firebase-auth.js');
  F = await import('https://www.gstatic.com/firebasejs/' + V + '/firebase-firestore.js');
  const app = initializeApp(cfg); auth = A.getAuth(app); db = F.getFirestore(app);
  try { const s = await F.getDoc(F.doc(db, 'settings', 'prayer')); if (s.exists()) { settings = s.data(); settings.maxPerDay = Number(settings.maxPerDay) || 0; if (settings.maxPerDay < 1) settings = null; } } catch (e) { console.error(e); }
  $('pr-signin').onclick = async () => { say(''); try { await A.signInWithPopup(auth, new A.GoogleAuthProvider()); } catch (e) { say('Đăng nhập không thành công: ' + (e.code || e.message), 'err'); } };
  $('pr-signout').onclick = () => A.signOut(auth);
  $('pr-form').addEventListener('submit', submit);
  A.onAuthStateChanged(auth, u => { user = u && u.emailVerified ? u : null; render(); });
  loadPublic();
}
boot().catch(e => { console.error(e); $('pr-state').textContent = 'Lỗi tải: ' + (e.message || e); });
