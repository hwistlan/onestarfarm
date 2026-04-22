import zipfile

# 1. index.html - Original base with fixes
index_orig = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>한별농원 — 2026 햇사과 산지직송</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700&family=Noto+Sans+KR:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --cream:#fdf8f2; --warm:#fff9f4; --brown:#2c1e0f; --brown-m:#5a3e28;
  --brown-l:#a07050; --brown-p:#e8d5c0; --red:#c8421a; --red-d:#a83210;
  --red-p:#fff0e8; --red-b:#f0c0a0; --green:#1D9E75; --green-p:#eaf3de;
  --amber:#EF9F27; --amber-p:#fffbe8; --blue:#185FA5; --blue-p:#e6f1fb;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{height:100%;font-family:'Noto Sans KR',sans-serif;background:#ede4d8;color:var(--brown);}

/* 메인 앱 컨테이너 */
#app { display: flex; flex-direction: column; min-height: 100vh; max-width: 500px; margin: 0 auto; background: var(--warm); box-shadow: 0 0 30px rgba(0,0,0,0.05); }

/* 헤더 */
header { padding: 40px 20px 20px; text-align: center; }
.logo-area { font-family: 'Noto Serif KR', serif; font-weight: 700; font-size: 26px; letter-spacing: -0.5px; color: var(--brown); margin-bottom: 4px; }
.sub-tag { font-size: 13px; color: var(--brown-l); font-weight: 400; letter-spacing: 2px; }

/* 안내 섹션 */
.notice-box { margin: 10px 20px 24px; padding: 18px; background: var(--red-p); border-radius: 12px; border-left: 4px solid var(--red); }
.notice-label { font-size: 11px; font-weight: 700; color: var(--red); margin-bottom: 6px; display: block; }
.notice-text { font-size: 14.5px; line-height: 1.6; color: var(--brown); font-weight: 500; word-break: keep-all; }

/* 상품 카드 */
.product-card { margin: 0 20px 16px; background: white; border-radius: 16px; padding: 24px; border: 1px solid #eee; transition: 0.2s; }
.item-name { font-family: 'Noto Serif KR', serif; font-size: 18px; font-weight: 700; margin-bottom: 8px; color: var(--brown); }
.item-price { font-size: 17px; font-weight: 600; color: var(--red); margin-bottom: 12px; }
.item-desc { font-size: 13.5px; color: var(--brown-m); line-height: 1.5; margin-bottom: 18px; }
.order-btn { width: 100%; padding: 14px; background: var(--brown); color: white; border-radius: 10px; border: none; font-weight: 600; cursor: pointer; font-size: 14px; }

/* 정보 섹션 */
.info-section { margin-top: auto; padding: 40px 20px; background: #f9f4ee; font-size: 13.5px; color: var(--brown-m); }
.info-title { font-weight: 700; margin-bottom: 12px; color: var(--brown); font-size: 14px; border-left: 3px solid var(--brown-l); padding-left: 8px; }
.info-item { margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }

/* 토스트 메시지 */
#toast { position: fixed; bottom: 40px; left: 50%; transform: translateX(-50%); background: rgba(44, 30, 15, 0.9); color: white; padding: 12px 24px; border-radius: 30px; font-size: 13px; opacity: 0; transition: 0.3s; pointer-events: none; z-index: 1000; }
#toast.show { opacity: 1; }

#admin-app { display: none; }
</style>
</head>
<body>

<div id="app">
  <header>
    <div class="logo-area">한별농원</div>
    <div class="sub-tag">HANBYEOL APPLE FARM</div>
  </header>

  <div class="notice-box">
    <span class="notice-label">농장 소식</span>
    <div class="notice-text" id="main-notice">올해에도 정성껏 키운 한별농원 햇사과를 만나보세요.</div>
  </div>

  <div id="product-list">
    </div>

  <div class="info-section">
    <div class="info-title">주문 및 문의</div>
    <div class="info-item"><span>대표 연락처</span> <span id="display-phone">010-0000-0000</span></div>
    <div class="info-item"><span>농장 위치</span> <span id="display-addr">충북 괴산군 장연면 방곡리</span></div>
    <div style="height:25px"></div>
    <div class="info-title">입금 계좌 안내</div>
    <div id="display-bank" style="font-weight:600; background:white; padding:15px; border-radius:12px; border:1px solid #e0d0c0;" onclick="copyAccount()">
      농협 000-00-00000 (한별농원)
    </div>
  </div>

  <div id="footer-admin" style="text-align:center;padding:30px 16px;cursor:pointer;" onclick="handleFooterClick()">
    <div style="font-size:10px;color:#a08c7d;line-height:1.8;">
      © 2026 한별농원 · All Rights Reserved<br>
      <span id="footer-gear" style="font-size:14px;opacity:0.1;transition:opacity 0.3s;">⚙</span>
    </div>
  </div>
</div>

<div id="toast">복사되었습니다.</div>

<script>
let footerClickCount = 0;
let footerTimer = null;

function syncAdminSettings() {
  const bank = localStorage.getItem('hb_bank') || "농협";
  const acct = localStorage.getItem('hb_account') || "000-00-00000";
  const holder = localStorage.getItem('hb_holder') || "한별농원";
  const phone = localStorage.getItem('hb_phone') || "010-0000-0000";
  const addr = localStorage.getItem('hb_addr') || "충북 괴산군 장연면 방곡리";
  const notice = localStorage.getItem('hb_notice') || "올해에도 정성껏 키운 한별농원 햇사과를 만나보세요.";

  document.getElementById('display-bank').textContent = `${bank} ${acct} (${holder})`;
  document.getElementById('display-phone').textContent = phone;
  document.getElementById('display-addr').textContent = addr;
  document.getElementById('main-notice').textContent = notice;
}

function renderHome() {
  const container = document.getElementById('product-list');
  const vars = JSON.parse(localStorage.getItem('hb_variety') || '[]');
  
  if(vars.length === 0) {
    container.innerHTML = '<div style="text-align:center; padding:60px 20px; color:#999; font-size:14px;">상품을 준비 중입니다.</div>';
    return;
  }

  container.innerHTML = vars.map(v => `
    <div class="product-card">
      <div class="item-name">${v.name}</div>
      <div class="item-price">${v.price}</div>
      <div class="item-desc">${v.desc}</div>
      <button class="order-btn" onclick="alert('전화 주문 부탁드립니다.')">주문 문의</button>
    </div>
  `).join('');
}

function handleFooterClick() {
  footerClickCount++;
  document.getElementById('footer-gear').style.opacity = footerClickCount * 0.15;
  clearTimeout(footerTimer);
  footerTimer = setTimeout(() => { footerClickCount = 0; document.getElementById('footer-gear').style.opacity = 0.1; }, 2000);

  if (footerClickCount >= 7) {
    location.href = './login.html'; // 수정됨
  }
}

function copyAccount() {
  const text = document.getElementById('display-bank').textContent;
  navigator.clipboard.writeText(text).then(() => {
    const t = document.getElementById('toast');
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2000);
  });
}

// 핵심 수정: 화면이 다시 보일 때마다 데이터 새로고침
window.addEventListener('pageshow', function() {
  syncAdminSettings();
  renderHome();
});

window.onload = () => {
  syncAdminSettings();
  renderHome();
};
</script>
</body>
</html>"""

# 2. login.html - Original base with fixes
login_orig = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>로그인 — 한별농원</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700&family=Noto+Sans+KR:wght@400;500;600&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #1a0e05;
  color: #f5e6d3;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  font-family: 'Noto Sans KR', sans-serif;
  padding: 20px;
}
.box {
  background: #25160d;
  padding: 40px 36px;
  border-radius: 24px;
  width: 100%;
  max-width: 360px;
  text-align: center;
  border: 0.5px solid #4a2c1a;
}
.logo { font-size: 36px; margin-bottom: 12px; }
.title { font-family: 'Noto Serif KR', serif; font-size: 18px; font-weight: 700; margin-bottom: 30px; }

.form-group { text-align: left; margin-bottom: 20px; }
.form-label { font-size: 12px; color: #8b5e3c; margin-bottom: 8px; display: block; }
input {
  width: 100%;
  background: #1a0e05;
  border: 1px solid #4a2c1a;
  border-radius: 12px;
  padding: 14px;
  color: #fff;
  outline: none;
}
.login-btn {
  width: 100%;
  padding: 14px;
  background: #8b5e3c;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
}
.error-msg { color: #ff6b6b; font-size: 13px; margin-top: 15px; min-height: 20px; }
</style>
</head>
<body>
<div class="box">
  <div class="logo">🍎</div>
  <div class="title">한별농원 관리자</div>
  <div class="form-group">
    <label class="form-label">아이디</label>
    <input type="text" id="uid" placeholder="admin">
  </div>
  <div class="form-group">
    <label class="form-label">비밀번호</label>
    <input type="password" id="upw" placeholder="1234">
  </div>
  <button class="login-btn" onclick="doLogin()">로그인</button>
  <div class="error-msg" id="err-msg"></div>
  <a href="./index.html" style="color:#5a3e28; font-size:13px; text-decoration:none; display:inline-block; margin-top:20px;">홈으로 돌아가기</a>
</div>

<script>
function doLogin() {
  const uid = document.getElementById('uid').value.trim();
  const upw = document.getElementById('upw').value;
  const msg = document.getElementById('err-msg');
  
  if (uid === 'admin' && upw === '1234') {
    location.href = './onestar_admin.html'; // 수정됨
  } else {
    msg.textContent = '정보가 일치하지 않습니다.';
  }
}
</script>
</body>
</html>"""

# 3. onestar_admin.html - Original base with fixes
onestar_admin_orig = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>한별농원 관리 시스템</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@600;700&family=Noto+Sans+KR:wght@400;500;600&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #1a0e05; color: #f5e6d3; font-family: 'Noto Sans KR', sans-serif; min-height: 100vh; padding-bottom: 80px; }
.shell { max-width: 500px; margin: 0 auto; }
header { padding: 20px; border-bottom: 1px solid #2d1a0d; display: flex; justify-content: space-between; align-items: center; }
.brand { font-family: 'Noto Serif KR', serif; font-weight: 700; font-size: 16px; }
.card { background: #25160d; margin: 16px; border-radius: 16px; padding: 20px; border: 1px solid #2d1a0d; }
.input-group { margin-bottom: 15px; }
label { display: block; font-size: 12px; color: #8b5e3c; margin-bottom: 6px; }
input, textarea { width: 100%; background: #1a0e05; border: 1px solid #3d2516; border-radius: 10px; padding: 12px; color: #fff; font-size: 14px; outline: none; }
.save-btn { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); width: calc(100% - 32px); max-width: 468px; padding: 18px; background: #8b5e3c; color: #fff; border: none; border-radius: 12px; font-weight: 700; cursor: pointer; }
.var-item { background: #1a0e05; padding: 12px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #2d1a0d; }
.del-btn { color: #ff6b6b; font-size: 11px; cursor: pointer; float: right; }
</style>
</head>
<body>
<header>
  <div class="brand">한별농원 ADMIN</div>
  <a href="./index.html" style="color:#8b5e3c; text-decoration:none; font-size:13px;">나가기</a>
</header>

<div class="shell">
  <div class="card">
    <div class="input-group"><label>농장 공지</label><textarea id="farm-notice" rows="2"></textarea></div>
    <div class="input-group"><label>연락처</label><input type="text" id="farm-phone"></div>
    <div class="input-group"><label>주소</label><input type="text" id="farm-addr"></div>
  </div>
  <div class="card">
    <div class="input-group"><label>은행</label><input type="text" id="bank-name"></div>
    <div class="input-group"><label>계좌번호</label><input type="text" id="acct-num"></div>
    <div class="input-group"><label>예금주</label><input type="text" id="acct-holder"></div>
  </div>
  <div class="card">
    <div id="var-list"></div>
    <button onclick="addVariety()" style="width:100%; padding:10px; background:transparent; border:1px dashed #4a2c1a; color:#8b5e3c; border-radius:8px;">+ 상품 추가</button>
  </div>
</div>
<button class="save-btn" onclick="saveAll()">설정 저장하기</button>

<script>
function addVariety() {
  const list = document.getElementById('var-list');
  const div = document.createElement('div');
  div.className = 'var-item';
  div.innerHTML = `
    <span class="del-btn" onclick="this.parentElement.remove()">삭제</span>
    <input type="text" placeholder="상품명" class="v-name" style="margin-bottom:8px">
    <input type="text" placeholder="가격" class="v-price" style="margin-bottom:8px">
    <input type="text" placeholder="설명" class="v-desc">
  `;
  list.appendChild(div);
}

function saveAll() {
  localStorage.setItem('hb_notice', document.getElementById('farm-notice').value);
  localStorage.setItem('hb_phone', document.getElementById('farm-phone').value);
  localStorage.setItem('hb_addr', document.getElementById('farm-addr').value);
  localStorage.setItem('hb_bank', document.getElementById('bank-name').value);
  localStorage.setItem('hb_account', document.getElementById('acct-num').value);
  localStorage.setItem('hb_holder', document.getElementById('acct-holder').value);

  const vars = [];
  document.querySelectorAll('.var-item').forEach(item => {
    vars.push({
      name: item.querySelector('.v-name').value,
      price: item.querySelector('.v-price').value,
      desc: item.querySelector('.v-desc').value
    });
  });
  localStorage.setItem('hb_variety', JSON.stringify(vars));
  alert("저장되었습니다.");
  location.href = './index.html'; // 수정됨
}

window.onload = () => {
  document.getElementById('farm-notice').value = localStorage.getItem('hb_notice') || "";
  document.getElementById('farm-phone').value = localStorage.getItem('hb_phone') || "";
  document.getElementById('farm-addr').value = localStorage.getItem('hb_addr') || "";
  document.getElementById('bank-name').value = localStorage.getItem('hb_bank') || "";
  document.getElementById('acct-num').value = localStorage.getItem('hb_account') || "";
  document.getElementById('acct-holder').value = localStorage.getItem('hb_holder') || "";
  
  const vars = JSON.parse(localStorage.getItem('hb_variety') || '[]');
  vars.forEach(v => {
    const list = document.getElementById('var-list');
    const div = document.createElement('div');
    div.className = 'var-item';
    div.innerHTML = `
      <span class="del-btn" onclick="this.parentElement.remove()">삭제</span>
      <input type="text" value="${v.name}" class="v-name" style="margin-bottom:8px">
      <input type="text" value="${v.price}" class="v-price" style="margin-bottom:8px">
      <input type="text" value="${v.desc}" class="v-desc">
    `;
    list.appendChild(div);
  });
};
</script>
</body>
</html>"""

# Writing to files
with open("index.html", "w", encoding="utf-8") as f: f.write(index_orig)
with open("login.html", "w", encoding="utf-8") as f: f.write(login_orig)
with open("onestar_admin.html", "w", encoding="utf-8") as f: f.write(onestar_admin_orig)

# Creating ZIP
zip_name = "onestarfarm_original_fixed.zip"
with zipfile.ZipFile(zip_name, 'w') as z:
    z.write("index.html")
    z.write("login.html")
    z.write("onestar_admin.html")