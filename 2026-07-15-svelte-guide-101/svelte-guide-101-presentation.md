# Svelte 가이드 101 — 온보딩 클래스
## PPT 슬라이드 아웃라인 (Svelte 5 Runes 기준, 2025~2026)

---

## Slide 1: 표지 (Cover)
**Visual**: Svelte 시그니처 오렌지(#FF3E00) 그라디언트 배경 + Svelte 로고. "Svelte 101" 크게.
**Key Points**:
- Svelte 가이드 101
- 온보딩 클래스
- Svelte 5 Runes로 시작하기
**Speaker Notes**: 이 클래스는 Svelte 5(Runes)를 기준으로 합니다. Svelte의 핵심 정체성은 "런타임이 아니라 컴파일러"라는 점입니다. 오늘 목표는 문법 암기가 아니라 명시적 반응성으로 생각하는 법을 심는 것입니다. 인터넷의 오래된 자료는 Svelte 4 문법이 많으니 Runes 기반인지 꼭 확인하라고 안내하세요.

---

## Slide 2: 목차 (Agenda)
**Visual**: 5개 블록 그리드.
**Key Points**:
- 컴파일러 정체성 / 컴포넌트 구조
- Runes / Props·통신
- 템플릿 / Snippets / 스타일
- SvelteKit 라우팅·데이터
- 마이그레이션 / 로드맵
**Speaker Notes**: 각 파트는 개념 → 코드 → 자주 하는 실수 순서입니다. 4주면 클릭 가능한 멀티페이지 앱까지 만듭니다.

---

## Slide 3: Svelte란? — "컴파일러"라는 정체성
**Visual**: 좌 React/Vue(런타임+가상DOM) vs 우 Svelte(컴파일→순수 JS) 비교 도식.
**Key Points**:
- 빌드 시점에 순수 JS로 컴파일, 가상 DOM 없음
- 작은 번들 · 빠른 성능 · 적은 보일러플레이트
- Svelte(언어) vs SvelteKit(메타프레임워크)
**Speaker Notes**: React·Vue는 브라우저에서 도는 런타임을 배포하지만, Svelte는 컴파일 시점에 필요한 DOM 갱신 코드를 생성합니다. 그래서 번들이 작고 빠릅니다. 실무는 보통 SvelteKit으로 시작합니다.

---

## Slide 4: 컴포넌트 3영역 (.svelte)
**Visual**: script / markup / style 3분할 코드 카드.
**Key Points**:
- `<script>` 로직 · 마크업 · `<style>`(기본 scoped)
- `{ }`로 JS 표현식 삽입
- 스타일은 컴포넌트에만 적용, 전역은 `:global`
**Speaker Notes**: 세 영역 모두 선택 사항입니다. 가장 자주 하는 실수가 스타일이 전역인 줄 아는 것 — Svelte의 style은 기본 scoped입니다.

---

## Slide 5: 섹션 구분 — Runes (핵심)
**Visual**: "$" 대형 기호 + "명시적 반응성" 카피.
**Key Points**:
- Svelte 5의 가장 큰 변화
- `$`로 시작하는 컴파일러 기호
**Speaker Notes**: 여기가 클래스의 심장입니다. Runes는 반응성을 명시적으로 선언하며, Svelte 4의 암묵적 반응성(let, $:, export let)을 대체합니다.

---

## Slide 6: `$state` & `$derived`
**Visual**: 카운터 코드 + doubled 파생값 흐름 화살표.
**Key Points**:
- `$state(0)`: 반응형 상태(객체·배열 깊은 반응)
- `$derived(count*2)`: 파생값, 의존성 자동추적·메모
- 복잡한 계산은 `$derived.by(() => …)`
**Speaker Notes**: state가 바뀌면 UI가 자동 갱신됩니다. 다른 상태로부터 계산되는 값은 반드시 derived를 쓰세요 — effect로 수동 동기화하지 마세요.

---

## Slide 7: `$effect` — 부수 효과
**Visual**: effect가 외부세계(DOM/로그/서드파티)와 동기화하는 도식.
**Key Points**:
- 마운트/의존성 변경 시 실행
- DOM 조작·로깅·서드파티 연동에만 사용
- 상태 파생에 남용 금지 (루프·버그)
**Speaker Notes**: effect는 외부 세계와의 동기화 전용입니다. "계산은 derived, 동기화만 effect" — 이 한 문장이 버그의 절반을 막습니다.

---

## Slide 8: Runes 요약표 (4→5 대응)
**Visual**: 4열 대응표.
**Key Points**:
- `$state` = let / `$derived` = `$:` / `$effect` = `$: {}`
- `$props` = `export let`
**Speaker Notes**: 이 표를 치트시트로 배포하세요. React/Vue 경험자에게는 각 rune을 익숙한 개념(useState/computed 등)에 대응시켜 설명하면 빠릅니다.

---

## Slide 9: Props & 컴포넌트 통신
**Visual**: 부모→자식(props), 자식→부모(콜백), 양방향($bindable) 3화살표 도식.
**Key Points**:
- 부모→자식: `let { title } = $props()`
- 자식→부모: 콜백 prop (dispatcher 대신)
- 양방향: `$bindable()` + `bind:value`
**Speaker Notes**: Svelte 5는 createEventDispatcher 대신 콜백 prop을 권장합니다. $bindable은 Vue의 v-model처럼 느껴진다고 연결하면 이해가 빠릅니다.

---

## Slide 10: 템플릿 문법
**Visual**: if/each/await 블록 + 이벤트/바인딩 코드.
**Key Points**:
- `{#if}` `{#each ... (key)}` `{#await}`
- 이벤트: `onclick` (Svelte 5) — `on:click` 아님!
- `bind:value`, `bind:checked`
**Speaker Notes**: each에는 반드시 안정적 key를 주세요. 가장 흔한 함정이 오래된 자료의 on:click입니다 — Svelte 5는 표준 속성 onclick을 씁니다.

---

## Slide 11: Snippets (slot 대체)
**Visual**: `{#snippet}` 정의 + `{@render}` 사용 코드.
**Key Points**:
- `{#snippet name(param)}` / `{@render name(x)}`
- 파라미터·props 전달 가능 → slot보다 강력
**Speaker Notes**: Svelte 5는 slot을 Snippets로 대체했습니다. React의 render props/children, Vue의 slot과 같은 개념이라고 대응시키세요.

---

## Slide 12: 스타일 & 트랜지션
**Visual**: transition:fade 코드 + class:/style: 디렉티브.
**Key Points**:
- Scoped CSS, 전역 `:global`
- `class:active={x}`, `style:color={c}`
- `transition:fade` — 내장 애니메이션
**Speaker Notes**: 트랜지션이 프레임워크에 내장되어 별도 라이브러리 없이 매끄러운 UI를 만듭니다. Svelte의 큰 매력 포인트입니다.

---

## Slide 13: 섹션 구분 — SvelteKit
**Visual**: "폴더가 곧 라우터" 카피 + 파일 트리.
**Key Points**:
- 실무는 SvelteKit으로 시작
- 파일 시스템 = 라우터
**Speaker Notes**: 설정 파일 없이 src/routes에 폴더만 만들면 라우트가 생깁니다.

---

## Slide 14: 파일 기반 라우팅 & load
**Visual**: 파일 트리(+page/+layout/[slug]) + load→data 흐름.
**Key Points**:
- `+page.svelte`, `+layout.svelte`, `[slug]` 동적
- `load` 반환값 → `data` prop
- `+page.server.js`는 서버 전용(DB·비밀키)
**Speaker Notes**: +page.js는 서버·클라 모두, +page.server.js는 서버에서만 실행됩니다. DB나 비밀 키가 필요하면 .server를 쓰세요.

---

## Slide 15: Form Actions & 렌더링 모드
**Visual**: form action 코드 + SSR/SSG/CSR/ISR 배지.
**Key Points**:
- `actions`: 표준 `<form>`으로 서버에 쓰기
- 기본 progressive enhancement (JS 없이도 동작)
- SSR(기본)·SSG·CSR·ISR 페이지별 제어
**Speaker Notes**: load가 읽기라면 actions는 쓰기입니다. 웹 표준 form을 그대로 쓰고, JS가 꺼져도 동작하는 점진적 향상이 기본입니다.

---

## Slide 16: Svelte 4 → 5 마이그레이션
**Visual**: 좌 4 / 우 5 대응표(하이라이트).
**Key Points**:
- let→$state, $:→$derived/$effect
- export let→$props, on:click→onclick
- slot→snippet, dispatcher→콜백
**Speaker Notes**: 대부분 하위 호환되고 npx sv migrate로 자동 변환도 됩니다. 하지만 온보딩에서는 처음부터 Runes만 가르쳐 혼란을 줄이세요.

---

## Slide 17: 온보딩 10계명
**Visual**: 번호 체크리스트.
**Key Points**:
- 컴파일러 정체성 이해 / Runes 자료만
- 계산=derived, 동기화=effect
- onclick(5) / scoped style / Snippets
- 실무는 SvelteKit, 폴더가 라우터
**Speaker Notes**: 클래스를 관통하는 원칙 요약입니다. 3번(계산은 derived)만 지켜도 버그가 크게 줄어듭니다.

---

## Slide 18: 4주 로드맵 & 마무리
**Visual**: 4주 타임라인 + "명시적 반응성으로 생각하기" 카피.
**Key Points**:
- 1주 컴파일러·컴포넌트·$state/$derived
- 2주 $effect·$props·통신·블록
- 3주 Snippets·스타일·트랜지션
- 4주 SvelteKit 라우팅·load·actions
**Speaker Notes**: "컴파일러 개념 → Runes → 컴포넌트 통신 → SvelteKit" 순서를 지키면 학습 곡선이 완만합니다. 최고의 시작점은 svelte.dev의 인터랙티브 튜토리얼입니다. 질문 받겠습니다 — 참고문헌은 references 파일을 보세요.
