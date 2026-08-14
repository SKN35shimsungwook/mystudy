# -*- coding: utf-8 -*-
"""몰래 야구 게임 규칙 — 순수 로직만 (Streamlit 의존 없음).

원본 HTML/캔버스 버전(sneak_baseball.html)의 수치와 판정 규칙을 그대로 옮김.
Streamlit은 프레임 단위로 캔버스를 그릴 수 없어서 시각 연출(파티클, 혜성 궤적,
배트 크기 애니메이션 등)은 옮기지 않고, 판정/점수/강화/버닝 로직만 이식했음.

이 모듈은 순수 함수 위주라 baseballhomerun.ipynb에서 바로 import해서 실험 가능.
"""
import json
import os
import random

OUT_LIMIT = 5
BAT_MAX = 11
BURN_COST = 50

# 강화 레벨(0~10)에서 한 단계 올릴 확률 — index = 현재 레벨
ENHANCE_CHANCE = [0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.25, 0.10, 0.01, 0.005, 0.001]

# 레벨별 점수 배율 — +1~5는 완만, +6~8은 확 뜀, +9~11은 "크리티컬" 구간
SCORE_MULT = [1, 1.5, 2, 2.5, 3, 3.5, 5, 6.5, 8, 12, 18, 26]

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
BAT_FILE = os.path.join(DATA_DIR, "bat.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")


def enhance_cost(level: int) -> int:
    """다음 강화 시도에 필요한 포인트."""
    return 30 + level * 15


def enhance_chance(level: int) -> float:
    """다음 강화 시도의 성공 확률 (0~1)."""
    if 0 <= level < len(ENHANCE_CHANCE):
        return ENHANCE_CHANCE[level]
    return 0.0


def score_multiplier(level: int) -> float:
    if 0 <= level < len(SCORE_MULT):
        return SCORE_MULT[level]
    return SCORE_MULT[-1]


def bat_distance_multiplier(level: int) -> float:
    """비거리 배율 — 원본 batMultiplier()와 동일 공식."""
    if level <= 0:
        return 1.0
    if level <= 5:
        return 1 + level * 0.05
    return 1.25 + (level - 5) * 0.12


def compute_windows(difficulty: float, bat_level: int):
    """난이도(0~12)에 따라 좁아지고, 배트 레벨(+4부터)에 따라 살짝 넓어지는
    판정 범위(ms)를 반환: (hr_window, hit_window, flyout_window)."""
    diff_t = min(1.0, difficulty / 10)
    hr_window = 45 - diff_t * 19
    hit_window = 130 - diff_t * 45
    flyout_window = 180 - diff_t * 60

    bat_bonus = 1 + max(0, bat_level - 3) * 0.03
    return hr_window * bat_bonus, hit_window * bat_bonus, flyout_window * bat_bonus


def compute_pitch_duration_ms(difficulty: float, recent_errors: list) -> float:
    """난이도가 오를수록 더 빠르고 좁은 범위에서 투구 시간을 뽑고,
    최근 스윙이 이르거나/늦은 쪽으로 치우쳐 있으면 그 반대로 살짝 밀어줌."""
    diff_t = min(1.0, difficulty / 10)
    min_dur = 480 - diff_t * 180
    max_dur = 1000 - diff_t * 300
    if max_dur < min_dur + 140:
        max_dur = min_dur + 140
    base_dur = min_dur + random.random() * (max_dur - min_dur)

    bias = 0.0
    if len(recent_errors) >= 3:
        bias = sum(recent_errors) / len(recent_errors)

    return max(260.0, base_dur - bias * 0.5)


def classify_swing(abs_diff_ms: float, hr_window: float, hit_window: float, flyout_window: float) -> str:
    """스윙 시점과 목표 시점의 차이(ms, 절댓값)로 결과 분류."""
    if abs_diff_ms <= hr_window:
        return "hr"
    if abs_diff_ms <= hit_window:
        return "hit"
    if abs_diff_ms <= flyout_window:
        return "flyout"
    return "strike"


def roll_hr_distance(bat_level: int) -> int:
    base = 95 + random.randint(0, 55)
    return round(base * bat_distance_multiplier(bat_level))


def roll_hit_distance(bat_level: int) -> int:
    base = 12 + random.randint(0, 78)
    return round(base * bat_distance_multiplier(bat_level))


def is_perfect_timing(abs_diff_ms: float, hr_window: float) -> bool:
    """완벽 타이밍 — 홈런 판정 범위의 1/4 이내로 정확히 맞춘 경우."""
    return abs_diff_ms <= hr_window * 0.25


# ---------------------------------------------------------------- 파일 저장

def _load_json(path: str, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(path: str, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_bat() -> dict:
    return _load_json(BAT_FILE, {"level": 0, "points": 0})


def save_bat(bat: dict) -> None:
    _save_json(BAT_FILE, bat)


def load_history() -> list:
    """서버 파일에 저장되는 TOP 5 — 같은 Streamlit 서버에 접속하는 모든
    사용자가 공유하는 랭킹. localStorage와 달리 진짜 공용 랭킹이 가능함."""
    history = _load_json(HISTORY_FILE, [])
    return history if isinstance(history, list) else []


def save_history(history: list) -> None:
    _save_json(HISTORY_FILE, history[:5])


def submit_score(nickname: str, score: int, hr: int, hit: int, dist: int) -> bool:
    """이번 게임 결과를 공용 TOP 5에 반영. TOP 5에 들었으면 True."""
    history = load_history()
    entry = {"nickname": nickname or "익명", "score": score, "hr": hr, "hit": hit, "dist": dist}
    history.append(entry)
    history.sort(key=lambda h: h["score"], reverse=True)
    made_top = entry in history[:5]
    save_history(history)
    return made_top
