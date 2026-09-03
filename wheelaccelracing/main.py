# -*- coding: utf-8 -*-
"""휠 액셀 레이싱 (Streamlit)

Canvas + 순수 JavaScript로 만든 실시간 탑다운 드리프트 레이싱 게임(game.html)을
st.components.v1.html()로 그대로 임베드한다. 물리 연산·렌더링·입력 처리는 전부
브라우저 안의 JS로 돌아가고, Streamlit은 페이지 틀과 배포만 담당한다 — 마우스 휠과
키보드를 프레임 단위로 받아야 하는 실시간 게임이라 Streamlit 자체 rerun 방식으로는
재구현이 불가능하기 때문.
"""
import os

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="휠 액셀 레이싱", page_icon="🏎️", layout="wide")

GAME_HTML_PATH = os.path.join(os.path.dirname(__file__), "game.html")

st.markdown(
    """
    <style>
    .stApp{background:#1a1d24;}
    header[data-testid="stHeader"]{background:transparent;}
    .block-container{padding-top:1.2rem; padding-bottom:1rem; max-width:1000px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏎️ 휠 액셀 레이싱")
st.caption("마우스 휠 = 가속/브레이크, WASD = 조향, Space = 드리프트 — 기록은 이 브라우저에만 저장됩니다.")

with open(GAME_HTML_PATH, "r", encoding="utf-8") as f:
    game_html = f.read()

components.html(game_html, height=760, scrolling=False)

with st.expander("📖 조작법"):
    st.markdown(
        """
        - **마우스 휠 위로 굴리기** : 가속 (계속 굴려야 속도 유지 — 페달처럼 스프링백됩니다)
        - **마우스 휠 아래로 굴리기** : 브레이크 / 후진
        - **A / D** : 좌우 조향
        - **W / S** : 보조 가속 / 브레이크 (휠 대신 사용 가능)
        - **Space** : 핸드브레이크(드리프트) — 슬립 각도·속도에 따라 콤보가 쌓이고, 떼는 순간 부스트
        - **R** : 재시작
        - 3랩을 완주하면 총 기록과 베스트 랩이 표시됩니다.
        """
    )
