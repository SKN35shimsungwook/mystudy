# -*- coding: utf-8 -*-
"""몰래 야구 - 홈런더비 (Streamlit)

두 가지 모드를 제공:
  1. "풀 게임" 탭 — 원본 캔버스 게임(game.html, 구 sneak_baseball.html)을
     st.components.v1.html()로 그대로 임베드. 파티클/혜성 궤적/배트 크기 변화
     등 지금까지 만든 모든 시각 연출이 원본 그대로 살아있음. 대신 저장은
     이 iframe 안의 localStorage라서 이 브라우저에서만 유지됨.
  2. "서버 랭킹전" 탭 — 위 게임의 판정 규칙·강화 시스템·버닝 라운드·반사
     크리티컬·점수 공식을 logic.py로 이식한 순수 Streamlit 버전. 캔버스
     연출은 없지만, TOP 5가 data/history.json 파일에 저장되어 접속하는
     모든 사람이 진짜로 같은 랭킹을 공유함.
"""
import os
import random
import time

import streamlit as st
import streamlit.components.v1 as components

import logic

st.set_page_config(page_title="몰래 야구 - 홈런더비", page_icon="⚾", layout="centered")

GAME_HTML_PATH = os.path.join(os.path.dirname(__file__), "game.html")

st.markdown(
    """
    <style>
    .stApp{background:#0b0d12;color:#e9ebf1;}
    .scorebar{display:flex;justify-content:space-around;padding:12px 4px;
              background:#12151d;border-radius:10px;border:1px solid #2a3142;margin:10px 0;}
    .scorebar .stat{text-align:center;}
    .scorebar .num{font-size:1.3rem;font-weight:800;}
    .scorebar .label{font-size:.68rem;color:#9aa2b4;letter-spacing:.05em;}
    .hr-num{color:#5fbf77;} .hit-num{color:#e0a83e;} .out-num{color:#e2543f;}
    .pip-row{text-align:center;color:#5b6376;font-size:.85rem;letter-spacing:.15em;margin-bottom:4px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- 세션 상태

if "initialized" not in st.session_state:
    st.session_state.phase = "idle"  # idle | pitching | result | burnoffer | gameover
    st.session_state.stats = {"hr": 0, "hit": 0, "out": 0, "best": 0, "score": 0}
    st.session_state.difficulty = 0.0
    st.session_state.recent_errors = []
    st.session_state.strike_count = 0
    st.session_state.ball_count = 0
    st.session_state.burning = False
    st.session_state.burn_offered = False
    st.session_state.bat = logic.load_bat()
    st.session_state.nickname = ""
    st.session_state.result_message = ""
    st.session_state.last_balloons = False
    st.session_state.disguise = False
    st.session_state.enhance_msg = ""
    st.session_state.made_top = False
    st.session_state.earned_points = 0
    st.session_state.initialized = True

s = st.session_state


def tier_name(level: int) -> str:
    if level >= 9:
        return "파이널 티어"
    if level >= 6:
        return "파이어 티어"
    if level >= 1:
        return "강화 티어"
    return "기본"


def reset_game():
    s.phase = "idle"
    s.stats = {"hr": 0, "hit": 0, "out": 0, "best": 0, "score": 0}
    s.difficulty = 0.0
    s.recent_errors = []
    s.strike_count = 0
    s.ball_count = 0
    s.burning = False
    s.burn_offered = False
    s.result_message = ""


def start_pitch():
    s.pitch_duration_ms = logic.compute_pitch_duration_ms(s.difficulty, s.recent_errors)
    diff_t = min(1.0, s.difficulty / 10)
    s.pitch_is_ball = random.random() < (0.38 + diff_t * 0.12)
    s.pitch_start = time.time()
    s.phase = "pitching"
    s.result_message = ""


def end_game():
    s.phase = "gameover"
    s.made_top = logic.submit_score(
        s.nickname, s.stats["score"], s.stats["hr"], s.stats["hit"], s.stats["best"]
    )
    earned = max(1, s.stats["score"] // 20) if s.stats["score"] > 0 else 0
    s.bat["points"] += earned
    logic.save_bat(s.bat)
    s.earned_points = earned


def commit_result(kind: str, distance: int = 0, is_perfect: bool = False, swung: bool = True):
    bat = s.bat
    score_mult = logic.score_multiplier(bat["level"])
    terminal = True
    message = ""
    balloons = False

    if kind == "hr":
        s.difficulty = min(12.0, s.difficulty + 1.3)
        s.stats["hr"] += 1
        s.stats["best"] = max(s.stats["best"], distance)
        pts = round(distance * 2 * score_mult)
        if s.burning:
            pts *= 2
        s.stats["score"] += pts
        crit = bat["level"] >= 9
        message = (
            f"{'💥 CRITICAL! ' if crit else '🎉 '}홈런! {distance}m (+{pts}점)"
            f"{' 🔥' if s.burning else ''} · {tier_name(bat['level'])}"
        )
        balloons = True

        # +9~+11 완벽 타이밍 홈런: 벽 맞고 돌아온 공이 50% 확률로 타자를 맞춰
        # 반사 크리티컬(점수 2배 추가)
        if crit and is_perfect:
            if random.random() < 0.5:
                s.stats["score"] += pts
                message += "\n\n💥 반사 크리티컬! 점수 2배!"
            else:
                message += "\n\n(벽 맞고 돌아온 공이 타자를 비껴감)"

    elif kind == "hit":
        s.difficulty = min(12.0, s.difficulty + 0.7)
        s.stats["hit"] += 1
        s.stats["best"] = max(s.stats["best"], distance)
        pts = round(distance * score_mult)
        if s.burning:
            pts *= 2
        s.stats["score"] += pts
        message = f"안타! {distance}m (+{pts}점){' 🔥' if s.burning else ''}"

    elif kind == "flyout":
        s.difficulty = max(0.0, s.difficulty - 0.4)
        s.stats["out"] += 1
        s.burning = False
        message = "플라이아웃…"

    elif kind == "strike":
        s.strike_count += 1
        if s.strike_count >= 3:
            s.difficulty = max(0.0, s.difficulty - 0.8)
            s.burning = False
            s.stats["out"] += 1
            s.strike_count = 0
            s.ball_count = 0
            message = "⚾ 삼진 아웃!"
        else:
            terminal = False
            message = f"스트라이크 ({s.strike_count}/3) — {'헛스윙' if swung else '루킹'}"

    else:  # 'ball'
        s.ball_count += 1
        if s.ball_count >= 4:
            s.strike_count = 0
            s.ball_count = 0
            message = "포볼! (4구, 출루)"
        else:
            terminal = False
            message = f"볼 ({s.ball_count}/4)"

    if terminal:
        s.strike_count = 0
        s.ball_count = 0

    s.result_message = message
    s.last_balloons = balloons
    s.phase = "result"

    if s.stats["out"] >= logic.OUT_LIMIT:
        if not s.burn_offered and not s.burning and bat["points"] >= logic.BURN_COST:
            s.phase = "burnoffer"
        else:
            end_game()


def attempt_swing():
    now = time.time()
    diff_ms = (now - s.pitch_start) * 1000 - s.pitch_duration_ms
    abs_diff = abs(diff_ms)

    s.recent_errors.append(diff_ms)
    if len(s.recent_errors) > 8:
        s.recent_errors.pop(0)

    hr_w, hit_w, fly_w = logic.compute_windows(s.difficulty, s.bat["level"])
    kind = logic.classify_swing(abs_diff, hr_w, hit_w, fly_w)
    is_perfect = logic.is_perfect_timing(abs_diff, hr_w)

    if kind == "hr":
        commit_result("hr", logic.roll_hr_distance(s.bat["level"]), is_perfect, swung=True)
    elif kind == "hit":
        commit_result("hit", logic.roll_hit_distance(s.bat["level"]), swung=True)
    elif kind == "flyout":
        commit_result("flyout", swung=True)
    else:
        commit_result("strike", swung=True)


def take_pitch():
    if s.pitch_is_ball:
        commit_result("ball", swung=False)
    else:
        commit_result("strike", swung=False)


def burn_accept():
    s.burn_offered = True
    s.bat["points"] -= logic.BURN_COST
    logic.save_bat(s.bat)
    s.burning = True
    s.stats["out"] -= 1
    s.phase = "result"
    s.result_message = "🔥 버닝! 이후 얻는 점수가 2배!"


def burn_decline():
    s.burn_offered = True
    end_game()


def try_enhance():
    bat = s.bat
    if bat["level"] >= logic.BAT_MAX:
        return
    cost = logic.enhance_cost(bat["level"])
    if bat["points"] < cost:
        return
    bat["points"] -= cost
    if random.random() < logic.enhance_chance(bat["level"]):
        bat["level"] += 1
        s.enhance_msg = f"✨ 강화 성공! +{bat['level']}"
    else:
        s.enhance_msg = "실패… 포인트만 소모됐어요"
    logic.save_bat(bat)


# ---------------------------------------------------------------- 타이틀바

top1, top2, top3 = st.columns([3, 1, 1])
with top1:
    s.nickname = st.text_input(
        "닉네임", value=s.nickname, placeholder="닉네임 (랭킹에 표시됨)", label_visibility="collapsed"
    )
with top2:
    with st.popover(f"🏏 +{s.bat['level']}", use_container_width=True):
        bat = s.bat
        st.markdown(f"**배트 강화** — {tier_name(bat['level'])}")
        st.write(f"현재: +{bat['level']} / {logic.BAT_MAX}")
        bonus_pct = round((logic.bat_distance_multiplier(bat["level"]) - 1) * 100)
        st.write(f"비거리 보너스: +{bonus_pct}%")
        st.write(f"보유 포인트: {bat['points']}P")
        if bat["level"] >= logic.BAT_MAX:
            st.success("최대 강화 완료!")
        else:
            cost = logic.enhance_cost(bat["level"])
            chance = logic.enhance_chance(bat["level"])
            chance_label = f"{chance*100:.1f}%" if chance * 100 < 1 else f"{round(chance*100)}%"
            st.write(f"필요 포인트: {cost}P · 성공 확률: {chance_label}")
            if st.button(
                f"강화하기 ({cost}P)",
                use_container_width=True,
                disabled=bat["points"] < cost,
                key="enhance_btn",
            ):
                try_enhance()
                st.rerun()
        if s.enhance_msg:
            st.caption(s.enhance_msg)
with top3:
    s.disguise = st.toggle("🙈", value=s.disguise, help="위장 모드")

if s.disguise:
    st.markdown("### 주간 정기 회의록")
    st.markdown(
        "1. 지난 스프린트 회고 공유\n"
        "2. 2분기 로드맵 우선순위 재정렬\n"
        "3. 리소스 배분 및 일정 조정\n"
        "4. 다음 주 액션 아이템 확정"
    )
    st.stop()

st.title("⚾ 몰래 야구 - 홈런더비")

with st.expander("📖 게임 설명"):
    st.markdown(
        f"""
        - **조작**: 투구 시작 후 "스윙!"을 누른 시점과 실제 목표 시점의 차이(ms)로 판정.
        - **판정**: 정확히 맞으면 홈런, 살짝 빗나가면 안타, 어중간하면 플라이아웃(즉시 아웃),
          완전히 빗나가거나 안 치면 스트라이크.
        - **볼/스트라이크**: 스트라이크 3개 = 삼진 아웃. 주황 공을 "보내기"로 흘려보내면 볼,
          4개 모이면 포볼(출루).
        - **난이도**: 잘 칠수록 투구가 빨라지고 판정 범위도 좁아짐. 못 치면 다시 관대해짐.
        - **점수**: 안타는 비거리만큼, 홈런은 비거리×2점 — 여기에 배트 강화 배율이 곱해짐.
          아웃 {logic.OUT_LIMIT}개면 게임 종료.
        - **배트 강화**: 게임이 끝나면 총점만큼 강화 포인트 획득. 🏏 메뉴에서 뽑기식으로
          강화(+{logic.BAT_MAX}까지). +9강부터는 완벽한 타이밍의 홈런에 한해 50% 확률로
          점수가 한 번 더 2배가 되는 "반사 크리티컬"이 터짐.
        - **버닝 라운드**: 5번째 아웃 순간 포인트가 {logic.BURN_COST}P 이상 있으면, 그 포인트를
          태워 보너스 타석에 도전할 수 있음. 이후 점수가 2배로 적용됨(계속 성공하면 계속 이어짐).
        - **랭킹**: TOP 5는 이 서버의 파일에 저장돼서, 접속하는 모든 사람이 같은 랭킹을 봄.
        """
    )

# ---------------------------------------------------------------- 탭 분기

tab_full, tab_server = st.tabs(["🎮 풀 게임 (원본)", "📊 서버 랭킹전"])

with tab_full:
    st.caption("파티클·혜성 궤적·배트 강화 이펙트까지 원본 그대로. 기록은 이 브라우저에만 저장됨(localStorage).")
    with open(GAME_HTML_PATH, "r", encoding="utf-8") as f:
        game_html = f.read()
    # 원본은 Artifact 위에 투명하게 떠 있도록 만들어졌지만, 여기선 배경을
    # 직접 깔아줘야 카드의 반투명 유리 효과가 washed-out 되지 않음.
    game_html = game_html.replace("background:transparent;", "background:#0b0d12;", 1)
    components.html(game_html, height=640, scrolling=False)

with tab_server:
    st.caption("판정·강화·버닝 라운드 규칙은 동일. TOP 5는 이 서버의 모든 접속자가 공유함.")

    # ------------------------------------------------------------ 스코어보드
    st.markdown(
        f"""
        <div class="scorebar">
          <div class="stat"><div class="num hr-num">{s.stats['hr']}</div><div class="label">홈런</div></div>
          <div class="stat"><div class="num hit-num">{s.stats['hit']}</div><div class="label">안타</div></div>
          <div class="stat"><div class="num out-num">{s.stats['out']}/{logic.OUT_LIMIT}</div><div class="label">아웃</div></div>
          <div class="stat"><div class="num">{s.stats['best']}m</div><div class="label">최고비거리</div></div>
          <div class="stat"><div class="num">{s.stats['score']}</div><div class="label">총점</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"아웃 {logic.OUT_LIMIT}개면 종료 · 난이도 {s.difficulty:.1f}")

    if s.phase in ("pitching", "result"):
        st.markdown(
            f"<div class='pip-row'>S {'●' * s.strike_count}{'○' * (3 - s.strike_count)}"
            f"&nbsp;&nbsp;&nbsp;B {'●' * s.ball_count}{'○' * (4 - s.ball_count)}</div>",
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------ 메인 화면
    if s.phase == "idle":
        if st.button("⚾ 투구 시작", use_container_width=True, type="primary"):
            start_pitch()
            st.rerun()

    elif s.phase == "pitching":
        duration_s = s.pitch_duration_ms / 1000
        ball_color = "#e8a355" if s.pitch_is_ball else "#eee7d6"
        components.html(
            f"""
            <div style="position:relative;height:34px;background:#12151d;border-radius:8px;
                         overflow:hidden;border:1px solid #2a3142;">
              <div style="position:absolute;top:50%;left:0;width:12px;height:12px;margin-top:-6px;
                           border-radius:50%;background:{ball_color};box-shadow:0 0 8px {ball_color};
                           animation:pitchmove {duration_s}s linear forwards;"></div>
            </div>
            <style>
              @keyframes pitchmove {{ from{{left:0%}} to{{left:calc(100% - 12px)}} }}
            </style>
            """,
            height=44,
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("스윙! 🏏", use_container_width=True, type="primary"):
                attempt_swing()
                st.rerun()
        with c2:
            if st.button("보내기 (안 치기)", use_container_width=True):
                take_pitch()
                st.rerun()

    elif s.phase == "result":
        st.info(s.result_message)
        if s.last_balloons:
            st.balloons()
            s.last_balloons = False
        if st.button("다음 투구 ▶", use_container_width=True, type="primary"):
            start_pitch()
            st.rerun()

    elif s.phase == "burnoffer":
        st.warning(
            f"🔥 **보너스 라운드?**\n\n포인트 {logic.BURN_COST}P를 태우면 보너스 타석에 도전 — "
            f"성공하면 이후 점수 2배!\n\n보유 포인트: {s.bat['points']}P"
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔥 태우기", use_container_width=True, type="primary", disabled=s.bat["points"] < logic.BURN_COST):
                burn_accept()
                st.rerun()
        with c2:
            if st.button("그냥 종료", use_container_width=True):
                burn_decline()
                st.rerun()

    elif s.phase == "gameover":
        st.error(f"GAME OVER — 총점 {s.stats['score']}점")
        st.write(f"홈런 {s.stats['hr']} · 안타 {s.stats['hit']} · 최고 {s.stats['best']}m")
        if s.made_top:
            st.success("🏆 TOP 5 진입!")
        st.write(f"🏏 강화 포인트 +{s.earned_points}")

        st.markdown("#### 🏆 TOP 5 (전체 공유 랭킹)")
        history = logic.load_history()
        if history:
            for i, h in enumerate(history, 1):
                st.write(f"{i}. **{h['nickname']}** — {h['score']}점 (홈런 {h['hr']} · 안타 {h['hit']})")
        else:
            st.write("아직 기록이 없습니다.")

        if st.button("다시 시작", use_container_width=True, type="primary"):
            reset_game()
            st.rerun()
