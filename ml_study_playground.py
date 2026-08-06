# -*- coding: utf-8 -*-
"""데이터 분석 전체 연습 노트 — Streamlit 실행용 래퍼

실제 콘텐츠(개념 카드, 코드 연습, 회귀/분류 놀이터, 퀴즈)는 같은 폴더의
ml_study_playground.html 에 있고, 이 스크립트는 그 파일을 Streamlit 안에서
그대로 띄워주는 역할만 한다.

실행:
    streamlit run ml_study_playground.py
"""
import os

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="데이터 분석 전체 연습 노트", page_icon="🧮", layout="wide")

_HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ml_study_playground.html")

with open(_HTML_PATH, "r", encoding="utf-8") as f:
    _html = f.read()

components.html(_html, height=1400, scrolling=True)
