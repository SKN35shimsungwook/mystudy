# 📚 mystudy

데이터 분석을 공부하면서 만든 연습 노트와, 쉬어가는 겸 만든 미니 게임 몇 개를 모아둔 저장소예요.

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

### 🎮 보너스: 미니 게임 (Streamlit 임베드)

공부하다 지칠 때 만든 게임들이에요. HTML/JS로 만든 게임을 `st.components.v1.html()`로
Streamlit 안에 그대로 넣은 구조예요.

| 폴더 | 내용 | 실행 |
|---|---|---|
| [`baseballhomerun/`](./baseballhomerun) | 몰래 야구 홈런더비 — 타이밍 맞춰 스윙하는 게임 + 서버 공유 랭킹전 | `streamlit run baseballhomerun/main.py` |
| [`spiderwebswing/`](./spiderwebswing) | 스파이더맨 웹스윙 3D — Three.js로 만든 실시간 3D 액션 게임 ([단독 저장소](https://github.com/SKN35shimsungwook/spider)도 있음) | `streamlit run spiderwebswing/main.py` |

## 왜 파일이 이렇게 적어 보여요?

이 저장소는 원래 훨씬 많은 개인 작업 폴더(강의 자료, API 키, 캡처 이미지 등)와 같은 폴더를 공유하고
있어서, `.gitignore`에서 **기본적으로 전부 무시하고 위 파일들만 명시적으로 허용**해뒀어요. 그래서
실제 로컬 폴더에는 더 많은 파일이 있어도, 이 저장소(GitHub)에는 위 항목들만 올라와 있어요.

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

## 트러블슈팅

**GitHub에서 `ml_study_playground.html`을 직접 받아 폰 브라우저로 열면 한글이 깨짐**

- 원인: 원래 이 파일은 `<title>`과 `<style>`만 있고 `<!doctype html>`, `<head>`, `<meta charset="UTF-8">`가
  없는 "조각(fragment)" 상태였어요. Streamlit의 `components.html()`은 이걸 `srcdoc`으로 감싸서
  항상 UTF-8로 해석하지만, GitHub에서 파일을 그대로 내려받아 열면 브라우저가 인코딩을 추측하다가
  한글이 깨지는 경우가 있었어요.
- 해결: 파일을 완전한 HTML 문서로 감쌈.

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

---

🤖 이 저장소의 README는 Claude Code와 함께 작성했어요.
