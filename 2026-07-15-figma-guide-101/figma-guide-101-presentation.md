# 피그마 가이드 101 — 온보딩 클래스
## PPT 슬라이드 아웃라인 (2025~2026, 신입/개발자/기획자 대상)

---

## Slide 1: 표지 (Cover)
**Visual**: 보라(#A259FF)~검정 그라디언트 배경에 피그마 로고. "Figma 101" 크게, 부제 중간.
**Key Points**:
- 피그마 가이드 101
- 온보딩 클래스
- "화면을 그린다 → 재사용 UI를 만든다"
**Speaker Notes**: 이 클래스의 목표는 피그마의 모든 기능을 외우는 게 아니라, 재사용 가능하고 일관된 UI를 협업으로 만드는 사고방식을 심는 것입니다. 오늘 흐름은 인터페이스 → Auto Layout → 컴포넌트 → 변수 → 프로토타입 → 개발 협업 순입니다.

---

## Slide 2: 목차 (Agenda)
**Visual**: 6개 블록 그리드(아이콘 포함).
**Key Points**:
- 피그마란? / 인터페이스
- 기본 도구 / Auto Layout
- 컴포넌트 / 변수·토큰
- 프로토타입 / Dev Mode
- 협업 / 신기능
- 단축키 & 로드맵
**Speaker Notes**: 각 파트는 개념 → 실습 → 자주 하는 실수 순서입니다. 실습 결과물이 매주 쌓여 4주 뒤엔 클릭 가능한 프로토타입과 핸드오프까지 완성됩니다.

---

## Slide 3: 피그마란 무엇인가
**Visual**: 브라우저 창 안에서 여러 커서가 동시에 편집하는 일러스트.
**Key Points**:
- 브라우저 기반, 설치 불필요
- 실시간 협업 (구글 문서처럼)
- 디자인 → 프로토타입 → 개발 핸드오프 한 곳에서
- UI3(2024) 인터페이스
**Speaker Notes**: 피그마와 Sketch/XD의 근본 차이는 실시간 협업과 클라우드입니다. 링크만으로 접근하고 여러 명이 동시에 편집합니다. 오늘은 Figma Design에 집중하고, FigJam·Slides·Make·Sites는 마지막에 소개합니다.

---

## Slide 4: 인터페이스 5개 영역
**Visual**: UI3 스크린샷에 5개 영역을 번호로 표시(캔버스/툴바/레이어/속성/페이지).
**Key Points**:
- 캔버스 · 툴바 · 레이어(좌) · 속성(우) · 페이지
- 이동/확대: 스페이스 드래그, Cmd+스크롤
**Speaker Notes**: 이 지도를 먼저 각인시키면 이후 실습이 쉽습니다. 레이어 패널의 이름을 의미 있게 짓는 습관을 첫 시간부터 강조하세요. 'Rectangle 47'은 협업의 적입니다.

---

## Slide 5: 기본 도구 & 프레임 vs 그룹
**Visual**: 프레임/도형/텍스트/펜 아이콘 + 프레임과 그룹 비교 도식.
**Key Points**:
- 프레임(F): 화면·컨테이너 기본 단위
- 그룹은 단순 묶음 → 프레임을 기본으로
- 도형 R/O, 텍스트 T, 펜 P
**Speaker Notes**: Auto Layout과 제약은 프레임에만 붙기 때문에, 처음부터 프레임을 기본 단위로 쓰도록 가르칩니다. 실습: 아이폰 프레임에 사각형·텍스트 배치.

---

## Slide 6: 제약(Constraints) — 반응형 기초
**Visual**: 프레임 리사이즈 시 Left/Right/Center로 요소가 따라가는 애니메이션 프레임.
**Key Points**:
- 프레임 크기 변화 시 자식의 위치 규칙
- Left/Right/Center/Scale, Top/Bottom
**Speaker Notes**: 카드 제목은 Left&Top, 닫기 버튼은 Right&Top으로 걸고 프레임을 넓혀보며 동작을 관찰합니다. 반응형의 첫걸음입니다.

---

## Slide 7: 섹션 구분 — Auto Layout (핵심)
**Visual**: "가장 중요한 장" 배지 + Flexbox 아이콘.
**Key Points**:
- Auto Layout = 피그마 학습의 분수령
- CSS Flexbox와 동일 개념
**Speaker Notes**: 여기서 대부분의 초보자가 도약합니다. 개발자에겐 특히 직관적입니다.

---

## Slide 8: Auto Layout 개념 (Flexbox 대응표)
**Visual**: 좌 Auto Layout 속성 / 우 CSS Flexbox 대응표.
**Key Points**:
- 방향=flex-direction, 간격=gap, 패딩=padding
- 정렬=justify/align
- Hug / Fill / Fixed = fit-content / flex:1 / 고정
**Speaker Notes**: Shift+A로 적용, 패딩 16·gap 8 설정. 텍스트를 길게 바꿔도 버튼이 자연스럽게 늘어나는지 확인시키세요. 그다음 세로 Auto Layout으로 카드 리스트를 만듭니다.

---

## Slide 9: Auto Layout이 중요한 이유
**Visual**: 절대좌표로 깨진 화면 vs Auto Layout으로 정렬된 화면 비교.
**Key Points**:
- 내용이 늘어도 패딩·간격 유지
- 재사용 컴포넌트의 전제 조건
- 절대 좌표 배치는 화면 바뀌면 깨짐
**Speaker Notes**: 가장 흔한 초보 실수가 모든 것을 절대 좌표로 두는 것입니다. Auto Layout을 먼저 가르쳐 이 습관을 원천 차단합니다.

---

## Slide 10: 컴포넌트(Component) & 인스턴스
**Visual**: 원본 1개 → 인스턴스 여러 개, 원본 수정 시 전체 반영 다이어그램.
**Key Points**:
- 원본(Main) → 인스턴스(Instance)
- 원본 수정 → 모든 인스턴스 자동 업데이트
- 만들기: Cmd/Ctrl+Alt+K
**Speaker Notes**: "두 번 이상 쓸 것 같으면 컴포넌트로." 복붙으로 20개를 만들고 색 하나 바꾸려 20번 수정하는 참사를 피하는 습관입니다.

---

## Slide 11: 배리언트(Variants) & 컴포넌트 속성
**Visual**: 버튼의 Primary/Secondary × Default/Disabled 매트릭스 + 속성 패널.
**Key Points**:
- 상태(Hover/Disabled/Size)를 한 세트로
- 속성: Boolean / Text / Instance swap / Variant
**Speaker Notes**: 버튼 하나에도 상태가 여럿입니다. 배리언트로 묶고 속성으로 전환합니다. 실습: Primary/Secondary + Default/Disabled 구성 후 인스턴스에서 상태 전환.

---

## Slide 12: 스타일(Styles) vs 변수(Variables)
**Visual**: 좌 스타일(복합값) / 우 변수(원자값+모드) 비교.
**Key Points**:
- 스타일: 색·타이포·이펙트 재사용(모드 없음)
- 변수: Color/Number/String/Boolean + Alias
- 변수 = 디자인 토큰의 피그마 구현
**Speaker Notes**: 초보자가 가장 헷갈리는 지점입니다. 복합값(그라디언트·타이포 세트)은 스타일, 단일 원자값+테마는 변수로 정리하세요. 현대 워크플로우는 변수를 토큰의 근간으로 삼습니다.

---

## Slide 13: 모드(Modes) — 테마의 핵심
**Visual**: 같은 프레임이 Light/Dark 모드로 전환되는 비교.
**Key Points**:
- 모드로 라이트/다크·브랜드·반응형 컨텍스트 전환
- 프레임을 복제하지 않고 한 곳에서 처리
- 토큰부터 시작, 컴포넌트는 점진적으로
**Speaker Notes**: color/bg 변수가 Light엔 흰색, Dark엔 검정. 프레임 복제 없이 모드만 바꾸면 됩니다. 작은 팀은 100개 컴포넌트가 아니라 토큰(색·간격·타이포)부터 시작하라는 게 정석입니다.

---

## Slide 14: 프로토타이핑
**Visual**: 두 프레임을 잇는 연결선 + 트리거/액션/애니메이션 라벨.
**Key Points**:
- 트리거(On click 등) · 액션(Navigate/Overlay) · 애니메이션
- Smart Animate로 부드러운 전환
- Present(Cmd+Alt+Enter)로 실행
**Speaker Notes**: 실습: 홈→상세 Navigate 연결, 모달 Open overlay, 카드 확장 Smart Animate. 프로토타입은 흐름·인터랙션 검증용이지 최종 스펙이 아니라는 점을 분명히 하세요.

---

## Slide 15: Dev Mode & Code Connect
**Visual**: Inspect 패널(간격·색·CSS) + Code Connect로 실제 코드 표시.
**Key Points**:
- Ready for Dev / Dev complete 워크플로우
- Inspect: 크기·색·타이포·CSS
- Code Connect: 실제 코드베이스 컴포넌트 매핑
**Speaker Notes**: 개발자 대상 클래스라면 반드시 시연하세요. Inspect로 값 읽기, 변수명을 코드 토큰과 맞추기, Ready for Dev 표시. Code Connect는 자동 생성 코드 대신 팀의 실제 컴포넌트 코드를 보여줍니다.

---

## Slide 16: 협업 기능
**Visual**: 멀티커서 + 코멘트 핀 + 버전 히스토리 타임라인.
**Key Points**:
- 실시간 멀티커서, 코멘트(C)
- 버전 히스토리 / 브랜칭
- 라이브러리 발행(Publish)
**Speaker Notes**: 공유(Share) 권한(view/edit) 설정, 코멘트로 피드백, 버전 히스토리로 되돌리기를 실습합니다. 브랜칭은 Git 브랜치와 유사한 조직 기능입니다.

---

## Slide 17: 2024~2025 신기능
**Visual**: UI3 / Figma AI / Slides / Make / Sites 카드 배열 + Config 로고.
**Key Points**:
- Config 2024: UI3, Figma AI, Slides, Dev Mode·Code Connect
- Config 2025: Figma Make, Sites, Check designs 린터, 고급 드로잉, 새 Grid
**Speaker Notes**: "피그마는 이렇게 확장 중"이라는 동기부여용 슬라이드입니다. 단, AI·Make·Sites는 요금제·베타 상태가 자주 바뀌니 조직 플랜 확인을 안내하세요.

---

## Slide 18: 필수 단축키
**Visual**: 키캡 그래픽으로 단축키 치트시트.
**Key Points**:
- V/F/R/O/T/P, Shift+A(Auto Layout)
- Cmd+Alt+K(컴포넌트), Cmd+D(복제)
- C(코멘트), Cmd+Alt+Enter(Present)
**Speaker Notes**: 이 슬라이드는 수강생에게 치트시트로 배포하세요. 단축키가 몸에 붙으면 작업 속도가 극적으로 올라갑니다.

---

## Slide 19: 온보딩 10계명
**Visual**: 번호가 매겨진 체크리스트.
**Key Points**:
- 프레임 기본 / Auto Layout 조기 습득
- 이름 잘 짓기 / 두 번이면 컴포넌트
- 색·간격·타이포는 변수 / 모드로 테마
- 프로토타입=흐름, 스펙=Dev Mode
**Speaker Notes**: 클래스 전체를 관통하는 원칙 요약입니다. 이 10가지만 지켜도 협업·유지보수가 크게 좋아집니다.

---

## Slide 20: 4주 학습 로드맵 & 마무리
**Visual**: 4주 타임라인(주차별 주제 + 결과물) + "Auto Layout이 분수령" 카피.
**Key Points**:
- 1주 인터페이스 / 2주 Auto Layout·컴포넌트
- 3주 변수·모드 / 4주 프로토타입·Dev Mode
- 순서만 지키면 학습 곡선은 완만
**Speaker Notes**: "기본 도구 → Auto Layout → 컴포넌트 → 변수/토큰" 순서를 지키는 게 핵심입니다. 목표는 기능 암기가 아니라 재사용·일관·협업의 사고방식입니다. 이 흐름만 잡으면 신기능은 언제든 얹을 수 있습니다. 질문 받겠습니다 — 참고문헌은 references 파일을 보세요.
