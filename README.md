# 📚 mystudy

데이터 분석을 공부하면서 만든 연습 노트 저장소입니다. 개념 카드, 코드 연습, 퀴즈로 회귀·분류부터 pandas 전처리와 시각화까지 익힐 수 있게 만들었습니다.

- **바로 열기:** https://skn35shimsungwook.github.io/mystudy/ml_study_playground.html

## 따로 옮긴 프로젝트

예전에는 미니 게임도 이 저장소에 함께 넣었는데, 저장소 하나에 성격이 다른 것들이 섞여서 찾기 어려웠습니다. 그래서 프로젝트마다 저장소를 나눴습니다.

| 프로젝트 | 저장소 | 바로 열기 |
|---|---|---|
| ⚾ 몰래 야구 홈런더비 | [baseballhomerun](https://github.com/SKN35shimsungwook/baseballhomerun) | [게임](https://skn35shimsungwook.github.io/baseballhomerun/game.html) |
| 🕸️ 스파이더맨 웹스윙 3D | [spider](https://github.com/SKN35shimsungwook/spider) | [게임](https://skn35shimsungwook.github.io/spider/) |
| 🏎️ 휠 액셀 카레이싱 | [wheelaccelracing](https://github.com/SKN35shimsungwook/wheelaccelracing) | [게임](https://skn35shimsungwook.github.io/wheelaccelracing/game.html) |

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

## 왜 파일이 이렇게 적어 보이나요?

이 폴더는 원래 제 개인 작업 폴더(강의 자료, API 키, 캡처 이미지 등)와 같이 쓰고 있었습니다. 그래서 `.gitignore`에서 **기본적으로 전부 무시하고 노트 파일만 골라서 허용**해 두었습니다. 제 PC에는 더 많은 파일이 있지만, GitHub에는 노트 관련 파일만 올렸습니다.

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
