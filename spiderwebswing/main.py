# -*- coding: utf-8 -*-
"""스파이더멘 웹스윙 3D (Streamlit)

Three.js로 만든 실시간 3D 웹스윙 게임(game.html)을 st.components.v1.html()로
그대로 임베드. 물리 연산·렌더링·입력 처리는 전부 브라우저 안의 JS로 돌아가고,
Streamlit은 페이지 틀과 배포만 담당한다 — 실시간 물리/조작감이 필요한 게임이라
Streamlit 자체 rerun 방식으로는 재구현이 불가능하기 때문.
"""
import os

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="스파이더멘 웹스윙 3D", page_icon="🕸️", layout="wide")

GAME_HTML_PATH = os.path.join(os.path.dirname(__file__), "game.html")

st.markdown(
    """
    <style>
    .stApp{background:#0a0c22;}
    header[data-testid="stHeader"]{background:transparent;}
    .block-container{padding-top:1.2rem; padding-bottom:1rem; max-width:1000px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🕸️ 스파이더멘 웹스윙 3D")
st.caption("웹스윙 · 벽타기 · 거리 착지 시 격투(스파이더 센스 회피) — 기록은 이 브라우저에만 저장됩니다.")

with open(GAME_HTML_PATH, "r", encoding="utf-8") as f:
    game_html = f.read()

components.html(game_html, height=760, scrolling=False)

with st.expander("📖 조작법"):
    st.markdown(
        """
        - **W** 걷기 · **A / D** 조준 · **스페이스바 / 클릭** 웹 발사(타깃 없으면 다이브)
        - 스윙 중 **A / D**로 커브, 뗄 때 관성으로 날아감 · **Shift** 웹지퍼(가까운 앵커로 순간 이동)
        - 건물에 부딪히면 벽타기, 거리에 착지하면 가끔 총잡이/검객이 나타나 격투 시작
        - 격투: **WASD** 이동 · **F** 펀치 · **클릭/스페이스** 웹 공격 · 적이 붉게 예고하면 **Shift**로 회피
        """
    )
