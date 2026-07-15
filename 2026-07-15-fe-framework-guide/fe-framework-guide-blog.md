---
layout: default
title: "프론트엔드 프레임워크 비교 & 개발 가이드 (2025~2026)"
---

# 프론트엔드 프레임워크 완전 정복 (2025~2026): 프레임워크 비교 · 개발 시 주의점 · 코드 스타일 가이드

> 📊 **발표자료**: [fe-framework-guide-presentation.md](./fe-framework-guide-presentation.md)

> "The era of relentless framework creation has quietly wound down. For all the talk of the front-end ecosystem being in constant turmoil, things have been remarkably stable over the past year."
> — [State of JavaScript 2025](https://2025.stateofjs.com/en-US/libraries/front-end-frameworks/)

2020년대 초반의 "프레임워크 전쟁"은 끝났다. 2025~2026년의 프론트엔드 생태계는 **수렴(convergence)**의 시대다. React 19, Vue 3.5, Angular 20, Svelte 5는 서로 다른 문법을 유지하면서도 **fine-grained reactivity(세밀한 반응성), 컴파일러 기반 최적화, 서버 우선 렌더링(server-first)**이라는 동일한 기술적 해법으로 모여들고 있다. 이제 "무엇이 가장 빠른가"보다 "우리 팀·제품에 무엇이 맞는가"가 훨씬 중요한 질문이 되었다.

이 글은 세 부분으로 구성된다.

1. **FE 프레임워크별 비교** — React / Vue / Angular / Svelte / Solid / Qwik + 메타프레임워크(Next.js / Nuxt / SvelteKit / Astro / Remix)
2. **FE 개발자가 개발 시 주의해야 할 점** — 성능(Core Web Vitals) · 접근성(WCAG 2.2) · 보안(XSS/CSP/OWASP) · 상태 관리 · 렌더링 전략 · 하이드레이션
3. **코드 가이드** — ESLint 9 Flat Config · Prettier · TypeScript · 네이밍 · 컴포넌트/폴더 구조 · Git 컨벤션

---

## 목차

1. [프레임워크 지형도: 2025~2026 한눈에 보기](#1-프레임워크-지형도-20252026-한눈에-보기)
2. [프레임워크별 상세 비교](#2-프레임워크별-상세-비교)
3. [메타프레임워크와 렌더링 전략](#3-메타프레임워크와-렌더링-전략)
4. [FE 개발자가 개발 시 주의해야 할 점](#4-fe-개발자가-개발-시-주의해야-할-점)
5. [코드 가이드 (스타일 · 구조 · 도구)](#5-코드-가이드-스타일--구조--도구)
6. [선택 가이드: 상황별 추천](#6-선택-가이드-상황별-추천)
7. [참고문헌](#참고문헌)

---

## 1. 프레임워크 지형도: 2025~2026 한눈에 보기

[State of JavaScript 2025](https://2025.stateofjs.com/en-US/libraries/front-end-frameworks/)에 따르면, 지난 1년간 프론트엔드 사용 순위는 (Alpine.js와 HTMX가 자리를 바꾼 것을 제외하면) **거의 변동이 없었다**. 생태계가 "요동치는(churning)" 단계에서 "안정되는(settling)" 단계로 넘어갔다는 신호다.

### 핵심 지표 요약

| 프레임워크 | 최신 버전(2026 기준) | 사용률(점유) | 만족도 특징 | 반응성 모델 |
|------------|---------------------|--------------|-------------|-------------|
| **React** | 19.x | 시장 최대(약 44%) | 채용·커뮤니티 압도적 | Compiler 자동 메모이제이션 |
| **Vue** | 3.5 / Vapor 프리뷰 | 높음 | 학습 곡선 완만, 균형 | Signals + Vapor(VDOM 우회) |
| **Angular** | 20 | 엔터프라이즈 중심 | TypeScript-first | Signals + Zoneless |
| **Svelte** | 5 (Runes) | 약 7% | 5년째 상위 만족도 | Runes($state/$derived) |
| **Solid** | 1.x | 약 10% | **5년 연속 최고 만족도** | 진짜 fine-grained signals |
| **Qwik** | 2.x | 낮음(niche) | Resumability 실험적 | Resumable + Signals |

> 참고: 성능 벤치마크에서 Svelte 5는 대체로 가장 빠르고 번들이 작으며(≈28KB), Vue는 Vapor Mode에서 10KB 이하까지 줄고, React는 상대적으로 큰 베이스라인(≈72KB)을 갖는다. 다만 **벤치마크 수치는 측정 조건에 매우 민감**하므로 절대적 순위보다 "경향"으로 읽어야 한다. ([byteiota](https://byteiota.com/react-19-vs-vue-3-6-vs-svelte-5-2026-framework-convergence/), [jsgurujobs](https://jsgurujobs.com/blog/svelte-5-vs-react-19-vs-vue-4-the-2025-framework-war-nobody-expected-performance-benchmarks))

### 2025~2026의 3대 수렴 트렌드

1. **Signals(시그널)의 보편화** — Angular, Vue, Svelte(Runes), Solid, Preact가 모두 시그널 기반 세밀 반응성으로 이동. React만 "컴파일러가 대신 메모이제이션"하는 다른 길을 택했다.
2. **컴파일러 우선(compiler-first)** — Svelte는 원래 컴파일러 기반, Vue는 Vapor Mode, React는 React Compiler로 런타임 오버헤드를 컴파일 시점으로 옮기는 흐름.
3. **서버 우선 렌더링** — RSC(React Server Components), Nuxt/SvelteKit의 서버 로더, Astro의 아일랜드 아키텍처 등 "기본은 서버, 필요한 곳만 클라이언트"가 표준이 되었다.

---

## 2. 프레임워크별 상세 비교

### 2.1 React 19 — 생태계의 중심, "컴파일러의 길"

React는 여전히 시장 점유율 1위이며 채용 시장에서 압도적이다. React 19의 핵심 변화:

- **React Compiler**: 개발자가 손으로 하던 `useMemo`/`useCallback`/`React.memo`를 **컴파일러가 자동 메모이제이션**. 초기 도입 사례에서 불필요한 리렌더가 25~40% 줄었다는 보고가 있다.
- **Server Components(RSC) 안정화**: 데이터 페칭이 클라이언트 번들에 포함되지 않고 서버에서 수행. 번들 크기와 워터폴을 줄인다.
- **Actions API / `use()` 훅**: 폼 제출·비동기 상태(pending/error)를 선언적으로 다룬다. `useActionState`, `useOptimistic`으로 낙관적 업데이트가 쉬워졌다.

```tsx
// React 19: Actions + useActionState — 폼 상태를 선언적으로
import { useActionState } from "react";

async function updateName(prevState: State, formData: FormData): Promise<State> {
  const name = formData.get("name") as string;
  const error = await saveName(name);        // 서버 호출
  if (error) return { error };
  return { success: true };
}

function ProfileForm() {
  const [state, action, isPending] = useActionState(updateName, {});
  return (
    <form action={action}>
      <input name="name" />
      <button disabled={isPending}>{isPending ? "저장 중…" : "저장"}</button>
      {state.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

**장점**: 최대 생태계, 방대한 라이브러리·채용 풀, RSC·Compiler로의 진화. **단점**: 상대적으로 큰 번들, "React 방식"에 대한 학습 부담, 상태 관리 라이브러리 선택 피로.

### 2.2 Vue 3.5 — 균형의 미학, Vapor Mode의 도약

Vue는 학습 곡선이 완만하고 문서가 뛰어나 **빠른 온보딩**에 강하다. 3.5의 핵심:

- **Vapor Mode**: 가상 DOM을 우회해 컴파일 시점에 직접적인 DOM 업데이트 코드를 생성. Solid/Svelte에 근접한 성능을 노리면서 Vue의 DX를 유지한다. DOM 조작 벤치마크에서 최대 36% 개선, Vapor 사용 시 런타임이 10KB 이하로 줄 수 있다.
- **Composition API + `<script setup>`**: 로직 재사용(composables)과 타입 추론이 우수.
- **반응성 개선**: `ref`/`reactive`/`computed` 기반 시그널형 모델이 성숙.

```vue
<!-- Vue 3.5: <script setup> + Composition API -->
<script setup lang="ts">
import { ref, computed } from "vue";

const count = ref(0);
const doubled = computed(() => count.value * 2);  // 자동 추적
</script>

<template>
  <button @click="count++">{{ count }} → {{ doubled }}</button>
</template>
```

**장점**: 완만한 학습 곡선, 단일 파일 컴포넌트(SFC)의 응집력, Nuxt와의 시너지. **단점**: 채용 풀이 React보다 작음, 대규모 엔터프라이즈 레퍼런스는 Angular/React 대비 적음.

### 2.3 Angular 20 — 엔터프라이즈의 표준, Signals + Zoneless

Angular는 프레임워크가 라우팅·폼·HTTP·DI·테스트까지 "다 들어있는(batteries-included)" 풀 프레임워크다. TypeScript-first 팀과 대규모 조직에 적합.

- **Signals**: `signal()`, `computed()`, `effect()`로 세밀 반응성 도입. 기존 Zone.js 기반의 전역 변경 감지 오버헤드를 줄인다.
- **Zoneless 변경 감지**: Zone.js 의존을 제거하는 방향으로 진화. 번들 축소·초기 로딩 개선 보고가 있다.
- **Standalone Components**: NgModule 없이 컴포넌트를 독립적으로 구성하는 것이 표준이 되면서 보일러플레이트가 크게 감소.

```typescript
// Angular 20: Signals 기반 컴포넌트
import { Component, signal, computed } from "@angular/core";

@Component({
  selector: "app-counter",
  standalone: true,
  template: `<button (click)="inc()">{{ count() }} → {{ doubled() }}</button>`,
})
export class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);
  inc() { this.count.update((n) => n + 1); }
}
```

**장점**: 일관된 아키텍처·강한 규약, 대규모 팀의 유지보수성, LTS·엔터프라이즈 지원. **단점**: 가파른 학습 곡선, 상대적으로 무거움, 소규모 프로젝트엔 과함.

### 2.4 Svelte 5 — 컴파일러의 정점, Runes

Svelte는 런타임 프레임워크가 아니라 **컴파일러**다. 빌드 시점에 컴포넌트를 직접적인 DOM 조작 코드로 컴파일하므로 가상 DOM이 없고 번들이 작다. 5의 핵심은 **Runes**:

- `$state`, `$derived`, `$effect`가 암묵적 최상위 반응성을 **명시적 시그널**로 대체. 컴포넌트뿐 아니라 스토어·유틸 함수 어디서든 동작.
- SvelteKit과 결합 시 동급 기능에서 React 계열 대비 50~70% 적은 JS를 배포한다는 보고가 있다.

```svelte
<!-- Svelte 5: Runes -->
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  $effect(() => console.log("count changed:", count));
</script>

<button onclick={() => count++}>{count} → {doubled}</button>
```

**장점**: 최소 번들·최고 수준 성능, 간결한 문법, 5년째 상위 만족도. **단점**: 상대적으로 작은 생태계·채용 풀, 대형 엔터프라이즈 레퍼런스 부족(단, 증가 중).

### 2.5 Solid & Qwik — 성능 최전선의 실험

- **Solid.js**: React와 유사한 JSX를 쓰지만 **진짜 fine-grained signals**로 컴포넌트가 한 번만 실행되고 이후엔 시그널이 DOM을 직접 갱신. **5년 연속 State of JS 최고 만족도**. 사용률은 약 10%로 낮지만 "무엇을 잘 하는지 주목할 가치"가 있다.
- **Qwik**: **Resumability(재개성)** 라는 급진적 아이디어 — 하이드레이션을 하지 않고 서버 상태를 그대로 "재개"해 초기 상호작용까지의 JS를 거의 0에 가깝게 만든다. 아직 niche지만 대규모 콘텐츠 사이트에서 흥미로운 선택지.

---

## 3. 메타프레임워크와 렌더링 전략

프레임워크(라이브러리) 위에 라우팅·데이터 로딩·SSR·빌드를 얹은 것이 **메타프레임워크**다. 실무에서는 사실상 이 레이어를 선택하게 된다.

### 3.1 렌더링 전략 개념 정리

| 전략 | 의미 | 적합 |
|------|------|------|
| **CSR** | 브라우저에서 렌더 | 로그인 후 대시보드, 앱 내부 화면 |
| **SSR** | 요청 시 서버 렌더 | 개인화된 동적 페이지 |
| **SSG** | 빌드 시 정적 생성 | 블로그·문서·마케팅 |
| **ISR** | 정적 + 주기적 재생성 | 준정적 이커머스 목록 |
| **Islands** | 정적 HTML + 부분 하이드레이션 | 콘텐츠 위주 사이트 |
| **PPR** | 정적 셸 즉시 + 동적 스트리밍 | 혼합형(Next.js 16) |

### 3.2 메타프레임워크 비교

- **Next.js (React)**: 최대 점유·최대 커뮤니티. Next.js 16(2025-10)은 **PPR(Partial Prerendering)**을 "Cache Components"로 일반화하는 방향. 안전한 기본 선택이자 가장 많이 논쟁되는 선택. App Router/RSC가 표준.
- **Nuxt (Vue)**: Nitro 엔진 기반으로 SSR/SSG/ISR·파일 기반 라우팅·Layers·풍부한 모듈 생태계. Vue를 대규모로 쓸 때의 사실상 표준.
- **SvelteKit (Svelte)**: 동급 기능에서 React 계열보다 50~70% 적은 JS. TTI·INP에 유리. Svelte 5 Runes로 성숙, 엔터프라이즈 채택 증가.
- **Astro**: **콘텐츠 우선** 사이트(블로그·문서·마케팅·랜딩)의 챔피언. 아일랜드 아키텍처로 기본 JS 0에 가깝고, React/Vue/Svelte를 섞어 쓸 수 있다. 2026-01 Cloudflare 인수로 입지 강화.
- **Remix / React Router v7**: 웹 표준(폼·fetch) 우선 접근. Remix가 React Router v7으로 합류하면서 데이터 로딩·뮤테이션을 표준 웹 방식으로 다룬다.

> 실무 요령: "블로그/문서/마케팅" → Astro, "React 팀의 앱·SaaS" → Next.js, "Vue 팀" → Nuxt, "최소 번들·빠른 배송" → SvelteKit. ([Leapcell](https://leapcell.io/blog/the-2025-frontend-framework-showdown-next-js-nuxt-js-sveltekit-and-astro), [DEV](https://dev.to/pockit_tools/nextjs-vs-remix-vs-astro-vs-sveltekit-in-2026-the-definitive-framework-decision-guide-lp5))

---

## 4. FE 개발자가 개발 시 주의해야 할 점

프레임워크 선택만큼 중요한 것이 **공통적으로 지켜야 할 원칙**이다. 어떤 프레임워크를 쓰든 아래는 무너지면 안 되는 기둥이다.

### 4.1 성능 — Core Web Vitals를 예산으로 관리하라

2024년 3월부터 **INP(Interaction to Next Paint)**가 FID를 대체해 Core Web Vitals의 상호작용 지표가 되었다. 목표치(p75 기준):

| 지표 | 의미 | 목표(Good) |
|------|------|------------|
| **LCP** | 최대 콘텐츠 표시 | ≤ 2.5s |
| **INP** | 상호작용 반응 지연 | ≤ 200ms |
| **CLS** | 누적 레이아웃 이동 | ≤ 0.1 |

**주의점 체크리스트**:
- **성능 예산(performance budget)**을 CI에 넣어라. 예: 상호작용 페이지의 JS를 gzip 기준 ~400KB 이하로 제한. 초과 시 빌드 경고/실패.
- **번들을 코드 분할(code splitting)**하고, 라우트·컴포넌트 단위로 lazy load 하라.
- **하이드레이션을 최소화**하라. 서버 컴포넌트/아일랜드/PPR로 "인터랙티브가 필요한 곳"에만 JS를 보낸다.
- **이미지**: `next/image` 등으로 적절한 크기·포맷(AVIF/WebP)·`loading="lazy"`·명시적 width/height(CLS 방지).
- **RUM(Real User Monitoring)**으로 실제 사용자 지표를 상시 관측하라. Lighthouse "랩 데이터"만 믿지 말 것.
- **리스트 가상화**(react-window, TanStack Virtual)로 대량 렌더링을 잘라내라.

> "Poor vitals increase bounce rates 20–30% and hurt mobile rankings." — [Crystallize Frontend Performance Checklist](https://crystallize.com/blog/frontend-performance-checklist)

### 4.2 접근성(a11y) — WCAG 2.2 AA를 최소선으로

접근성은 "나중에 추가하는 기능"이 아니라 **처음부터의 설계**다. [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/)가 최소 기준:

- **시맨틱 HTML 우선**: `<div onClick>` 대신 `<button>`. 스크린리더·키보드가 공짜로 동작한다.
- **키보드 내비게이션**: 모든 상호작용을 키보드만으로 완주할 수 있어야 한다. 포커스 표시(focus ring)는 대비 ≥3:1로 항상 보이게.
- **터치 타깃 24×24px 이상**(WCAG 2.2 신규 기준), 드래그 전용 조작 금지(대안 제공).
- **폼**: `<label>` 연결, 오류 메시지에 `role="alert"`, `aria-describedby`.
- **색상만으로 정보 전달 금지**, 텍스트 대비 4.5:1 이상.
- **테스트**: axe-core, eslint-plugin-jsx-a11y, 실제 스크린리더(VoiceOver/NVDA)로 조기에 검증.

### 4.3 보안 — XSS를 넘어서

[OWASP Top 10:2025](https://owasp.org/www-project-top-ten/)에서 최상위 위험은 **Broken Access Control(#1), Security Misconfiguration(#2), Supply-chain(#3)**이다. 프론트엔드 관점 주의점:

- **XSS 방지**:
  - `dangerouslySetInnerHTML`/`v-html`/`{@html}`를 남용하지 말고, 불가피하면 **DOMPurify**로 새니타이즈.
  - **CSP(Content-Security-Policy)** 헤더로 인라인 스크립트·외부 소스를 화이트리스트.
- **인증 토큰 저장**: `localStorage`는 XSS에 취약. 가능하면 **`HttpOnly` + `Secure` + `SameSite=Strict` 쿠키**를 사용해 JS 접근을 차단.
- **입력 검증은 서버에서**: 클라이언트 검증은 UX용일 뿐, 신뢰 경계는 서버다. 폼·URL 파라미터·API 입력을 서버에서 엄격히 검증.
- **공급망(supply chain)**: `npm audit`, 잠금 파일 고정, Dependabot/Renovate, 무분별한 서드파티 스크립트·npm 패키지 지양. 하나의 오염된 패키지가 전체를 장악할 수 있다.
- **비밀은 클라이언트에 두지 말 것**: `NEXT_PUBLIC_*` 등 클라이언트 노출 환경변수에 시크릿을 넣지 않는다.

### 4.4 상태 관리 — 필요한 만큼만

- **서버 상태와 클라이언트 상태를 구분**하라. 서버 데이터(캐시·동기화)는 **TanStack Query / SWR / RTK Query**로, UI 상태는 로컬 state나 경량 스토어로.
- **전역 상태 남용 금지**: 모든 것을 Redux/Zustand에 넣지 말 것. 컴포넌트 지역 상태로 충분한 경우가 대부분이다.
- **경량 옵션 선호 흐름**: Redux Toolkit은 여전히 강력하지만, 많은 팀이 **Zustand/Jotai**(React), **Pinia**(Vue), **Signals**(Angular/Svelte) 등 더 가벼운 선택으로 이동.
- **파생 상태는 계산으로**: `computed`/`derived`/`useMemo`로 도출하고, 중복 저장(state 동기화 버그의 근원)을 피하라.

### 4.5 렌더링·하이드레이션 함정

- **하이드레이션 불일치(hydration mismatch)**: 서버와 클라이언트 렌더 결과가 다르면 경고·깜빡임 발생. `Date.now()`, `Math.random()`, `window` 접근을 초기 렌더에서 조심.
- **use client / 서버-클라이언트 경계**(RSC)를 명확히 인식. 서버 컴포넌트에 브라우저 전용 API를 넣지 말 것.
- **워터폴(waterfall) 데이터 페칭** 피하기: 병렬 로딩·프리페치·스트리밍 활용.

### 4.6 타입 안정성 & 에러 처리

- **TypeScript는 사실상 표준**이다([State of JS 2025](https://www.infoq.com/news/2026/03/state-of-js-survey-2025/)에서 TypeScript 지배력 강화 확인). `any` 남용 금지, `strict` 모드 활성화.
- **에러 바운더리**(React `ErrorBoundary`, Vue `errorCaptured`, SvelteKit `+error.svelte`)로 부분 실패를 격리.
- **로딩/에러/빈 상태(empty state)**를 반드시 설계하라. "행복 경로(happy path)"만 만들면 실사용에서 무너진다.

---

## 5. 코드 가이드 (스타일 · 구조 · 도구)

### 5.1 린팅 & 포매팅 — ESLint 9 Flat Config + Prettier

ESLint 9부터 **Flat Config(`eslint.config.js`)**가 기본이다. 기존 `.eslintrc`보다 단순하고 강력하다. 핵심 원칙: **Prettier가 포매팅을, ESLint가 코드 품질을 담당**하고, `eslint-config-prettier`로 둘의 충돌을 제거한다.

```javascript
// eslint.config.js — ESLint 9 Flat Config (TypeScript + React 예시)
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";
import prettier from "eslint-config-prettier";

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    files: ["**/*.{ts,tsx}"],
    plugins: { react, "react-hooks": reactHooks, "jsx-a11y": jsxA11y },
    languageOptions: {
      parserOptions: { projectService: true },
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "react/react-in-jsx-scope": "off",       // React 17+ JSX transform
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/consistent-type-imports": "error",
    },
  },
  prettier,   // 반드시 마지막 — 포매팅 규칙 비활성화
);
```

```json
// .prettierrc — 의도적으로 옵션이 적다(일관성이 목적)
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

> Prettier는 "버그를 잡지 않는다". 오직 일관된 포매팅만 담당한다. 품질·베스트 프랙티스는 ESLint의 몫이다. ([TeachMeIDEA](https://teachmeidea.com/configuring-prettier-and-eslint-for-typescript-javascript-projects/))

### 5.2 네이밍 컨벤션

| 대상 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 | PascalCase | `UserProfileCard` |
| 컴포넌트 파일 | PascalCase | `UserProfileCard.tsx` |
| 훅(hook) | `use` + camelCase | `useUserProfile` |
| 변수·함수 | camelCase | `fetchUserData` |
| 상수 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 타입·인터페이스 | PascalCase | `type UserProfile` |
| 불리언 | is/has/should 접두 | `isLoading`, `hasError` |
| 이벤트 핸들러 | handle 접두 | `handleSubmit` |
| CSS 클래스 | kebab-case / BEM | `card__title--active` |

- **이름은 의도를 드러내라**: `data`, `temp`, `flag` 같은 무의미한 이름 금지.
- **부정형 네이밍 지양**: `isNotReady`보다 `isReady`.

### 5.3 컴포넌트 작성 원칙

```tsx
// ✅ 좋은 예: 단일 책임 · props 타입 명시 · 이른 반환 · 파생 계산
interface UserCardProps {
  user: User;
  onSelect?: (id: string) => void;
}

export function UserCard({ user, onSelect }: UserCardProps) {
  if (!user) return null;                       // early return

  const fullName = `${user.firstName} ${user.lastName}`;  // 파생값

  return (
    <button className="user-card" onClick={() => onSelect?.(user.id)}>
      <span>{fullName}</span>
    </button>
  );
}
```

원칙:
- **단일 책임(SRP)**: 컴포넌트 하나가 한 가지 일만. 200줄을 넘으면 분리를 고려.
- **Props drilling 지양**: 3단계 이상 넘기면 Context/컴포지션/스토어를 검토.
- **로직은 커스텀 훅/컴포저블로 추출**: UI와 로직을 분리해 테스트·재사용성을 높인다.
- **제어/비제어 컴포넌트를 명확히**, **key는 안정적인 id**를 사용(인덱스 key 지양).
- **부수효과(effect)를 최소화**: 렌더 중 계산으로 대체 가능한지 먼저 검토.

### 5.4 폴더 구조 — 기능 기반(Feature-based) & FSD

파일 타입별(`components/`, `hooks/`, `utils/` 전역 나열)보다 **기능(feature) 단위 응집**이 확장에 유리하다. 대규모에서는 **Feature-Sliced Design(FSD)**가 인기.

```
src/
├── app/                 # 앱 초기화, 프로바이더, 라우팅
├── pages/               # 라우트 단위 페이지
├── widgets/             # 페이지를 구성하는 큰 UI 블록
├── features/            # 사용자 시나리오(로그인, 장바구니 담기 등)
│   └── auth/
│       ├── ui/          # 컴포넌트
│       ├── model/       # 상태·로직
│       └── api/         # 데이터 접근
├── entities/            # 도메인 엔티티(User, Product)
└── shared/              # 공용 UI·유틸·설정 (하위 계층 없음)
```

FSD 핵심 규칙: **상위 계층만 하위 계층을 의존**하고, 슬라이스 간에는 **public API(index.ts)로만** 접근해 숨은 결합을 막는다. ([Feature-Sliced Design](https://feature-sliced.design/blog/mastering-eslint-config))

### 5.5 스타일링 전략

- **선택지**: CSS Modules · Tailwind CSS · CSS-in-JS(런타임 비용 주의) · Vanilla Extract(제로 런타임) · 컴포넌트 라이브러리(shadcn/ui, Radix).
- **디자인 토큰**을 CSS 변수로 두어 테마(라이트/다크)를 일원화.
- **런타임 CSS-in-JS는 성능 비용**이 있으므로 대규모에선 제로 런타임 방식이나 유틸리티 CSS를 선호하는 흐름.

### 5.6 Git · 협업 컨벤션

- **Conventional Commits**: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:` 등 타입 접두로 자동 changelog·버전 관리를 지원.
- **작은 PR·명확한 설명**: 리뷰 가능한 크기(가급적 400줄 이하)로 쪼개라.
- **자동화 파이프라인**: `lint-staged` + `husky`로 커밋 전 lint/format, CI에서 타입체크·테스트·번들 예산 검사.
- **테스트**: 단위(Vitest/Jest), 컴포넌트(Testing Library), E2E(Playwright). "구현 세부"가 아니라 "사용자 관점 동작"을 테스트하라.

---

## 6. 선택 가이드: 상황별 추천

| 상황 | 추천 | 이유 |
|------|------|------|
| 대규모 SaaS·풍부한 채용 필요 | **React + Next.js** | 최대 생태계·인력, RSC·Compiler |
| 엔터프라이즈·대형 조직·강한 규약 | **Angular** | 일관 아키텍처, TypeScript-first, LTS |
| 빠른 온보딩·중소 규모 앱 | **Vue + Nuxt** | 완만한 학습 곡선, 균형 |
| 최소 번들·최고 성능·빠른 배송 | **Svelte + SvelteKit** | 컴파일러, 작은 번들, 높은 만족도 |
| 블로그·문서·마케팅(콘텐츠 우선) | **Astro** | 아일랜드, 거의 0 JS, 멀티 프레임워크 |
| 극한 초기 상호작용 성능 실험 | **Solid / Qwik** | fine-grained signals / resumability |

### 마무리: 프레임워크보다 원칙

2025~2026의 결론은 명확하다. **프레임워크 간 성능·기능 격차는 대부분의 제품에서 결정적이지 않다.** fine-grained reactivity, 서버 우선 렌더링, 컴파일러 최적화는 이제 "경쟁 우위"가 아니라 "기본값(table stakes)"이다. 진짜 차이를 만드는 것은:

1. **팀의 숙련도와 채용 가능성**
2. **성능 예산·접근성·보안을 CI로 강제하는 규율**
3. **일관된 코드 스타일과 확장 가능한 구조**

프레임워크는 도구다. 위 원칙을 지키는 팀은 어떤 프레임워크로도 좋은 제품을 만든다.

---

## 참고문헌

참고문헌 전체 목록은 [create_references.py](./create_references.py)로 생성되는 `fe-framework-guide-references.xlsx`를 참고하세요. 주요 출처:

1. [State of JavaScript 2025 — Front-end Frameworks](https://2025.stateofjs.com/en-US/libraries/front-end-frameworks/)
2. [State of JavaScript 2025: A Maturing Ecosystem — InfoQ](https://www.infoq.com/news/2026/03/state-of-js-survey-2025/)
3. [React 19 vs Vue 3.6 vs Svelte 5: 2026 Framework Convergence — byteiota](https://byteiota.com/react-19-vs-vue-3-6-vs-svelte-5-2026-framework-convergence/)
4. [The 2025 Frontend Framework Showdown — Leapcell](https://leapcell.io/blog/the-2025-frontend-framework-showdown-next-js-nuxt-js-sveltekit-and-astro)
5. [Next.js vs Remix vs Astro vs SvelteKit in 2026 — DEV Community](https://dev.to/pockit_tools/nextjs-vs-remix-vs-astro-vs-sveltekit-in-2026-the-definitive-framework-decision-guide-lp5)
6. [Frontend Performance Checklist For 2025 — Crystallize](https://crystallize.com/blog/frontend-performance-checklist)
7. [Front-End Security Best Practices — SecureFlag](https://blog.secureflag.com/2025/11/17/front-end-security-best-practices/)
8. [OWASP Top 10:2025](https://owasp.org/www-project-top-ten/)
9. [WCAG 2.2 — W3C](https://www.w3.org/TR/WCAG22/)
10. [Web Vitals — web.dev](https://web.dev/articles/vitals)
11. [ESLint 9 Flat Config Tutorial — DEV Community](https://dev.to/aolyang/eslint-9-flat-config-tutorial-2bm5)
12. [Mastering ESLint Config — Feature-Sliced Design](https://feature-sliced.design/blog/mastering-eslint-config)

> Powered by Claude Code & Auto Research Pipeline · 2026-07-15
