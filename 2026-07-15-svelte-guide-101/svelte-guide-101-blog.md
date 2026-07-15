---
layout: default
title: "Svelte 101: 온보딩 클래스 (Svelte 5 Runes 기준, 2025~2026)"
---

# Svelte 가이드 101: 온보딩 클래스 — Svelte 5 Runes로 시작하기

> 📊 **발표자료**: [svelte-guide-101-presentation.md](./svelte-guide-101-presentation.md)

> "Svelte 5 introduces the `$derived` and `$effect` runes, which determine the dependencies of their expressions when they are evaluated — a significant shift from Svelte 4's compiler-based reactivity."
> — [Svelte Blog: Introducing runes](https://svelte.dev/blog/runes)

이 문서는 **Svelte 온보딩 클래스**용 강사/수강생 커리큘럼이다. React·Vue 등 다른 프레임워크 경험이 있거나, 프론트엔드가 처음인 개발자를 대상으로 **Svelte 5(Runes)**를 기준으로 작성했다. Svelte는 런타임 프레임워크가 아니라 **컴파일러**라는 점이 핵심 정체성이며, 이 사고방식을 먼저 심는 것이 온보딩의 목표다. 각 장은 **개념 → 코드 → 자주 하는 실수** 순서로 구성해 그대로 수업 흐름으로 쓸 수 있다.

> ⚠️ **버전 주의**: 이 클래스는 **Svelte 5**를 기준으로 한다. 인터넷의 오래된 튜토리얼은 Svelte 4 문법(`export let`, `$:`, 스토어 위주)을 쓰는 경우가 많으니, 수강생에게 "Runes 기반 자료인지" 먼저 확인하라고 안내한다.

---

## 목차

1. [Svelte란 무엇인가 — "컴파일러"라는 정체성](#1-svelte란-무엇인가--컴파일러라는-정체성)
2. [컴포넌트 구조: `.svelte` 파일 3영역](#2-컴포넌트-구조-svelte-파일-3영역)
3. [반응성의 핵심: Runes](#3-반응성의-핵심-runes)
4. [Props와 컴포넌트 통신](#4-props와-컴포넌트-통신)
5. [템플릿 문법: 블록·이벤트·바인딩](#5-템플릿-문법-블록이벤트바인딩)
6. [Snippets — slot을 대체하는 재사용 조각](#6-snippets--slot을-대체하는-재사용-조각)
7. [스타일링과 트랜지션](#7-스타일링과-트랜지션)
8. [SvelteKit — 파일 기반 라우팅과 데이터 로딩](#8-sveltekit--파일-기반-라우팅과-데이터-로딩)
9. [Svelte 4 → 5 마이그레이션 핵심](#9-svelte-4--5-마이그레이션-핵심)
10. [온보딩 팁 & 학습 로드맵](#10-온보딩-팁--학습-로드맵)
11. [참고문헌](#참고문헌)

---

## 1. Svelte란 무엇인가 — "컴파일러"라는 정체성

React·Vue는 브라우저에서 실행되는 **런타임 라이브러리**를 함께 배포한다(가상 DOM diff 등). 반면 **Svelte는 빌드 시점에 컴포넌트를 순수 JavaScript로 컴파일**하고, 가상 DOM 없이 **필요한 DOM 노드만 직접 갱신**하는 코드를 생성한다.

### 그래서 무엇이 좋은가 (온보딩 첫 슬라이드 요점)
- **작은 번들**: 프레임워크 런타임을 거의 배포하지 않음 → 동급 기능에서 React 계열 대비 JS가 크게 적다.
- **빠른 성능**: 가상 DOM diff가 없어 업데이트가 직접적이다.
- **적은 보일러플레이트**: HTML/CSS/JS를 한 파일에 자연스럽게 쓴다. "웹 표준에 가까운" 느낌.
- **Svelte 5 Runes**: 반응성이 명시적 시그널로 바뀌어 컴포넌트 밖(유틸·모듈)에서도 동작.

### 용어 정리
- **Svelte**: UI 컴포넌트를 만드는 언어/컴파일러.
- **SvelteKit**: Svelte 기반 **풀스택 메타프레임워크**(라우팅·SSR·빌드·배포). 실무에서는 보통 SvelteKit으로 프로젝트를 시작한다.

**실습 시작**: [svelte.dev](https://svelte.dev)의 인터랙티브 튜토리얼 또는 `npx sv create my-app`로 프로젝트 생성.

---

## 2. 컴포넌트 구조: `.svelte` 파일 3영역

Svelte 컴포넌트는 하나의 `.svelte` 파일이며 세 영역으로 구성된다. 세 영역 모두 선택 사항이다.

```svelte
<script lang="ts">
  // 1) 로직: 상태, props, 함수
  let name = $state("world");
</script>

<!-- 2) 마크업: HTML + Svelte 템플릿 문법 -->
<h1>Hello {name}!</h1>
<input bind:value={name} />

<style>
  /* 3) 스타일: 기본적으로 이 컴포넌트에만 적용(scoped) */
  h1 { color: #ff3e00; }
</style>
```

- `<script>`: 컴포넌트 로직. `lang="ts"`로 TypeScript 사용.
- 마크업: `{ }`로 JS 표현식을 삽입한다.
- `<style>`: **자동으로 스코프**된다 — 이 컴포넌트에만 적용되어 전역 오염이 없다.

**자주 하는 실수**: 스타일이 전역인 줄 알고 다른 컴포넌트에 영향을 기대함. → Svelte의 `<style>`은 기본 scoped이며, 전역이 필요하면 `:global(...)`을 쓴다.

---

## 3. 반응성의 핵심: Runes

Svelte 5의 가장 큰 변화가 **Runes**다. `$`로 시작하는 컴파일러 기호로, 반응성을 **명시적**으로 선언한다. `let`(Svelte 4의 암묵적 반응성), `$:`, `export let`을 대체한다.

### 3.1 `$state` — 반응형 상태
```svelte
<script>
  let count = $state(0);           // 반응형 변수
  let user = $state({ name: "Ana", age: 30 });  // 객체/배열도 깊게 반응
</script>

<button onclick={() => count++}>클릭 수: {count}</button>
```
`$state`로 선언한 값이 바뀌면 그 값을 사용하는 UI가 자동으로 갱신된다. 객체·배열은 깊은(deep) 반응성을 갖는다.

### 3.2 `$derived` — 파생 값
```svelte
<script>
  let count = $state(0);
  let doubled = $derived(count * 2);            // 의존성 자동 추적, 메모이제이션
  let parity = $derived.by(() => count % 2 ? "홀수" : "짝수");  // 복잡한 계산
</script>

<p>{count} → {doubled} ({parity})</p>
```
`$derived`는 의존하는 상태가 바뀔 때만 재계산되며 **메모이제이션**된다. 복잡한 로직은 `$derived.by(() => {...})`를 쓴다.

> **핵심 규칙**: 다른 상태로부터 "계산되는" 값이면 `$effect`로 수동 동기화하지 말고 **반드시 `$derived`**를 써라. ([DEV: $derived vs $effect](https://dev.to/mikehtmlallthethings/understanding-svelte-5-runes-derived-vs-effect-1hh))

### 3.3 `$effect` — 부수 효과
```svelte
<script>
  let count = $state(0);
  $effect(() => {
    console.log("count가 바뀜:", count);   // 마운트/의존성 변경 시 실행
    document.title = `Count: ${count}`;
  });
</script>
```
`$effect`는 DOM 조작·로깅·서드파티 연동 등 **외부 세계와의 동기화**에만 쓴다. 상태 파생에 남용하면 무한 루프·버그의 원인이 된다.

### 3.4 `$props` — 컴포넌트 입력 (4장에서 상세)
```svelte
<script>
  let { title, count = 0 } = $props();  // 구조 분해 + 기본값
</script>
```

**Runes 요약표**

| Rune | 역할 | Svelte 4 대응 |
|------|------|---------------|
| `$state` | 반응형 상태 | `let x = ...` |
| `$derived` | 파생 값(메모) | `$: y = ...` |
| `$effect` | 부수 효과 | `$: {...}` / `onMount` |
| `$props` | 컴포넌트 props | `export let` |

**자주 하는 실수**: `$derived`로 될 것을 `$effect` 안에서 다른 `$state`에 대입 → 불필요한 리렌더·루프. "계산은 derived, 동기화만 effect" 규칙을 반복 강조한다.

---

## 4. Props와 컴포넌트 통신

### 부모 → 자식: `$props`
```svelte
<!-- Child.svelte -->
<script lang="ts">
  let { label, disabled = false }: { label: string; disabled?: boolean } = $props();
</script>
<button {disabled}>{label}</button>
```
```svelte
<!-- Parent.svelte -->
<script>import Child from "./Child.svelte";</script>
<Child label="저장" />
```

### 자식 → 부모: 콜백 props (Svelte 5 권장)
Svelte 5는 `createEventDispatcher` 대신 **콜백 함수를 prop으로 넘기는** 방식을 권장한다.
```svelte
<!-- Child.svelte -->
<script>let { onsave } = $props();</script>
<button onclick={() => onsave("데이터")}>저장</button>
```
```svelte
<!-- Parent.svelte -->
<Child onsave={(data) => console.log("받음:", data)} />
```

### 양방향 바인딩: `$bindable`
```svelte
<!-- Child.svelte -->
<script>let { value = $bindable() } = $props();</script>
<input bind:value />
```
```svelte
<!-- Parent.svelte -->
<Child bind:value={text} />
```

**온보딩 포인트**: React 경험자에겐 "props로 콜백 내리기"가 익숙하고, Vue 경험자에겐 `$bindable`이 `v-model`처럼 느껴진다고 연결해주면 이해가 빠르다.

---

## 5. 템플릿 문법: 블록·이벤트·바인딩

### 조건/반복/비동기 블록
```svelte
{#if loggedIn}
  <p>환영합니다</p>
{:else}
  <button onclick={login}>로그인</button>
{/if}

{#each items as item, i (item.id)}   <!-- (item.id): 안정적 key -->
  <li>{i}: {item.name}</li>
{/each}

{#await promise}
  <p>로딩 중…</p>
{:then data}
  <p>{data.title}</p>
{:catch error}
  <p>에러: {error.message}</p>
{/await}
```

### 이벤트 (Svelte 5는 표준 속성 문법)
```svelte
<button onclick={handleClick}>클릭</button>   <!-- Svelte 5: on:click 아님! -->
<input oninput={(e) => (text = e.currentTarget.value)} />
```
> Svelte 5부터 이벤트는 `on:click`이 아니라 **`onclick`** 처럼 일반 속성으로 쓴다(Svelte 4는 `on:click`).

### 바인딩
```svelte
<input bind:value={name} />
<input type="checkbox" bind:checked={agree} />
<select bind:value={selected}>…</select>
```

**자주 하는 실수**: 오래된 자료를 보고 `on:click`을 씀 → Svelte 5에서 경고/미동작. 이벤트 문법 변경을 반드시 짚어준다.

---

## 6. Snippets — slot을 대체하는 재사용 조각

Svelte 5는 `<slot>`을 **Snippets**로 대체한다. `{#snippet}`으로 정의하고 `{@render}`로 렌더링하며, **파라미터를 받고 props로 전달**할 수 있어 slot보다 강력하다.

```svelte
<!-- 정의 & 사용 -->
{#snippet row(item)}
  <tr><td>{item.name}</td><td>{item.price}원</td></tr>
{/snippet}

<table>
  {#each products as p}
    {@render row(p)}
  {/each}
</table>
```

자식 컴포넌트에 조각을 넘기는 것도 가능하다(기존 named slot 대체).
```svelte
<Card>
  {#snippet header()}<h2>제목</h2>{/snippet}
  {#snippet children()}<p>본문</p>{/snippet}
</Card>
```

**온보딩 포인트**: "React의 render props / children, Vue의 slot과 같은 개념"이라고 대응시키면 빠르게 이해한다.

---

## 7. 스타일링과 트랜지션

- **Scoped CSS**: `<style>`은 기본 컴포넌트 스코프. 전역은 `:global(...)`.
- **동적 클래스/스타일**: `class:active={isActive}`, `style:color={c}`.
- **트랜지션**: `svelte/transition`의 `fade`, `fly`, `slide` 등을 `transition:fade`로 선언적으로 적용.

```svelte
<script>import { fade } from "svelte/transition";</script>
{#if visible}
  <div transition:fade={{ duration: 200 }}>부드럽게 등장</div>
{/if}

<button class:active={isActive} style:opacity={isActive ? 1 : 0.5}>토글</button>
```

트랜지션·애니메이션이 프레임워크에 내장되어 별도 라이브러리 없이 매끄러운 UI를 만들 수 있는 점이 Svelte의 매력이다.

---

## 8. SvelteKit — 파일 기반 라우팅과 데이터 로딩

실무 Svelte 프로젝트는 대부분 **SvelteKit**으로 만든다. 핵심은 **파일 시스템이 곧 라우터**라는 점이다.

### 8.1 파일 기반 라우팅
`src/routes` 아래 폴더 구조가 URL이 되고, `+` 접두 파일이 특수 역할을 한다.
```
src/routes/
├── +page.svelte          →  /            (페이지)
├── +layout.svelte        →  모든 하위 라우트를 감싸는 레이아웃
├── about/+page.svelte    →  /about
└── blog/[slug]/+page.svelte  →  /blog/:slug (동적 파라미터)
```

### 8.2 데이터 로딩: `load` 함수
`+page.svelte` 옆에 `+page.js`(또는 서버 전용 `+page.server.js`)를 두고 `load`를 export한다. 반환값이 페이지의 `data` prop이 된다.
```javascript
// src/routes/blog/[slug]/+page.server.js
export async function load({ params }) {
  const post = await db.getPost(params.slug);   // DB·비밀키는 .server 파일에서만
  return { post };
}
```
```svelte
<!-- +page.svelte -->
<script>let { data } = $props();</script>
<h1>{data.post.title}</h1>
```
> `+page.js`는 서버·클라이언트 모두에서, `+page.server.js`는 **서버에서만** 실행된다. DB 접근이나 비밀 API 키가 필요하면 `.server`를 쓴다. ([SvelteKit Routing Docs](https://svelte.dev/docs/kit/routing))

### 8.3 폼 액션(Form Actions)
`load`가 읽기라면, **actions**는 표준 `<form>`으로 서버에 쓰기(mutation)를 한다. 기본적으로 **점진적 향상(progressive enhancement)**이 적용되어 JS 없이도 동작한다.
```javascript
// +page.server.js
export const actions = {
  create: async ({ request }) => {
    const data = await request.formData();
    await db.create({ title: data.get("title") });
    return { success: true };
  },
};
```
```svelte
<form method="POST" action="?/create">
  <input name="title" />
  <button>생성</button>
</form>
```

### 8.4 렌더링 모드
SvelteKit은 SSR(기본)·SSG(prerender)·CSR·ISR을 지원한다. 페이지별로 `export const prerender = true` 등으로 제어한다.

**온보딩 포인트**: "설정 파일 없이 폴더만 만들면 라우트가 생긴다"는 점, 그리고 `load`/`actions`가 "웹 표준(fetch/form)에 가깝다"는 점이 SvelteKit의 매력임을 강조한다.

---

## 9. Svelte 4 → 5 마이그레이션 핵심

수강생이 오래된 자료와 섞여 혼란스럽지 않도록, 4→5 변경점을 명확히 정리한다.

| 항목 | Svelte 4 | Svelte 5 |
|------|----------|----------|
| 반응형 상태 | `let count = 0` | `let count = $state(0)` |
| 파생 값 | `$: doubled = count * 2` | `let doubled = $derived(count * 2)` |
| 부수 효과 | `$: { ... }` | `$effect(() => { ... })` |
| props | `export let title` | `let { title } = $props()` |
| 이벤트 | `on:click` | `onclick` |
| 컨텐츠 삽입 | `<slot>` | `{#snippet}` + `{@render}` |
| 자식→부모 | `createEventDispatcher` | 콜백 prop |

> Svelte 5는 대부분 하위 호환되며 `npx sv migrate svelte-5`로 자동 마이그레이션을 지원하지만, 온보딩 클래스에서는 **처음부터 Runes 문법만** 가르쳐 혼란을 줄이는 것을 권장한다.

---

## 10. 온보딩 팁 & 학습 로드맵

### 온보딩 10계명
1. **"Svelte는 컴파일러"** 라는 정체성을 먼저 이해한다.
2. **Svelte 5 Runes 기준 자료**만 본다(오래된 `export let` 자료 주의).
3. **계산은 `$derived`, 동기화만 `$effect`** — 이 규칙만 지켜도 버그 절반이 사라진다.
4. `$effect` 남용 금지.
5. 이벤트는 `onclick`(5) — `on:click`(4) 아님.
6. `<style>`은 **기본 scoped**, 전역은 `:global`.
7. `<slot>` 대신 **Snippets**.
8. 자식→부모는 **콜백 prop**, 양방향은 `$bindable`.
9. 실무는 **SvelteKit**으로 시작 — 폴더가 라우터.
10. `load`(읽기)/`actions`(쓰기)는 **웹 표준**에 가깝게 생각한다.

### 4주 학습 로드맵 (클래스 커리큘럼 예시)

| 주차 | 주제 | 실습 결과물 |
|------|------|-------------|
| 1주 | 컴파일러 개념 · 컴포넌트 3영역 · `$state`/`$derived` | 카운터·투두 입력 |
| 2주 | `$effect` · `$props` · 컴포넌트 통신 · 템플릿 블록 | 재사용 컴포넌트 세트 |
| 3주 | Snippets · 스타일 · 트랜지션 | 리스트·모달 UI |
| 4주 | SvelteKit 라우팅 · `load` · form actions | 클릭 가능한 멀티페이지 앱 |

### 필수 학습 리소스
- [Svelte 공식 인터랙티브 튜토리얼](https://svelte.dev/tutorial) — 브라우저에서 바로 실습 (**최고의 시작점**)
- [Svelte 5 Docs](https://svelte.dev/docs/svelte/overview) · [SvelteKit Docs](https://svelte.dev/docs/kit/introduction)
- [Introducing runes (Svelte Blog)](https://svelte.dev/blog/runes) — Runes 설계 철학

### 마무리 메시지
Svelte의 학습 곡선은 "컴파일러 개념 → Runes(`$state`/`$derived`) → 컴포넌트 통신 → SvelteKit" 순서를 지키면 매우 완만하다. 문법이 웹 표준에 가깝고 보일러플레이트가 적어, 다른 프레임워크 경험자는 하루 만에, 프론트엔드 입문자도 몇 주면 실전 앱을 만든다. 온보딩의 목표는 문법 암기가 아니라 **"명시적 반응성으로 생각하는 법"**을 심는 것이다.

---

## 참고문헌

참고문헌 전체 목록은 [create_references.py](./create_references.py)로 생성되는 `svelte-guide-101-references.xlsx`를 참고하세요. 주요 출처:

1. [Introducing runes — Svelte Blog](https://svelte.dev/blog/runes)
2. [$state / $derived / $effect — Svelte Docs](https://svelte.dev/docs/svelte/$state)
3. [Svelte 5 runes: the complete guide — Full Stack SvelteKit](https://fullstacksveltekit.com/blog/svelte-5-runes)
4. [Understanding Svelte 5 Runes: $derived vs $effect — DEV](https://dev.to/mikehtmlallthethings/understanding-svelte-5-runes-derived-vs-effect-1hh)
5. [Routing — SvelteKit Docs](https://svelte.dev/docs/kit/routing)
6. [Svelte Tutorial (공식)](https://svelte.dev/tutorial)
7. [Svelte 5 Cheat Sheet — devtooleasy](https://devtooleasy.com/cheat-sheet/svelte)

> Powered by Claude Code & Auto Research Pipeline · 2026-07-15
