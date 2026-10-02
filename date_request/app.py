"""데이트 신청서 💌 — 핑크 & 하트 테마의 Streamlit 앱."""

import datetime as dt
from html import escape

import streamlit as st

st.set_page_config(page_title="데이트 신청서", page_icon="💖", layout="centered")

# ---------------------------------------------------------------------------
# 선택지 데이터
# ---------------------------------------------------------------------------
CUSTOM_TIME = "⏰ 직접 정하기"
TIME_SLOTS = [
    "🌅 아침 (09:00)",
    "🌤️ 점심 (12:00)",
    "☕ 오후 (15:00)",
    "🌆 저녁 (18:00)",
    "🌙 밤 (20:00)",
    CUSTOM_TIME,
]

FOODS = {
    "🍚 한식": "따끈한 집밥 감성",
    "🍣 일식": "초밥이랑 라멘",
    "🍝 양식": "파스타 & 스테이크",
    "🥟 중식": "짜장 짬뽕 탕수육",
    "🥩 고기": "지글지글 삼겹살",
    "🍢 분식": "떡볶이는 못 참지",
}

PLACES = ["☕ 카페", "🎬 영화", "🌳 산책", "🎨 전시회", "🎡 놀이공원", "🎤 노래방", "🛍️ 쇼핑", "🌊 바다"]

DESSERTS = ["🍰 케이크", "🍦 아이스크림", "🧇 와플", "🍩 도넛", "🧋 버블티", "🍓 탕후루"]

STEPS = ["신청", "날짜", "밥", "장소", "디저트", "완성"]

# ---------------------------------------------------------------------------
# 상태
# ---------------------------------------------------------------------------
ss = st.session_state
ss.setdefault("step", 0)

# 위젯 key = 데이트 계획 항목. 페이지를 넘겨도 값이 지워지지 않도록 매 실행마다 다시 대입한다.
PLAN_DEFAULTS = {
    "date": lambda: dt.date.today() + dt.timedelta(days=1),
    "time": lambda: "🌆 저녁 (18:00)",
    "custom_time": lambda: dt.time(19, 0),
    "food": lambda: None,
    "places": lambda: [],
    "custom_places": lambda: [],
    "dessert": lambda: None,
    "custom_desserts": lambda: [],
    "message": lambda: "",
}
for _k, _default in PLAN_DEFAULTS.items():
    ss[_k] = ss[_k] if _k in ss else _default()


def go(step: int) -> None:
    ss.step = step


def restart() -> None:
    for k in PLAN_DEFAULTS:
        del ss[k]
    ss.step = 0


# ---------------------------------------------------------------------------
# 전역 스타일: 핑크 테마 + 떠다니는 하트
# ---------------------------------------------------------------------------
st.html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Gaegu:wght@400;700&display=swap');

.stApp {
  background: linear-gradient(180deg, #fff0f6 0%, #ffe3ee 100%);
}
.stApp { color: #5b2140; }
.stApp, .stApp p, .stApp label, .stApp li {
  font-family: 'Gaegu', 'Jua', sans-serif;
  font-size: 1.15rem;
}
h1, h2, h3, .stButton button, .stDownloadButton button {
  font-family: 'Jua', sans-serif !important;
}
h1, h2, h3 { color: #e8457c !important; text-align: center; }
h1 { font-size: clamp(1.9rem, 8vw, 2.8rem) !important; white-space: nowrap; }

.stButton button, .stDownloadButton button {
  border-radius: 999px !important;
  border: 2px solid #ff8fb3 !important;
  transition: transform .15s ease;
}
.stButton button:hover, .stDownloadButton button:hover { transform: scale(1.05); }
.stButton button[kind="primary"] {
  background: linear-gradient(135deg, #ff6b9d, #ff4d88) !important;
  color: white !important;
  box-shadow: 0 6px 16px rgba(255, 77, 136, .35);
}

[data-testid="stVerticalBlockBorderWrapper"] {
  background: rgba(255,255,255,.75);
  border-radius: 24px !important;
}

.hearts { position: fixed; inset: 0; pointer-events: none; overflow: hidden; z-index: 0; }
.hearts span {
  position: absolute; bottom: -40px; opacity: .55;
  animation: floatUp linear infinite;
}
@keyframes floatUp {
  from { transform: translateY(0) rotate(0deg); }
  to   { transform: translateY(-115vh) rotate(25deg); }
}
.progress { text-align: center; font-size: 1.6rem; letter-spacing: .4rem; margin-bottom: .2rem; }
.progress-label { text-align: center; color: #c06088; font-size: 1rem; margin-bottom: 1rem; }
.stApp .subtitle { text-align: center; color: #b04a75; font-family: 'Jua', sans-serif; font-size: 1.6rem; }
</style>
<div class="hearts">
  <span style="left:5%;  font-size:22px; animation-duration:11s; animation-delay:0s">💗</span>
  <span style="left:18%; font-size:16px; animation-duration:14s; animation-delay:3s">💕</span>
  <span style="left:32%; font-size:26px; animation-duration:12s; animation-delay:6s">💖</span>
  <span style="left:50%; font-size:18px; animation-duration:15s; animation-delay:1s">💓</span>
  <span style="left:66%; font-size:24px; animation-duration:13s; animation-delay:4s">💗</span>
  <span style="left:80%; font-size:16px; animation-duration:10s; animation-delay:7s">💞</span>
  <span style="left:92%; font-size:22px; animation-duration:16s; animation-delay:2s">💘</span>
</div>
"""
)


def progress() -> None:
    hearts = "".join("💖" if i <= ss.step else "🤍" for i in range(len(STEPS)))
    st.html(
        f'<div class="progress">{hearts}</div>'
        f'<div class="progress-label">{ss.step + 1} / {len(STEPS)} · {STEPS[ss.step]}</div>'
    )


def nav(next_disabled: bool = False) -> None:
    left, right = st.columns(2)
    left.button("← 이전", on_click=go, args=(ss.step - 1,), width="stretch")
    right.button(
        "다음 💕",
        on_click=go,
        args=(ss.step + 1,),
        type="primary",
        disabled=next_disabled,
        width="stretch",
    )


# ---------------------------------------------------------------------------
# 도망가는 거절 버튼 컴포넌트
# ---------------------------------------------------------------------------
ASK_HTML = """
<div class="arena">
  <button class="yes">좋아 💖</button>
  <button class="no">거절 🙅</button>
  <div class="tease"></div>
</div>
"""

ASK_CSS = """
.arena {
  position: relative; height: 260px; width: 100%;
  font-family: 'Jua', sans-serif; user-select: none;
}
button {
  position: absolute; top: 50%; transform: translate(-50%, -50%);
  border-radius: 999px; cursor: pointer; font-family: inherit;
  padding: .7em 1.6em; font-size: 1.3rem; white-space: nowrap;
}
.yes {
  left: 32%;
  background: linear-gradient(135deg, #ff6b9d, #ff4d88); color: #fff;
  border: none; box-shadow: 0 8px 20px rgba(255, 77, 136, .4);
  transition: font-size .25s ease;
  animation: beat 1.2s ease-in-out infinite;
  z-index: 2;
}
.yes:hover { filter: brightness(1.05); }
.no {
  left: 68%;
  background: #fff; color: #c06088; border: 2px solid #ffb3cc;
  transition: left .25s ease, top .25s ease;
  z-index: 1;
}
.tease {
  position: absolute; bottom: 0; width: 100%; text-align: center;
  color: #c06088; font-size: 1.05rem; min-height: 1.4em;
}
@media (max-width: 480px) {
  button { font-size: 1.1rem; padding: .6em 1.2em; }
  .yes { left: 27%; }
  .no { left: 74%; }
}
@keyframes beat {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50%      { transform: translate(-50%, -50%) scale(1.07); }
}
"""

ASK_JS = """
export default function (component) {
  const { parentElement, setTriggerValue } = component;
  const arena = parentElement.querySelector('.arena');
  const yes = parentElement.querySelector('.yes');
  const no = parentElement.querySelector('.no');
  const tease = parentElement.querySelector('.tease');

  const lines = [
    '어딜 누르려고~? 😏', '못 잡지롱 🏃‍♀️', '거절 버튼은 휴가 중이에요 🏖️',
    '그 버튼은 고장났어요 🔧', '좋아 버튼이 더 예쁜데? 💕', '포기하면 편해요 😚',
    '도망 성공! 🐰', '이쯤 되면 운명이야 💘',
  ];
  let escapes = 0;

  const runAway = (e) => {
    if (e) { e.preventDefault(); e.stopPropagation(); }
    const w = arena.clientWidth, h = arena.clientHeight;
    const bw = no.offsetWidth, bh = no.offsetHeight;
    const yr = yes.getBoundingClientRect(), ar = arena.getBoundingClientRect();
    const nr = no.getBoundingClientRect();
    const pt = e && e.touches ? e.touches[0] : e;
    // 커서(없으면 현재 버튼 위치)에서 멀리 도망간다
    const px = pt && pt.clientX != null ? pt.clientX - ar.left : nr.left - ar.left + nr.width / 2;
    const py = pt && pt.clientY != null ? pt.clientY - ar.top : nr.top - ar.top + nr.height / 2;
    const overlapsYes = (x, y) =>
      Math.abs(x - (yr.left - ar.left + yr.width / 2)) < (bw + yr.width) / 2 + 10 &&
      Math.abs(y - (yr.top - ar.top + yr.height / 2)) < (bh + yr.height) / 2 + 10;
    let x, y, tries = 0;
    do {
      x = bw / 2 + Math.random() * Math.max(1, w - bw);
      y = bh / 2 + Math.random() * Math.max(1, h - bh - 30);
      tries++;
    } while (tries < 60 && (overlapsYes(x, y) || Math.hypot(x - px, y - py) < Math.min(150, w / 3)));
    no.style.left = x + 'px';
    no.style.top = y + 'px';
    escapes++;
    tease.textContent = lines[(escapes - 1) % lines.length];
    yes.style.fontSize = Math.min(1.3 + escapes * 0.08, 2.4) + 'rem';
  };

  no.addEventListener('mouseenter', runAway);
  no.addEventListener('touchstart', runAway, { passive: false });
  no.addEventListener('focus', runAway);
  no.addEventListener('click', runAway);
  yes.addEventListener('click', () => setTriggerValue('answer', 'yes'));
}
"""

ask_component = st.components.v2.component(
    "date_ask_buttons", html=ASK_HTML, css=ASK_CSS, js=ASK_JS
)


# ---------------------------------------------------------------------------
# 페이지들
# ---------------------------------------------------------------------------
def page_ask() -> None:
    st.markdown("<h1>💌 데이트 신청서 💌</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.html(
            '<div style="text-align:center;font-size:4rem">🥺👉👈</div>'
            '<p class="subtitle">저기... 나랑 데이트 할래?</p>'
        )
        result = ask_component(key="ask", on_answer_change=lambda: None)
    if result.answer == "yes":
        go(1)
        st.rerun()


def page_date() -> None:
    progress()
    st.markdown("## 📅 언제 만날까?")
    with st.container(border=True):
        st.date_input("날짜를 골라줘", min_value=dt.date.today(), key="date")
        st.radio("몇 시가 좋아?", TIME_SLOTS, horizontal=True, key="time")
        if ss.time == CUSTOM_TIME:
            st.time_input("원하는 시간을 골라줘", step=dt.timedelta(minutes=10), key="custom_time")
    nav()


def time_text() -> str:
    if ss.time != CUSTOM_TIME:
        return ss.time
    t = ss.custom_time
    ampm = "오전" if t.hour < 12 else "오후"
    hour = t.hour % 12 or 12
    return f"⏰ {ampm} {hour}시" + (f" {t.minute}분" if t.minute else "")


def add_custom(input_key: str, list_key: str | None, target_key: str, multi: bool) -> None:
    """직접 입력한 항목을 선택지에 추가하고 바로 선택한다."""
    text = ss[input_key].strip()
    if not text:
        return
    item = f"✏️ {text}"
    if list_key is not None and item not in ss[list_key]:
        ss[list_key] = ss[list_key] + [item]
    if multi:
        if item not in ss[target_key]:
            ss[target_key] = ss[target_key] + [item]
    else:
        ss[target_key] = item
    ss[input_key] = ""


def custom_input(label: str, placeholder: str, input_key: str, list_key: str | None, target_key: str, multi: bool) -> None:
    left, right = st.columns([3, 1], vertical_alignment="bottom")
    args = (input_key, list_key, target_key, multi)
    # 엔터만 쳐도 추가되도록 on_change에도 연결
    left.text_input(label, placeholder=placeholder, max_chars=20, key=input_key, on_change=add_custom, args=args)
    right.button(
        "추가 💕",
        key=f"{input_key}_btn",
        on_click=add_custom,
        args=args,
        width="stretch",
    )


def pick_food(name: str) -> None:
    ss.food = name


def page_food() -> None:
    progress()
    st.markdown("## 🍽️ 뭐 먹을까?")
    cols = st.columns(3)
    for i, (name, desc) in enumerate(FOODS.items()):
        with cols[i % 3].container(border=True):
            st.markdown(f"<h3>{name}</h3><p style='text-align:center'>{desc}</p>", unsafe_allow_html=True)
            picked = ss.food == name
            st.button(
                "💖 선택됨" if picked else "이거!",
                key=f"food_{i}",
                on_click=pick_food,
                args=(name,),
                type="primary" if picked else "secondary",
                width="stretch",
            )
    with st.container(border=True):
        custom_input("✏️ 먹고 싶은 게 따로 있어?", "예) 마라탕, 쌀국수", "new_food", None, "food", multi=False)
        if ss.food and ss.food not in FOODS:
            st.markdown(f"<p style='text-align:center'>💖 <b>{escape(ss.food)}</b> 선택됨!</p>", unsafe_allow_html=True)
    nav(next_disabled=not ss.food)


def page_place() -> None:
    progress()
    st.markdown("## 🗺️ 밥 먹고 어디 갈까?")
    with st.container(border=True):
        st.pills(
            "하고 싶은 거 다 골라줘 (여러 개 가능)",
            PLACES + ss.custom_places,
            selection_mode="multi",
            key="places",
        )
        custom_input("✏️ 가고 싶은 데 직접 추가", "예) 보드게임 카페, 한강 피크닉", "new_place", "custom_places", "places", multi=True)
    nav(next_disabled=not ss.places)


def page_dessert() -> None:
    progress()
    st.markdown("## 🍰 디저트는?")
    with st.container(border=True):
        st.pills("달달한 거 하나 골라줘", DESSERTS + ss.custom_desserts, key="dessert")
        custom_input("✏️ 먹고 싶은 디저트 직접 추가", "예) 붕어빵, 마카롱", "new_dessert", "custom_desserts", "dessert", multi=False)
        st.text_area(
            "나한테 하고 싶은 말 💬",
            placeholder="예) 맛있는 거 사줘 😋",
            max_chars=200,
            key="message",
        )
    nav(next_disabled=not ss.dessert)


def plan_text() -> str:
    d = ss.date
    lines = [
        "💖 데이트 확인서 💖",
        "",
        f"📅 날짜 : {d.year}년 {d.month}월 {d.day}일 ({'월화수목금토일'[d.weekday()]})",
        f"⏰ 시간 : {time_text()}",
        f"🍽️ 식사 : {ss.food}",
        f"🗺️ 코스 : {' → '.join(ss.places)}",
        f"🍰 디저트 : {ss.dessert}",
    ]
    if ss.message.strip():
        lines += ["", f"💬 한마디 : {ss.message.strip()}"]
    lines += ["", "위 내용으로 데이트를 약속합니다. 🤙 꼭 지키기!"]
    return "\n".join(lines)


def page_done() -> None:
    progress()
    if not ss.get("celebrated"):
        st.balloons()
        ss.celebrated = True
    st.markdown("<h1>🎉 데이트 확정! 🎉</h1>", unsafe_allow_html=True)
    with st.container(border=True):
        st.html('<div style="text-align:center;font-size:3.5rem">💑</div>')
        st.markdown(plan_text().replace("\n", "  \n"))
    st.download_button(
        "💾 확인서 저장하기",
        data=plan_text(),
        file_name="데이트_확인서.txt",
        type="primary",
        width="stretch",
    )
    left, right = st.columns(2)
    left.button("← 수정하기", on_click=go, args=(4,), width="stretch")
    right.button("처음부터 다시", on_click=restart, width="stretch")


PAGES = [page_ask, page_date, page_food, page_place, page_dessert, page_done]
if ss.step != len(PAGES) - 1:
    ss.celebrated = False
PAGES[ss.step]()
