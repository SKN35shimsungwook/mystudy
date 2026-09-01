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

---

🤖 이 저장소의 README는 Claude Code와 함께 작성했어요.
