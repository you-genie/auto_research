# 프론트엔드 프레임워크 완전 정복 (2025~2026)
## PPT 슬라이드 아웃라인 — 프레임워크 비교 · 개발 주의점 · 코드 가이드

---

## Slide 1: 표지 (Cover)
**Visual**: 어두운 남색 배경에 React/Vue/Angular/Svelte 로고가 궤도처럼 배치된 그래픽. 제목 크고 굵게.
**Key Points**:
- 프론트엔드 프레임워크 완전 정복
- 2025~2026: 수렴(Convergence)의 시대
- 비교 · 개발 주의점 · 코드 가이드
**Speaker Notes**: 이 발표는 2025~2026 프론트엔드 생태계를 세 축으로 정리합니다. 첫째 프레임워크별 비교, 둘째 어떤 프레임워크를 쓰든 지켜야 할 개발 주의점, 셋째 실무 코드 스타일 가이드입니다. 핵심 메시지는 "프레임워크 전쟁은 끝났고, 이제 원칙이 차이를 만든다"입니다.

---

## Slide 2: 목차 (Agenda)
**Visual**: 6개 섹션을 아이콘과 함께 나열한 그리드.
**Key Points**:
- 프레임워크 지형도
- 프레임워크별 상세 비교
- 메타프레임워크 & 렌더링 전략
- 개발 시 주의할 점
- 코드 가이드
- 상황별 선택 가이드
**Speaker Notes**: 총 6개 파트입니다. 1~3부는 "무엇을 고를까", 4부는 "무엇을 조심할까", 5부는 "어떻게 쓸까", 6부는 최종 의사결정 표입니다.

---

## Slide 3: 섹션 구분 — Part 1. 지형도
**Visual**: "Part 1" 대형 텍스트 + State of JS 로고.
**Key Points**:
- Part 1
- 2025~2026 프레임워크 지형도
**Speaker Notes**: State of JS 2025는 지난 1년간 사용 순위가 거의 변하지 않았다고 보고합니다. 생태계가 "요동침"에서 "안정됨"으로 넘어갔습니다.

---

## Slide 4: 핵심 지표 한눈에 보기
**Visual**: 6행 비교표(프레임워크 / 버전 / 점유 / 만족도 / 반응성 모델).
**Key Points**:
- React 19: 시장 최대(~44%), Compiler
- Vue 3.5: 균형, Vapor Mode
- Angular 20: 엔터프라이즈, Signals+Zoneless
- Svelte 5: 최소 번들, Runes
- Solid: 5년 연속 최고 만족도
**Speaker Notes**: 벤치마크상 Svelte가 가장 빠르고 번들이 작지만(≈28KB), React는 여전히 점유율 1위입니다. 성능 격차보다 생태계·채용이 실무 선택을 좌우합니다. 수치는 측정 조건에 민감하니 절대 순위보다 경향으로 보십시오.

---

## Slide 5: 2025~2026 3대 수렴 트렌드
**Visual**: 세 갈래가 하나로 모이는 다이어그램.
**Key Points**:
- Signals의 보편화 (Angular/Vue/Svelte/Solid)
- 컴파일러 우선 (Svelte/Vapor/React Compiler)
- 서버 우선 렌더링 (RSC/Islands/PPR)
**Speaker Notes**: 세 프레임워크가 문법은 다르지만 동일한 기술 해법으로 수렴 중입니다. "fine-grained reactivity, 서버 우선, 컴파일러 최적화"는 이제 경쟁 우위가 아니라 기본값입니다.

---

## Slide 6: 섹션 구분 — Part 2. 프레임워크별 비교
**Visual**: "Part 2" 대형 텍스트.
**Key Points**:
- Part 2
- React / Vue / Angular / Svelte / Solid / Qwik
**Speaker Notes**: 각 프레임워크의 최신 기능과 장단점을 실제 코드와 함께 봅니다.

---

## Slide 7: React 19 — "컴파일러의 길"
**Visual**: React Compiler 전/후 리렌더 감소 그래프 + Actions 코드.
**Key Points**:
- React Compiler: 자동 메모이제이션 (리렌더 25~40%↓)
- Server Components 안정화
- Actions / useActionState / useOptimistic
**Speaker Notes**: React는 시그널 대신 "컴파일러가 대신 최적화"하는 길을 택했습니다. useMemo/useCallback을 손으로 관리하던 시대가 저뭅니다. RSC로 데이터 페칭이 클라이언트 번들을 벗어납니다. 장점은 최대 생태계·채용, 단점은 큰 번들과 학습 부담입니다.

---

## Slide 8: Vue 3.5 — 균형과 Vapor Mode
**Visual**: `<script setup>` 코드 블록 + Vapor Mode 성능 막대.
**Key Points**:
- Vapor Mode: VDOM 우회, 최대 36%↑, 10KB 이하
- Composition API + `<script setup>`
- 완만한 학습 곡선
**Speaker Notes**: Vue는 빠른 온보딩과 뛰어난 문서가 강점입니다. Vapor Mode로 Solid/Svelte급 성능을 노리면서도 Vue의 DX를 유지합니다. Nuxt와의 시너지가 큽니다.

---

## Slide 9: Angular 20 — 엔터프라이즈 표준
**Visual**: Signals 컴포넌트 코드 + Zoneless 개념도.
**Key Points**:
- Signals: signal/computed/effect
- Zoneless 변경 감지
- Standalone Components (NgModule 탈피)
**Speaker Notes**: Angular는 라우팅·폼·HTTP·DI·테스트까지 다 들어있는 풀 프레임워크입니다. Signals와 Zoneless로 성능이 개선되고, Standalone으로 보일러플레이트가 줄었습니다. 대규모 팀·강한 규약에 적합하지만 학습 곡선이 가파릅니다.

---

## Slide 10: Svelte 5 — 컴파일러의 정점, Runes
**Visual**: Runes 코드($state/$derived/$effect) + 번들 크기 비교.
**Key Points**:
- Runes: 명시적 시그널
- 가상 DOM 없음, 최소 번들
- React 계열 대비 JS 50~70%↓ (SvelteKit)
**Speaker Notes**: Svelte는 런타임이 아니라 컴파일러입니다. Runes로 반응성이 컴포넌트 밖에서도 동작하게 되었습니다. 번들이 가장 작고 성능이 최상위권이며 5년째 만족도 상위입니다. 생태계·채용 풀이 상대적으로 작은 것이 트레이드오프입니다.

---

## Slide 11: Solid & Qwik — 성능 최전선
**Visual**: 좌우 분할 — Solid(fine-grained signals) / Qwik(resumability).
**Key Points**:
- Solid: 진짜 fine-grained, 5년 연속 최고 만족도
- Qwik: Resumability, 하이드레이션 제거
**Speaker Notes**: Solid는 사용률 10%지만 만족도 1위를 5년째 지킵니다. 컴포넌트가 한 번만 실행되고 시그널이 DOM을 직접 갱신합니다. Qwik은 하이드레이션 없이 서버 상태를 "재개"해 초기 JS를 거의 0으로 만듭니다.

---

## Slide 12: 섹션 구분 — Part 3. 메타프레임워크
**Visual**: "Part 3" 대형 텍스트.
**Key Points**:
- Part 3
- Next.js / Nuxt / SvelteKit / Astro / Remix
**Speaker Notes**: 실무에서는 라이브러리가 아니라 메타프레임워크를 고르게 됩니다.

---

## Slide 13: 렌더링 전략 정리
**Visual**: CSR/SSR/SSG/ISR/Islands/PPR 6칸 매트릭스.
**Key Points**:
- CSR: 앱 내부 화면
- SSR: 개인화 동적
- SSG: 블로그·문서
- Islands/PPR: 콘텐츠 + 부분 인터랙션
**Speaker Notes**: 렌더링 전략은 프레임워크만큼 중요합니다. "기본은 서버, 필요한 곳만 클라이언트"가 2025~2026의 표준 사고방식입니다. Next.js 16의 PPR은 정적 셸을 즉시 주고 동적 부분을 스트리밍합니다.

---

## Slide 14: 메타프레임워크 비교
**Visual**: 5개 메타프레임워크 카드 배열.
**Key Points**:
- Next.js: 최대 점유, PPR/Cache Components
- Nuxt: Vue 대규모 표준, Nitro
- SvelteKit: 최소 JS, INP 유리
- Astro: 콘텐츠 우선, 아일랜드
- Remix/RR v7: 웹 표준 우선
**Speaker Notes**: 블로그·문서는 Astro, React 팀 SaaS는 Next.js, Vue 팀은 Nuxt, 최소 번들은 SvelteKit. Astro는 2026년 1월 Cloudflare에 인수되며 입지를 강화했습니다.

---

## Slide 15: 섹션 구분 — Part 4. 개발 주의점
**Visual**: "Part 4" + 경고 아이콘.
**Key Points**:
- Part 4
- 어떤 프레임워크든 무너지면 안 되는 기둥
**Speaker Notes**: 프레임워크 선택보다 중요한 공통 원칙입니다. 성능·접근성·보안·상태관리·렌더링·타입.

---

## Slide 16: 성능 — Core Web Vitals를 예산으로
**Visual**: LCP/INP/CLS 신호등 게이지 + 성능 예산 개념.
**Key Points**:
- LCP ≤2.5s / INP ≤200ms / CLS ≤0.1
- 성능 예산을 CI로 강제 (JS ~400KB gzip)
- 코드 분할 · 하이드레이션 최소화 · RUM
**Speaker Notes**: 2024년부터 INP가 FID를 대체했습니다. Lighthouse 랩 데이터만 믿지 말고 RUM으로 실사용자 지표를 관측하세요. 나쁜 Vitals는 이탈률을 20~30% 높입니다. 이미지는 크기·포맷·명시적 width/height로 CLS를 막습니다.

---

## Slide 17: 접근성 — WCAG 2.2 AA
**Visual**: 시맨틱 HTML vs div, 포커스 링, 터치 타깃 24px 예시.
**Key Points**:
- 시맨틱 HTML 우선 (`<button>` > `<div onClick>`)
- 키보드 완주 + 포커스 표시 ≥3:1
- 터치 타깃 24×24px, 대비 4.5:1
- axe / jsx-a11y / 스크린리더 테스트
**Speaker Notes**: 접근성은 나중에 붙이는 게 아니라 처음부터의 설계입니다. 시맨틱 HTML을 쓰면 키보드·스크린리더가 공짜로 동작합니다. WCAG 2.2는 터치 타깃과 드래그 대안 등을 새로 요구합니다.

---

## Slide 18: 보안 — XSS를 넘어서
**Visual**: OWASP Top 10:2025 상위 3개 + 토큰 저장 비교(localStorage vs HttpOnly 쿠키).
**Key Points**:
- XSS: v-html/dangerouslySetInnerHTML 주의 + DOMPurify + CSP
- 토큰: HttpOnly+Secure+SameSite 쿠키
- 입력 검증은 서버에서
- 공급망(supply chain) #3 위험
**Speaker Notes**: OWASP Top 10:2025의 1~3위는 접근 제어, 보안 설정 오류, 공급망입니다. 클라이언트로 코드가 이동하면서 XSS·로직 유출이 쉬워졌습니다. localStorage 토큰은 XSS에 취약하니 HttpOnly 쿠키를 쓰고, 시크릿을 클라이언트 환경변수에 넣지 마세요.

---

## Slide 19: 상태 관리 & 렌더링 함정
**Visual**: 서버 상태 vs 클라이언트 상태 분리 다이어그램 + 하이드레이션 불일치 경고.
**Key Points**:
- 서버 상태(TanStack Query/SWR) ↔ UI 상태 분리
- 전역 상태 남용 금지, 경량 스토어 선호
- 하이드레이션 불일치 주의 (Date/random/window)
- 로딩·에러·빈 상태 반드시 설계
**Speaker Notes**: 모든 것을 Redux에 넣지 마세요. 서버 데이터는 쿼리 라이브러리로, UI 상태는 지역 상태로 나눕니다. 초기 렌더에서 Date.now/Math.random/window 접근은 하이드레이션 불일치를 만듭니다. 행복 경로만 만들면 실사용에서 무너집니다.

---

## Slide 20: 섹션 구분 — Part 5. 코드 가이드
**Visual**: "Part 5" + 코드 브래킷 아이콘.
**Key Points**:
- Part 5
- 스타일 · 구조 · 도구
**Speaker Notes**: 일관성이 곧 유지보수성입니다.

---

## Slide 21: 린팅 & 포매팅 — ESLint 9 + Prettier
**Visual**: eslint.config.js Flat Config 코드 + 역할 분담 도식.
**Key Points**:
- ESLint 9 Flat Config가 기본
- ESLint=품질, Prettier=포매팅
- eslint-config-prettier로 충돌 제거
**Speaker Notes**: ESLint 9부터 flat config가 기본입니다. Prettier는 버그를 잡지 않고 포매팅만 담당합니다. 둘의 충돌은 eslint-config-prettier를 마지막에 배치해 제거합니다. Prettier는 옵션이 적은 게 의도입니다 — 일관성이 목적이니까요.

---

## Slide 22: 네이밍 & 컴포넌트 원칙
**Visual**: 네이밍 컨벤션 표 + 좋은 컴포넌트 코드.
**Key Points**:
- 컴포넌트 PascalCase, 훅 useXxx, 상수 UPPER_SNAKE
- 불리언 is/has, 핸들러 handle
- 단일 책임 · early return · 파생 계산
- props drilling 3단계↑ → Context/스토어
**Speaker Notes**: 이름은 의도를 드러내야 합니다. data/temp/flag 같은 무의미한 이름을 피하고, 부정형 네이밍을 지양하세요. 컴포넌트는 한 가지 일만 하고, 로직은 커스텀 훅으로 추출해 테스트·재사용성을 높입니다.

---

## Slide 23: 폴더 구조 — Feature-Sliced Design
**Visual**: FSD 계층 다이어그램(app→pages→widgets→features→entities→shared).
**Key Points**:
- 파일 타입별 < 기능(feature)별 응집
- FSD: 상위 계층만 하위 의존
- 슬라이스 간 public API(index.ts)로만 접근
**Speaker Notes**: components/hooks/utils로 전역 나열하는 방식은 커질수록 무너집니다. 기능 단위로 묶으세요. 대규모에서는 FSD가 인기입니다. 계층 규칙과 public API로 숨은 결합을 막습니다.

---

## Slide 24: Git · 협업 · 테스트
**Visual**: Conventional Commits 예시 + CI 파이프라인 도식.
**Key Points**:
- Conventional Commits (feat/fix/docs…)
- 작은 PR(≤400줄), lint-staged+husky
- CI: 타입체크·테스트·번들 예산
- 테스트: Vitest/Testing Library/Playwright
**Speaker Notes**: 커밋 컨벤션으로 changelog·버전을 자동화합니다. 커밋 전 lint/format을 자동화하고, CI에서 타입체크·테스트·번들 예산을 강제합니다. 테스트는 구현 세부가 아니라 사용자 관점 동작을 검증하세요.

---

## Slide 25: 상황별 선택 가이드
**Visual**: 6행 의사결정 표(상황 → 추천 → 이유).
**Key Points**:
- 대규모 SaaS → React+Next.js
- 엔터프라이즈 → Angular
- 빠른 온보딩 → Vue+Nuxt
- 최소 번들 → Svelte+SvelteKit
- 콘텐츠 우선 → Astro
**Speaker Notes**: 정답은 없습니다. 팀의 숙련도와 채용 가능성, 제품 특성에 맞추세요.

---

## Slide 26: 마무리 — 프레임워크보다 원칙
**Visual**: "Frameworks are tools. Principles win." 대형 카피.
**Key Points**:
- 프레임워크 간 격차는 대부분 결정적이지 않다
- 진짜 차이: 팀 숙련도 · 규율(CI) · 일관된 구조
**Speaker Notes**: fine-grained reactivity, 서버 우선, 컴파일러 최적화는 이제 기본값입니다. 성능 예산·접근성·보안을 CI로 강제하고, 일관된 스타일과 확장 가능한 구조를 갖춘 팀은 어떤 프레임워크로도 좋은 제품을 만듭니다. 프레임워크는 도구일 뿐입니다.

---

## Slide 27: Q&A / 참고문헌
**Visual**: 주요 출처 로고(State of JS, web.dev, OWASP, WCAG, ESLint).
**Key Points**:
- 감사합니다
- 참고문헌: fe-framework-guide-references.xlsx
**Speaker Notes**: 질문을 받습니다. 상세 출처는 references 파일을 참고하세요.
