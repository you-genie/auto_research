---
layout: default
title: "피그마 가이드 101: 온보딩 클래스 (2025~2026)"
---

# 피그마(Figma) 가이드 101: 온보딩 클래스를 위한 완전 입문

> 📊 **발표자료**: [figma-guide-101-presentation.md](./figma-guide-101-presentation.md)

> "Move into components and auto layout after basics — these features help beginners jump from 'I can draw screens' to 'I can build reusable UI'."
> — [Figma Learn: Figma Design for beginners (2025)](https://help.figma.com/hc/en-us/articles/30848209492887-Course-overview-Figma-Design-for-beginners-2025)

이 문서는 **피그마 온보딩 클래스**를 진행하기 위한 강사용/수강생용 커리큘럼이다. 디자인 툴을 처음 접하는 개발자·기획자·신입 디자이너를 대상으로, "화면을 그릴 수 있다"에서 "재사용 가능한 UI를 만든다"까지 한 번에 도달하는 것을 목표로 한다. 각 장은 **개념 → 실습 포인트 → 자주 하는 실수** 순서로 구성되어, 그대로 수업 흐름으로 사용할 수 있다.

---

## 목차

1. [피그마란 무엇인가](#1-피그마란-무엇인가)
2. [인터페이스 기초: 5개 영역](#2-인터페이스-기초-5개-영역)
3. [기본 도구: 프레임 · 도형 · 텍스트 · 제약(Constraints)](#3-기본-도구-프레임--도형--텍스트--제약)
4. [Auto Layout — 반응형의 핵심](#4-auto-layout--반응형의-핵심)
5. [컴포넌트 & 배리언트 — 재사용의 시작](#5-컴포넌트--배리언트--재사용의-시작)
6. [스타일 · 변수(Variables) · 디자인 토큰](#6-스타일--변수variables--디자인-토큰)
7. [프로토타이핑 — 화면을 살아 움직이게](#7-프로토타이핑--화면을-살아-움직이게)
8. [Dev Mode & Code Connect — 개발자 협업](#8-dev-mode--code-connect--개발자-협업)
9. [협업 기능: 실시간 · 코멘트 · 버전 · 브랜치](#9-협업-기능-실시간--코멘트--버전--브랜치)
10. [2024~2025 신기능: UI3 · AI · Slides · Make · Sites](#10-20242025-신기능-ui3--ai--slides--make--sites)
11. [단축키 & 온보딩 팁 & 학습 로드맵](#11-단축키--온보딩-팁--학습-로드맵)
12. [참고문헌](#참고문헌)

---

## 1. 피그마란 무엇인가

피그마는 **브라우저에서 실행되는 협업형 UI/UX 디자인 툴**이다. 설치 없이 링크만으로 접근하고, 구글 문서처럼 여러 사람이 **동시에 같은 파일을 편집**한다. 이 "실시간 협업 + 클라우드 저장"이 Sketch·Adobe XD 같은 데스크톱 툴과의 근본적 차이다.

### 왜 피그마인가 (온보딩 첫 슬라이드용 요점)
- **설치 불필요 · OS 무관**: 브라우저(또는 데스크톱 앱)만 있으면 된다.
- **실시간 협업**: 디자이너·기획자·개발자가 한 파일에서 동시에 작업하고 코멘트를 남긴다.
- **하나의 파일에서 디자인 → 프로토타입 → 개발 핸드오프**까지 이어진다.
- **UI3**: 2024년 Config에서 공개된 세 번째 인터페이스 개편으로, 더 몰입감 있는 캔버스와 컴포넌트 중심 UI, 새 아이콘셋을 갖췄다.

### 피그마 제품군 (2025 기준)

| 제품 | 용도 |
|------|------|
| **Figma Design** | UI/UX 화면 디자인 (본 클래스의 중심) |
| **FigJam** | 온라인 화이트보드 (브레인스토밍, 다이어그램) |
| **Figma Slides** | 프레젠테이션 제작 (2024 발표, 2025 정식) |
| **Dev Mode** | 개발자용 스펙·코드 뷰 |
| **Figma Make** | 프롬프트→앱, 고충실도 프로토타입 생성 (2025) |
| **Figma Sites** | 디자인을 반응형 웹사이트로 발행 (2025) |

> **강사 팁**: 첫 시간에는 "Figma Design"만 다룬다. 나머지 제품군은 "이런 것도 있다" 수준으로 소개하고 마지막 장에서 다시 언급하는 것이 학습 부하를 줄인다.

---

## 2. 인터페이스 기초: 5개 영역

UI3 화면은 크게 **5개 영역**으로 나뉜다. 온보딩에서 이 지도를 먼저 각인시키면 이후 모든 실습이 수월하다.

1. **캔버스(Canvas)**: 무한 작업 공간. 스페이스바 드래그로 이동, `Ctrl/Cmd + 스크롤`(또는 핀치)로 확대/축소.
2. **툴바(Toolbar)**: 하단(UI3) 또는 상단의 도구 모음 — 이동(V), 프레임(F), 도형(R/O), 텍스트(T), 펜(P) 등.
3. **레이어 패널(Layers, 왼쪽)**: 페이지·프레임·레이어의 계층 구조. 이름을 잘 짓는 습관이 협업의 기본.
4. **속성 패널(Design/Properties, 오른쪽)**: 선택한 요소의 크기·색·타이포·효과·Auto Layout 설정.
5. **페이지(Pages)**: 한 파일 안의 여러 페이지(예: Cover, Wireframe, UI, Prototype).

**실습 포인트**
- 새 파일 만들기 → 프레임(F)으로 아이폰 화면 크기 선택 → 사각형(R)·텍스트(T) 배치 → 확대/이동 익히기.
- 레이어 이름을 `Header`, `Card/Title` 처럼 의미 있게 바꾸기.

**자주 하는 실수**: 레이어 이름을 방치(`Rectangle 47`)해 나중에 협업·개발 핸드오프에서 혼란을 초래. → 처음부터 이름 짓는 습관을 들인다.

---

## 3. 기본 도구: 프레임 · 도형 · 텍스트 · 제약

### 프레임(Frame) vs 그룹(Group)
- **프레임**은 화면·컨테이너의 기본 단위다. 자체 크기·배경·제약·Auto Layout을 가질 수 있어 "미니 화면"처럼 동작한다.
- **그룹**은 단순히 여러 요소를 묶는 것. 되도록 **프레임을 기본으로** 쓰도록 가르친다. (Auto Layout·제약이 프레임에만 붙기 때문)

### 도형·텍스트·펜
- 사각형(R), 원(O), 선(L), 텍스트(T), 펜(P/벡터). 텍스트는 폰트·크기·자간·행간·정렬을 속성 패널에서 조정.

### 제약(Constraints) — 반응형 기초
프레임 크기가 바뀔 때 자식 요소가 어떻게 따라갈지 정하는 규칙이다. Left/Right/Center/Scale, Top/Bottom 등을 조합한다. 예: 버튼을 "Right + Top"에 고정하면 프레임이 넓어져도 오른쪽 위에 붙어 있다.

**실습 포인트**: 카드 프레임을 만들고, 제목은 Left&Top, 닫기(X) 버튼은 Right&Top 제약을 걸어 프레임 리사이즈 시 동작을 관찰.

---

## 4. Auto Layout — 반응형의 핵심

> "Auto Layout is Figma's flexible layout system that lets you build components that adapt to their content, much like CSS Flexbox." — [Figma Learn: Guide to auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout)

**Auto Layout**은 피그마 학습의 분수령이다. CSS의 Flexbox와 거의 동일한 개념으로, 내용이 늘거나 줄면 요소가 **자동으로 재배치**된다. 개발자에게 특히 직관적이다.

### 핵심 개념 (Flexbox 대응)

| Auto Layout | CSS Flexbox |
|-------------|-------------|
| 방향(가로/세로) | `flex-direction` |
| 간격(Gap between items) | `gap` |
| 패딩(Padding) | `padding` |
| 정렬(Alignment) | `justify-content` / `align-items` |
| Hug / Fill / Fixed | `fit-content` / `flex: 1` / 고정 크기 |

- **Hug contents**: 내용 크기에 맞게 컨테이너가 줄어듦.
- **Fill container**: 부모의 남은 공간을 채움.
- **Fixed**: 고정 크기.

### 왜 중요한가
버튼에 텍스트가 길어져도 패딩이 유지되고, 리스트에 항목을 추가해도 간격이 자동 정렬된다. **재사용 가능한 컴포넌트의 전제 조건**이다.

**실습 포인트**: 텍스트 + 사각형 → 선택 후 `Shift + A`로 Auto Layout 적용 → 패딩 16, gap 8 설정 → 텍스트를 길게 바꿔도 버튼이 자연스럽게 늘어나는지 확인. 이후 세로 Auto Layout으로 카드 리스트 구성.

**자주 하는 실수**: 모든 것을 절대 좌표로 배치 → 화면이 바뀌면 다 깨진다. Auto Layout을 먼저 가르쳐 이 습관을 원천 차단한다.

---

## 5. 컴포넌트 & 배리언트 — 재사용의 시작

### 컴포넌트(Component)
반복 사용하는 UI 요소(버튼, 인풋, 카드)를 **하나의 원본(Main/Master component)**으로 만들고, 복제본인 **인스턴스(Instance)**를 여러 곳에 배치한다. 원본을 수정하면 모든 인스턴스가 자동 업데이트된다.

- 만들기: 요소 선택 → `Ctrl/Cmd + Alt + K` (또는 우클릭 → Create component).
- 인스턴스는 원본의 속성을 상속하되, 텍스트·색 등은 개별 오버라이드 가능.

### 배리언트(Variants)
하나의 버튼도 상태가 여럿이다(Default / Hover / Disabled, Primary / Secondary, Small / Large). 이런 **여러 상태를 하나의 컴포넌트 세트로 묶은 것**이 배리언트다. 속성(Property)으로 상태를 전환한다.

> "Figma's component system lets you create reusable elements with multiple variants — allowing you to define every state of a button, form field, or card within a single component." — [ALM Corp: Complete Guide to Figma](https://almcorp.com/blog/what-is-figma-complete-guide/)

### 컴포넌트 속성(Properties)
- **Boolean**: 아이콘 표시/숨김.
- **Text**: 라벨 텍스트 교체.
- **Instance swap**: 내부 아이콘 인스턴스 교체.
- **Variant**: 상태(크기/종류/상태) 전환.

**실습 포인트**: 버튼을 컴포넌트로 만들고 Primary/Secondary + Default/Disabled 배리언트 구성 → 인스턴스를 배치해 속성 패널에서 상태를 바꿔본다.

**자주 하는 실수**: 컴포넌트 없이 복붙으로 화면을 채운 뒤 색상 하나 바꾸려고 20개를 일일이 수정. → "두 번 이상 쓸 것 같으면 컴포넌트로" 규칙을 강조.

---

## 6. 스타일 · 변수(Variables) · 디자인 토큰

### 스타일(Styles)
색상·텍스트·이펙트·그리드를 **이름 붙은 재사용 값**으로 저장한다. 예: `Color/Primary`, `Text/Heading-1`. 스타일을 바꾸면 적용된 모든 곳이 갱신된다.

### 변수(Variables)와 디자인 토큰
[변수](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)는 색·간격·크기·문자열·불리언 등 **재사용 값**을 저장하는 상위 개념으로, **디자인 토큰**을 피그마에서 구현하는 방식이다.

- 지원 타입: **Color, Number, String, Boolean** + **Alias(참조/별칭)**.
- **컬렉션(Collection)**으로 묶고, **모드(Modes)**로 컨텍스트를 전환한다.

### 모드(Modes) — 테마의 핵심
> "Variable modes allow us to represent different contexts of our designs without needing to create multiple frames for every context." — [Figma Learn: Modes for variables](https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables)

라이트/다크 테마, 브랜드별, 반응형 크기 등을 **모드**로 정의하면 프레임 하나에서 컨텍스트를 전환할 수 있다. 예: `color/bg` 변수가 Light 모드에선 흰색, Dark 모드에선 검정.

### 스타일 vs 변수 (온보딩에서 헷갈리는 지점)
- **스타일**: 복합적 값(그라디언트, 타이포 세트)에 적합, 모드 없음.
- **변수**: 단일 원자값 + 모드/별칭 지원 → 테마·토큰 시스템에 적합.
- 현대 워크플로우는 **변수를 토큰의 근간**으로 삼고, 코드로 내보내 디자인–개발을 동기화한다.

> **온보딩 조언**: "작은 팀은 100개 컴포넌트를 만들려 하지 말고, **토큰(색·간격·타이포)부터** 시작하라. 컴포넌트는 실제 필요에 따라 점진적으로 추가한다." ([Design Systems Collective](https://www.designsystemscollective.com/design-system-mastery-with-figma-variables-the-2025-2026-best-practice-playbook-da0500ca0e66))

---

## 7. 프로토타이핑 — 화면을 살아 움직이게

프로토타입 모드에서 프레임들을 연결해 **클릭 가능한 시제품**을 만든다. 각 연결은 **트리거(Trigger) · 액션(Action) · 애니메이션(Animation)**으로 구성된다.

- **트리거**: On click, While hovering, Drag, After delay, Key/Gamepad, Mouse enter/leave 등.
- **액션**: Navigate to(화면 이동), Open overlay(모달), Scroll to, Back, Swap 등.
- **애니메이션**: Instant, Dissolve, Move in/out, Push, **Smart Animate**(요소 간 자동 보간).

### Smart Animate
같은 이름의 레이어를 두 프레임에서 자동으로 부드럽게 전환한다. 토글 스위치, 확장 카드, 탭 전환 등에 강력하다.

**실습 포인트**: 홈 → 상세 두 화면을 만들고 버튼에 On click → Navigate 연결 → Present(▶)로 실행. 이어서 모달을 Open overlay로, 카드 확장을 Smart Animate로 구현.

**자주 하는 실수**: 프로토타입을 실제 개발 스펙으로 착각. → 프로토타입은 "흐름·인터랙션 검증"이 목적이며, 최종 수치는 Dev Mode에서 확인한다고 명확히 구분.

---

## 8. Dev Mode & Code Connect — 개발자 협업

**Dev Mode**는 개발자가 디자인에서 **정확한 스펙·간격·색상 값·CSS/코드**를 추출하는 전용 뷰다.

- **Ready for Dev / Dev complete**: 디자이너가 "개발 준비됨"으로 표시하면 개발자는 무엇을 볼지 명확해진다. Focus View로 노이즈를 줄인다.
- **Inspect**: 요소 선택 시 크기·색·타이포·간격과 CSS(iOS/Android 코드도) 확인.
- **변수/토큰 연동**: raw 값이 아니라 변수명(토큰)으로 표시되어 코드와의 간극을 줄인다.
- **Code Connect**: 디자인 시스템 컴포넌트를 **실제 코드베이스의 컴포넌트에 매핑**하면, 개발자는 자동 생성 코드 대신 **자기 팀의 실제 컴포넌트 코드**를 Dev Mode에서 본다.

> "Code Connect brings component code into Dev Mode, where developers see design system code from their libraries instead of auto-generated code." — [Figma Config 2024 Recap](https://www.figma.com/blog/config-2024-recap/)

**온보딩 포인트(개발자 대상 클래스라면)**: Inspect로 간격·색을 읽는 법, 변수명을 코드 토큰과 맞추는 법, "Ready for Dev" 워크플로우를 반드시 시연한다.

---

## 9. 협업 기능: 실시간 · 코멘트 · 버전 · 브랜치

- **실시간 멀티커서**: 여러 명이 동시에 편집하고 상대 커서가 보인다.
- **코멘트(C)**: 특정 위치에 핀을 꽂아 피드백. 스레드로 논의하고 해결 처리.
- **버전 히스토리**: 자동 저장 + 특정 시점으로 되돌리기, 이름 있는 버전 저장.
- **브랜칭(Branching)**: 메인 파일에서 분기해 실험 후 병합(엔터프라이즈/조직 기능). Git 브랜치 개념과 유사.
- **라이브러리 발행(Publish)**: 컴포넌트·스타일·변수를 팀 라이브러리로 발행해 여러 파일에서 공유.

**실습 포인트**: 파일을 동료와 공유(Share)하고 권한(Can view/edit) 설정 → 코멘트 남기기 → 버전 히스토리 확인.

---

## 10. 2024~2025 신기능: UI3 · AI · Slides · Make · Sites

온보딩 마지막에 "피그마는 이렇게 확장되고 있다"를 보여주면 동기부여가 된다. ([Config 2024](https://www.figma.com/blog/config-2024-recap/), [Config 2025](https://www.figma.com/blog/config-2025-recap/))

**Config 2024**
- **UI3**: 세 번째 인터페이스 개편 — 몰입형 캔버스, 컴포넌트 중심 UI, 새 아이콘셋.
- **Figma AI**: 이미지 생성/편집, 레이어 자동 이름, 콘텐츠 채우기 등 AI 보조.
- **Figma Slides**: 디자인 정밀도 + 발표 도구.
- **Dev Mode 강화 & Code Connect**.

**Config 2025**
- **Figma Make**: 프롬프트→앱. 고충실도 프로토타입·코드를 빠르게 생성.
- **Figma Sites**: 디자인을 반응형 웹사이트로 원클릭 발행.
- **Check designs 린터**: raw 값을 알맞은 변수로 자동 제안(토큰 준수 검사).
- **고급 드로잉**: Dynamic strokes, Variable stroke width, Text on a path, Noise/Texture, Progressive blur, Pattern fills.
- **새 Grid 시스템**: 유연한 반응형 레이아웃, Dev Mode에서 CSS로 직접 변환.

> **주의**: AI·Make·Sites 등은 요금제·베타 상태가 자주 바뀐다. 클래스에서는 "존재와 개념"만 소개하고, 실제 사용 가능 여부는 조직 플랜을 확인하도록 안내한다.

---

## 11. 단축키 & 온보딩 팁 & 학습 로드맵

### 필수 단축키 (수강생 배포용)

| 동작 | 단축키(Mac / Win) |
|------|-------------------|
| 이동 도구 | `V` |
| 프레임 | `F` |
| 사각형 / 원 / 텍스트 | `R` / `O` / `T` |
| 펜(벡터) | `P` |
| Auto Layout 적용 | `Shift + A` |
| 컴포넌트 만들기 | `⌘⌥K` / `Ctrl+Alt+K` |
| 복제(제자리) | `⌘D` / `Ctrl+D` |
| 그룹 / 프레임 씌우기 | `⌘G` / `⌘⌥G` |
| 코멘트 | `C` |
| 프로토타입 실행(Present) | `⌘⌥Enter` |
| 확대/축소 맞춤 | `Shift+1`(전체), `Shift+2`(선택) |

### 온보딩 10계명 (초보자 팁)
1. **프레임을 기본 단위로** 쓴다(그룹 남용 금지).
2. **Auto Layout을 조기에** 익힌다 — 나머지가 다 쉬워진다.
3. **레이어·컴포넌트 이름**을 처음부터 잘 짓는다.
4. **두 번 이상 쓸 것은 컴포넌트**로.
5. **색·간격·타이포는 변수(토큰)**로 관리한다.
6. **모드**로 테마(라이트/다크)를 처리한다(프레임 복제 금지).
7. 절대 좌표 대신 **제약 + Auto Layout**으로 반응형을.
8. 프로토타입은 **흐름 검증**용, 스펙은 **Dev Mode**에서.
9. **코멘트로 소통**하고 버전 히스토리를 믿는다.
10. 단축키를 몸에 익혀 **속도**를 올린다.

### 4주 학습 로드맵 (클래스 커리큘럼 예시)

| 주차 | 주제 | 실습 결과물 |
|------|------|-------------|
| 1주 | 인터페이스 · 기본 도구 · 제약 | 정적 카드/화면 1개 |
| 2주 | Auto Layout · 컴포넌트 · 배리언트 | 버튼·인풋·카드 컴포넌트 |
| 3주 | 스타일 · 변수 · 모드(테마) | 라이트/다크 토큰 시스템 |
| 4주 | 프로토타이핑 · Dev Mode · 협업 | 클릭 가능한 프로토타입 + 핸드오프 |

### 공식 학습 리소스
- [Figma Learn — Figma Design for beginners (2025)](https://help.figma.com/hc/en-us/sections/30880632542743-Figma-Design-for-beginners)
- [Figma 릴리스 노트](https://www.figma.com/release-notes/)
- [Figma Community](https://www.figma.com/community) — 무료 템플릿·UI 키트로 실습

### 마무리 메시지
피그마의 학습 곡선은 "기본 도구 → **Auto Layout** → 컴포넌트 → 변수/토큰"의 순서를 지키면 완만하다. 온보딩의 목표는 도구의 모든 기능을 외우는 것이 아니라, **재사용 가능하고 일관된 UI를 협업으로 만드는 사고방식**을 심는 것이다. 이 흐름만 잡으면 신기능(AI, Make, Sites)은 언제든 얹을 수 있다.

---

## 참고문헌

참고문헌 전체 목록은 [create_references.py](./create_references.py)로 생성되는 `figma-guide-101-references.xlsx`를 참고하세요. 주요 출처:

1. [Figma Learn — Figma Design for beginners (2025)](https://help.figma.com/hc/en-us/articles/30848209492887-Course-overview-Figma-Design-for-beginners-2025)
2. [Figma Learn — Guide to auto layout](https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout)
3. [Figma Learn — Guide to variables in Figma](https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma)
4. [Figma Learn — Modes for variables](https://help.figma.com/hc/en-us/articles/15343816063383-Modes-for-variables)
5. [Figma Blog — Config 2024 Recap](https://www.figma.com/blog/config-2024-recap/)
6. [Figma Blog — Config 2025 Recap](https://www.figma.com/blog/config-2025-recap/)
7. [ALM Corp — Complete Guide to Figma](https://almcorp.com/blog/what-is-figma-complete-guide/)
8. [Design Systems Collective — Figma Variables Best-Practice Playbook 2025/2026](https://www.designsystemscollective.com/design-system-mastery-with-figma-variables-the-2025-2026-best-practice-playbook-da0500ca0e66)

> Powered by Claude Code & Auto Research Pipeline · 2026-07-15
