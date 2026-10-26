# 📚 mystudy

**⚾ 야구 홈런 게임(baseballhomerun) 바로 실행해 보기:** https://kodq7fgdwnrozkw5npbcin.streamlit.app

데이터 분석을 공부하면서 만든 연습 노트와, 쉬어 가는 겸 만든 미니 게임 몇 개를 모아 둔 제 공부 저장소입니다.

## 🔗 클릭하면 바로 열리는 페이지

GitHub에서 `.html` 파일을 누르면 코드만 보여서, GitHub Pages 주소로 바로 열리게 모아 두었어요.

| 페이지 | 바로 열기 | 파일 |
|---|---|---|
| 🧭 장고 가이드 모음 (시작 페이지) | [열기](https://skn35shimsungwook.github.io/mystudy/django_guide/index.html) | [`django_guide/index.html`](./django_guide/index.html) |
| 🍪 장고 첫걸음: 간식 투표 앱 튜토리얼 | [열기](https://skn35shimsungwook.github.io/mystudy/django_guide/%EC%9E%A5%EA%B3%A0_%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC.html) | [`django_guide/장고_튜토리얼.html`](./django_guide/%EC%9E%A5%EA%B3%A0_%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC.html) |
| 🗺️ 장고 앱 출시 지도 | [열기](https://skn35shimsungwook.github.io/mystudy/django_guide/%EC%9E%A5%EA%B3%A0_%EC%95%B1%EA%B0%9C%EB%B0%9C_%EC%B6%9C%EC%8B%9C_%EA%B0%80%EC%9D%B4%EB%93%9C.html) | [`django_guide/장고_앱개발_출시_가이드.html`](./django_guide/%EC%9E%A5%EA%B3%A0_%EC%95%B1%EA%B0%9C%EB%B0%9C_%EC%B6%9C%EC%8B%9C_%EA%B0%80%EC%9D%B4%EB%93%9C.html) |
| 🏗️ 최종 프로젝트 구조도 · 8주 일정표 | [열기](https://skn35shimsungwook.github.io/mystudy/django_guide/%EC%B5%9C%EC%A2%85%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EA%B5%AC%EC%A1%B0%EB%8F%84_%EC%9D%BC%EC%A0%95%ED%91%9C.html) | [`django_guide/최종프로젝트_구조도_일정표.html`](./django_guide/%EC%B5%9C%EC%A2%85%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8_%EA%B5%AC%EC%A1%B0%EB%8F%84_%EC%9D%BC%EC%A0%95%ED%91%9C.html) |
| 💰 내 앱 출시 · 수익화 계획 | [열기](https://skn35shimsungwook.github.io/mystudy/django_guide/%EC%95%B1%EC%B6%9C%EC%8B%9C_%EC%88%98%EC%9D%B5%ED%99%94_%EA%B3%84%ED%9A%8D.html) | [`django_guide/앱출시_수익화_계획.html`](./django_guide/%EC%95%B1%EC%B6%9C%EC%8B%9C_%EC%88%98%EC%9D%B5%ED%99%94_%EA%B3%84%ED%9A%8D.html) |
| 🧮 데이터 분석 전체 연습 노트 | [열기](https://skn35shimsungwook.github.io/mystudy/ml_study_playground.html) | [`ml_study_playground.html`](./ml_study_playground.html) |
| ⚾ 몰래 야구 홈런더비 | [열기](https://skn35shimsungwook.github.io/mystudy/baseballhomerun/game.html) | [`baseballhomerun/game.html`](./baseballhomerun/game.html) |
| 🕸️ 스파이더맨 웹스윙 3D | [열기](https://skn35shimsungwook.github.io/mystudy/spiderwebswing/game.html) | [`spiderwebswing/game.html`](./spiderwebswing/game.html) |
| 🏎️ 휠 액셀 카레이싱 | [열기](https://skn35shimsungwook.github.io/mystudy/wheelaccelracing/game.html) | [`wheelaccelracing/game.html`](./wheelaccelracing/game.html) |

## 이 저장소에는 뭐가 있나요?

### 🧮 데이터 분석 전체 연습 노트 (메인)

`ml_study_playground.html` / `.py` / `.ipynb`

회귀·분류 같은 개념부터 데이터 수집, pandas 전처리, 시각화까지 **개념 카드 + 코드 연습 + 퀴즈**로
익히는 학습 노트예요. 두 가지 방식으로 볼 수 있어요:

- **PWA(웹앱)로 설치해서 보기**: `manifest.json` / `sw.js` / `icons/`가 이 파일을 스마트폰이나
  PC에 앱처럼 설치할 수 있게 해줘요.
- **Streamlit으로 실행하기**:
  ```bash
  streamlit run ml_study_playground.py
  ```

### 🧭 장고 가이드 (`django_guide/`)

Streamlit을 쓰던 제가 최종 프로젝트에서 장고를 쓰려고 만든 정리예요. 간식 투표 튜토리얼, 장고 앱 출시 지도, 최종 프로젝트 구조도·8주 일정표, 캠프 이후 앱 출시·수익화 계획까지 순서대로 이어져요. 수업 교재 요약 PDF는 강사님 자료 보호를 위해 올리지 않았어요.

### 🎮 보너스: 미니 게임 (Streamlit 임베드)

공부하다 지칠 때 만든 게임들입니다. HTML/JS로 만든 게임을 `st.components.v1.html()`로
Streamlit 안에 그대로 넣은 구조예요.

| 폴더 | 내용 | 실행 |
|---|---|---|
| [`baseballhomerun/`](./baseballhomerun) | 몰래 야구 홈런더비 — 타이밍 맞춰 스윙하는 게임 + 서버 공유 랭킹전 | `streamlit run baseballhomerun/main.py` |
| [`spiderwebswing/`](./spiderwebswing) | 스파이더맨 웹스윙 3D — Three.js로 만든 실시간 3D 액션 게임 ([단독 저장소](https://github.com/SKN35shimsungwook/spider)도 있음) | `streamlit run spiderwebswing/main.py` |

## 왜 파일이 이렇게 적어 보이나요?

이 폴더는 원래 제 개인 작업 폴더(강의 자료, API 키, 캡처 이미지 등)와 같이 쓰고 있었습니다. 그래서 `.gitignore`에서 **기본적으로 전부 무시하고 위 파일들만 골라서 허용**해 두었습니다. 제 PC에는 더 많은 파일이 있지만, GitHub에는 위 항목들만 올렸습니다.

## 코드 구성

### `ml_study_playground.html` (핵심 콘텐츠)

탭 하나짜리 순수 HTML/CSS/JS 문서예요. 상단 `<nav class="tabs">`가 목차(회귀, 분류, 데이터 수집,
pandas 전처리, 시각화 등)이고, 각 탭 안에 **개념 카드 + 실행 가능한 코드 예제 + 퀴즈**가 순서대로
들어있어요. 다크/라이트 테마 전환은 `document.documentElement`의 `data-theme` 속성을 감시하는
`MutationObserver`로 처리해요.

### `ml_study_playground.py`

위 HTML을 그대로 읽어서 `st.components.v1.html()`로 띄우기만 하는 얇은 래퍼예요. 실제 로직은
전부 HTML/JS 쪽에 있어요.

### `manifest.json` / `sw.js` / `icons/`

PWA(설치형 웹앱) 구성 3종 세트예요. `manifest.json`이 앱 이름·아이콘·시작 페이지를 정의하고,
`sw.js`(서비스 워커)가 오프라인 캐싱을 담당해요.

### `baseballhomerun/logic.py`

Streamlit 화면 코드(`main.py`)와 분리된 **순수 게임 규칙 함수 모음**이에요. 스윙 타이밍 판정
(`classify_swing`), 배트 강화 확률·비용(`enhance_chance`, `enhance_cost`), 점수 배율
(`score_multiplier`), 랭킹 저장(`submit_score`, `load_history`) 같은 함수들이 UI 코드 없이
독립적으로 테스트 가능하게 분리돼 있어요.

## 만들면서 겪은 문제

직접 써 보고 배포하면서 실제로 부딪힌 문제와, 원인을 찾아 고친 방법을 적어 둡니다.

**GitHub에서 `ml_study_playground.html`을 직접 받아 폰 브라우저로 열면 한글이 깨짐**

- 원인: 원래 이 파일은 `<title>`과 `<style>`만 있고 `<!doctype html>`, `<head>`, `<meta charset="UTF-8">`가
  없는 "조각(fragment)" 상태였습니다. Streamlit의 `components.html()`은 이걸 `srcdoc`으로 감싸서
  항상 UTF-8로 해석하지만, GitHub에서 파일을 그대로 내려받아 열면 브라우저가 인코딩을 추측하다가
  한글이 깨지는 경우가 있었습니다.
- 해결: 파일을 완전한 HTML 문서로 감쌌습니다.

```diff
+<!doctype html>
+<html lang="ko">
+<head>
+<meta charset="UTF-8">
+<meta name="viewport" content="width=device-width, initial-scale=1">
 <title>데이터 분석 전체 연습 노트</title>
 <style> ... </style>
+</head>
+<body>

 <div class="app"> ... </div>

+</body>
+</html>
```
