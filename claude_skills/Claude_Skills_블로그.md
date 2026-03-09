# Claude Skills: AI 에이전트의 프로그래밍 가능한 미래

*단순 프롬프트에서 모듈화된 에이전트 시스템으로 (2025-2026)*

---

## 요약 (TL;DR)

Claude Skills는 AI 에이전트에게 작업 수행 방법을 가르치는 재사용 가능한 모듈입니다. 2025년 10월 베타로 시작한 이 시스템은 불과 6개월 만에 Microsoft, OpenAI 등 주요 기업이 채택한 오픈 스탠다드로 성장했습니다. 학술 연구는 평균 +16.2%p의 성능 향상을 보여주지만, 동시에 26.1%의 스킬에서 보안 취약점이 발견되며 새로운 과제도 드러났습니다.

---

## Claude Skills란 무엇인가?

당신이 특정 작업을 반복적으로 수행한다고 상상해보세요. 매번 처음부터 설명하는 대신, 한 번 가르치고 필요할 때마다 불러올 수 있다면? 이것이 바로 Claude Skills의 핵심입니다.

**Claude Skills는 다음을 할 수 있게 해줍니다:**
- 특정 작업 워크플로우를 재사용 가능한 모듈로 캡슐화
- 필요할 때 동적으로 로드하여 컨텍스트 효율성 극대화
- 스크립트, 참조 문서, 템플릿 등 리소스 포함
- 트리거 조건과 절차적 로직 정의

단순히 긴 프롬프트를 저장하는 것이 아닙니다. Skills는 **프로그램과 유사한 구조**를 가진 에이전트 모듈입니다.

---

## 타임라인: 폭발적 성장의 6개월

### 2025년 10월: Beta 출시

Anthropic이 Claude Skills를 `skills-2025-10-02` beta로 처음 공개했습니다. 초기 반응은 뜨거웠습니다.

> "Claude Skills are awesome, maybe a bigger deal than MCP"
>
> — Simon Willison, [simonwillison.net](https://simonwillison.net/2025/Oct/16/claude-skills/)

### 2025년 12월: 오픈 스탠다드로 도약

단 두 달 만에 Anthropic은 Agent Skills를 **오픈 스탠다드**로 발표했습니다.

> "Today, we're announcing that Agent Skills will be an open standard... The same skill format will work across any AI platform and tool that adopts the standard."
>
> — Anthropic, [Agent Skills 기술 블로그](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

**초기 채택 조직:**
- Microsoft
- OpenAI
- Atlassian
- Figma
- Cursor
- GitHub
- VS Code
- Notion
- Canva
- Cloudflare
- Ramp
- Sentry

### 2026년 1월: 종합 가이드 발행

Anthropic이 32페이지 분량의 ["The Complete Guide to Building Skills for Claude"](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)를 발행했습니다.

### 2026년 2월: 학술 연구 폭발

단 한 달 동안 **4편의 주요 arXiv 논문**이 발표되었습니다:
1. **Data-Driven Analysis** (2월 8일): 40,285개 스킬 분석
2. **Architecture & Security** (2월 12일): 보안 프레임워크 제안
3. **SkillsBench** (2월 13일): 86개 태스크 벤치마크
4. **Skill-Inject** (2월 23일): 취약점 연구

### 2026년 3월: Claude Marketplace

Anthropic이 엔터프라이즈 고객을 위한 Claude Marketplace를 출시했습니다.

**론칭 파트너:**
- **GitLab**: 소프트웨어 라이프사이클 오케스트레이션
- **Harvey**: 법률 작업용 Claude 플랫폼
- **Lovable**: 누구나 앱을 구축할 수 있는 도구
- **Replit**: 자연어로 소프트웨어 생성
- **Rogo**: 금융 전문가용 도구
- **Snowflake**: Cortex Agents

---

## 아키텍처: Progressive Disclosure의 마법

Claude Skills의 핵심 설계 원칙은 **Progressive Disclosure**입니다.

> "The world doesn't need to be loaded all at once to be understood."
>
> — Claude Skills 아키텍처 개념

### 3단계 정보 로딩

**1단계: 메타데이터**
- 스킬 사용 시점만 판단할 수 있을 만큼의 최소 정보
- 전체 내용을 로드하지 않음
- 토큰 효율성 극대화

**2단계: 바디 로딩**
- 스킬이 현재 태스크와 관련 있다고 판단되면 SKILL.md 전체를 컨텍스트에 로드
- 구체적인 지침과 워크플로우 제공

**3단계: 참조 파일**
- 필요 시 추가 파일을 동적으로 탐색
- 파일이 실제로 접근되기 전까지 컨텍스트 소비 없음

### Meta-Tool 아키텍처

Skills는 "도구 안의 도구"로 작동합니다:
- 직접 작업을 수행하지 않음
- 대화 히스토리에 **전문화된 지침을 주입**
- 에이전트의 컨텍스트를 동적으로 수정

---

## SkillsBench: 검증된 효과

### 핵심 수치

2026년 2월, 40명의 연구자가 참여한 대규모 벤치마크 연구가 발표되었습니다.

> "Curated skills improve average pass rates by +16.2 percentage points across 86 tasks spanning 11 domains."
>
> — SkillsBench, [arXiv:2602.12670](https://arxiv.org/abs/2602.12670)

**7,308개 궤적**을 테스트한 결과:
- **평균 성능 향상**: +16.2%p
- **최고 성능 향상**: +51.9%p (헬스케어 도메인)
- **최저 성능 향상**: +4.5%p (소프트웨어 엔지니어링)

### 놀라운 발견: 자체 생성 스킬의 실패

가장 충격적인 발견은 자체 생성 스킬의 결과였습니다.

> "Self-generated skills show no average benefit, suggesting that models cannot write procedural knowledge they benefit from consuming."
>
> — SkillsBench, [arXiv:2602.12670](https://arxiv.org/abs/2602.12670)

**시사점:**
- 모델이 스스로 효과적인 스킬을 작성할 수 없음
- 큐레이션된 스킬이 필수적
- 전문가가 작성한 스킬의 가치

### 작은 모델의 역전

또 다른 흥미로운 발견:

> "Smaller models equipped with skills can match the performance of larger models without skills."
>
> — SkillsBench 연구 결과

**비용 효율성:**
- 큰 모델 비용 절감 가능
- 작은 모델 + 좋은 스킬 = 경쟁력
- 실용적 배포 전략

---

## 보안: 어두운 그림자

### 26.1%의 취약점

2026년 2월 12일, Renjun Xu와 Yang Yan의 연구가 충격적인 수치를 공개했습니다.

> "26.1% of community-contributed skills contain vulnerabilities"
>
> — Agent Skills for Large Language Models, [arXiv:2602.12430](https://arxiv.org/abs/2602.12430)

### 80% 공격 성공률

불과 11일 후, 더 충격적인 연구가 발표되었습니다.

> "We evaluate LLM agent vulnerability to injection attacks through skill files... achieving up to 80% attack success rates across frontier models."
>
> — Skill-Inject, [arXiv:2602.20156](https://arxiv.org/abs/2602.20156)

**Skill-Inject 연구 결과:**
- **202개 인젝션-태스크 쌍** 테스트
- 명백히 악의적인 공격부터 미묘한 공격까지
- 데이터 유출, 파괴적 행동, 랜섬웨어 유사 행동
- 프론티어 모델(Claude Code, Gemini CLI, OpenAI Codex CLI)도 취약

### 해결책은?

> "Model scaling and simple input filtering are insufficient to address these vulnerabilities. Context-aware authentication frameworks are necessary."
>
> — Skill-Inject 연구 결론

Xu와 Yan은 **Skill Trust and Lifecycle Governance Framework**를 제안했습니다:
- 4단계 게이트 기반 권한 모델
- 스킬 라이프사이클 관리
- 컨텍스트 인식 인증

---

## Skills vs MCP: 상호보완적 접근

Claude Skills와 Model Context Protocol(MCP)은 종종 비교되지만, 근본적으로 다른 목적을 가지고 있습니다.

### 핵심 차이점

| | Claude Skills | MCP |
|---|---|---|
| **목적** | **HOW** (방법) 가르침 | **WHAT** (무엇) 접근 제공 |
| **내용** | 절차, 워크플로우, 표준 | 데이터베이스, API, 서비스 |
| **복잡성** | Markdown + YAML | 완전한 프로토콜 사양 |
| **토큰** | Progressive disclosure | 수만 토큰 소비 |
| **사용** | 반복 워크플로우 | 실시간 데이터 접근 |

### 함께 작동

> "MCP provides access to external systems, while Skills provide the context needed to use those connections effectively."
>
> — [Skills vs MCP 기술 비교](https://intuitionlabs.ai/articles/claude-skills-vs-mcp)

**예시:**
- **MCP**: Jira API 연결 제공
- **Skill**: Jira에서 티켓 생성하는 회사 표준 워크플로우

---

## 실제 데이터: 40,285개 스킬 분석

### 소프트웨어 엔지니어링 집중

2026년 2월 8일, George Ling과 동료들의 대규모 데이터 분석이 발표되었습니다.

> "Skill content is highly concentrated in software engineering workflows, with information retrieval and content generation accounting for substantial portions of adoption."
>
> — Agent Skills: A Data-Driven Analysis, [arXiv:2602.08004](https://arxiv.org/abs/2602.08004)

**주요 발견:**
- 주요 마켓플레이스에서 **40,285개 공개 스킬** 분석
- 소프트웨어 엔지니어링 워크플로우에 고도로 집중
- 카테고리별 **공급-수요 불균형** 존재
- Heavy-tailed 길이 분포

### 커뮤니티 마켓플레이스

**SkillsMP.com:**
- 400,000개 이상의 에이전트 스킬
- Claude Code, Codex CLI, ChatGPT 호환
- 카테고리, 작성자, 인기도별 필터링

**SkillHub.club:**
- 7,000개 이상의 AI 평가 스킬
- Claude, Codex, Gemini, OpenCode 지원

---

## SKILL.md: 스킬의 해부학

모든 스킬의 핵심은 **SKILL.md** 파일입니다.

### YAML Frontmatter (필수)

```yaml
---
name: skill-name  # 최대 64자
description: "스킬 설명"  # 최대 1024자
author: "작성자명"  # 선택사항
version: "1.0.0"
tags: ["tag1", "tag2"]
allowed-tools: ["tool1", "tool2"]
---
```

### Markdown 본문 (필수)

형식 제한 없이 자유롭게 작성 가능:
- 명확하고 구체적인 지침
- 예시와 템플릿
- XML 구조화된 데이터
- 사고 과정 장려

### 지원 파일 (선택사항)

```
skill-folder/
├── SKILL.md
├── scripts/
│   └── helper.py
├── references/
│   └── detailed-docs.md
├── assets/
│   └── template.json
└── templates/
    └── output-format.md
```

---

## Skill-Creator: 테스트, 측정, 개선

Anthropic은 스킬 개발을 위한 종합 툴킷인 **Skill-Creator**를 제공합니다.

### 4가지 운영 모드

1. **Create**: 초기 스킬 개발
2. **Eval**: 평가 실행
3. **Improve**: 결과 기반 개선
4. **Benchmark**: 성능 추적

### 다중 에이전트 아키텍처

- **Executor**: eval 프롬프트에 대해 스킬 실행
- **Grader**: 정의된 기대치에 대해 출력 평가
- **Comparator**: 스킬 버전 간 블라인드 A/B 비교
- **Analyzer**: 결과 기반 타겟팅된 개선 제안

### 벤치마크 모드

추적 메트릭:
- **통과율** (Pass rate)
- **경과 시간** (Elapsed time)
- **토큰 사용량** (Token usage)

---

## 주요 연구 논문 깊이 파기

### 1. Agent Skills: Data-Driven Analysis

**arXiv:2602.08004** | 2026년 2월 8일
**저자:** George Ling, Shanshan Zhong, Richard Huang

**핵심 기여:**
- 40,285개 공개 스킬의 대규모 실증 분석
- 소프트웨어 엔지니어링 워크플로우 집중 발견
- 카테고리별 공급-수요 불균형 식별
- 스킬 발행 패턴: 커뮤니티 관심 이동을 추적하는 짧은 버스트

### 2. SkillsBench: Benchmarking

**arXiv:2602.12670** | 2026년 2월 13일
**저자:** Xiangyi Li 외 39명 (총 40명)
**웹사이트:** [skillsbench.ai](https://www.skillsbench.ai/)

**핵심 기여:**
- 11개 도메인에 걸친 86개 태스크 벤치마크
- 7,308개 궤적 테스트
- 큐레이션된 스킬: 평균 +16.2%p 향상
- 자체 생성 스킬: 평균 이점 없음
- 2-3개 모듈의 집중 스킬 > 포괄적 문서

### 3. Architecture, Acquisition, Security

**arXiv:2602.12430** | 2026년 2월 12일 (v3: 2월 17일)
**저자:** Renjun Xu, Yang Yan

**핵심 기여:**
- 모놀리식 LM에서 모듈식 스킬 장착 에이전트로의 전환 분석
- 26.1% 커뮤니티 스킬에 취약점 발견
- Skill Trust and Lifecycle Governance Framework 제안
- 4단계 게이트 기반 권한 모델

### 4. Skill-Inject: Vulnerability Research

**arXiv:2602.20156** | 2026년 2월 23일 (v3: 2월 25일)
**저자:** David Schmotz, Luca Beurer-Kellner, Sahar Abdelnabi, Maksym Andriushchenko
**웹사이트:** [skill-inject.com](https://www.skill-inject.com/)
**GitHub:** [aisa-group/skill-inject](https://github.com/aisa-group/skill-inject)

**핵심 기여:**
- 202개 인젝션-태스크 쌍 포함
- 최대 80% 공격 성공률 (프론티어 모델)
- 데이터 유출, 파괴적 행동, 랜섬웨어 유사 행동
- 모델 스케일링 및 단순 입력 필터링으로 해결 불가
- 컨텍스트 인식 인증 프레임워크 필요성

---

## 주요 조직 및 전략

### Anthropic: 오픈 스탠다드 리더

**전략:**
- Claude Skills를 오픈 스탠다드로 전환
- 광범위한 산업 채택 촉진
- Constitutional AI 훈련 방법 통합

**주요 인물:**
- Dario Amodei (CEO, 전 OpenAI VP of Research)
- Daniela Amodei (President)

### Microsoft, OpenAI: 초기 채택자

**의미:**
- 경쟁사조차 스탠다드 채택
- 크로스 플랫폼 호환성 중시
- AI 에이전트 생태계 표준화

### 커뮤니티: 폭발적 성장

**40만 개 이상의 스킬:**
- SkillsMP.com
- SkillHub.club
- GitHub 커뮤니티 마켓플레이스

---

## 앞으로의 과제

### 1. 보안 거버넌스

**현재 상태:**
- 26.1% 취약점
- 80% 공격 성공률

**필요한 것:**
- Skill Trust Framework 구현
- 컨텍스트 인식 인증
- 라이프사이클 관리

### 2. 자체 생성 스킬

**현재 한계:**
- 모델이 스스로 효과적인 스킬을 작성 못함
- 큐레이션된 스킬에 의존

**미래 방향:**
- 자율 스킬 발견 (SEAgent)
- 조합 스킬 합성
- 강화학습 with 스킬 라이브러리

### 3. 도메인 확장

**현재 집중:**
- 소프트웨어 엔지니어링 과도하게 집중
- 다른 도메인 공급 부족

**기회:**
- 헬스케어 (+51.9%p 효과)
- 법률 (Harvey)
- 금융 (Rogo)
- 과학 연구

### 4. 표준화 및 호환성

**오픈 스탠다드:**
- [agentskills.io](https://agentskills.io) 사양
- 크로스 플랫폼 작동
- 마이그레이션 도구

---

## 프롬프트 엔지니어링에서 스킬 엔지니어링으로

Claude Skills는 단순한 기능 추가가 아닙니다. 이것은 **AI 에이전트와 상호작용하는 방식의 근본적 변화**를 대표합니다.

### 과거: 프롬프트 엔지니어링

```
매번 긴 프롬프트를 작성
→ 컨텍스트 낭비
→ 일관성 부족
→ 재사용 불가
```

### 현재: 스킬 엔지니어링

```
한 번 스킬 작성
→ Progressive disclosure
→ 일관된 워크플로우
→ 재사용 및 공유
```

### 미래: 에이전트 생태계

```
오픈 스탠다드
→ 크로스 플랫폼 호환
→ 커뮤니티 기여
→ 전문화된 에이전트
```

---

## 내 생각

Claude Skills의 6개월은 놀랍습니다. 베타에서 오픈 스탠다드로, 그리고 4편의 주요 학술 논문까지 - 이 속도는 이례적입니다.

**가장 인상적인 점:**

SkillsBench의 발견입니다. "모델이 소비하여 이득을 보는 절차적 지식을 스스로 작성할 수 없음"이라는 결과는 AI 능력의 근본적 한계를 드러냅니다. 이것은 단순히 더 많은 데이터나 더 큰 모델로 해결되지 않습니다. **인간의 전문 지식과 큐레이션이 필수적**입니다.

**가장 우려되는 점:**

보안입니다. 26.1% 취약점과 80% 공격 성공률은 심각합니다. Anthropic이 오픈 스탠다드를 추진하면서 보안 프레임워크도 함께 표준화하지 않으면, 우리는 광범위한 보안 문제에 직면할 수 있습니다.

**가장 기대되는 점:**

작은 모델의 가능성입니다. "스킬을 갖춘 작은 모델 = 스킬 없는 큰 모델"이라는 결과는 비용 효율성과 접근성에 혁명을 일으킬 수 있습니다. 로컬에서 실행 가능한 작은 모델 + 전문가가 큐레이션한 스킬 라이브러리 = 실용적이고 강력한 에이전트.

**전체적으로:**

Claude Skills는 AI 에이전트의 "함수 라이브러리"를 만들고 있습니다. 소프트웨어 엔지니어링에서 라이브러리와 프레임워크가 발전을 가속화했듯이, Skills 생태계는 AI 에이전트 개발을 가속화할 것입니다.

다만, 보안과 거버넌스가 성장 속도를 따라잡아야 합니다. 그렇지 않으면, 이 혁신은 새로운 공격 벡터의 온상이 될 수 있습니다.

2026년 말에 다시 확인해보고, 이 생태계가 어떻게 진화했는지 봅시다.

---

## 자료 및 추가 탐색

### 공식 문서
- **Agent Skills 개요**: [platform.claude.com/docs/agent-skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- **Claude Code Skills**: [code.claude.com/docs/skills](https://code.claude.com/docs/en/skills)
- **오픈 스탠다드**: [agentskills.io](https://agentskills.io)
- **GitHub**: [anthropics/skills](https://github.com/anthropics/skills)

### 주요 블로그 포스트
- [Introducing Agent Skills](https://www.anthropic.com/news/skills)
- [Equipping agents for the real world](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Improving skill-creator](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
- [Skills explained: Skills vs prompts, Projects, MCP](https://claude.com/blog/skills-explained)

### 학술 논문
- **arXiv:2602.08004** - [Agent Skills: A Data-Driven Analysis](https://arxiv.org/abs/2602.08004)
- **arXiv:2602.12670** - [SkillsBench: Benchmarking](https://arxiv.org/abs/2602.12670)
- **arXiv:2602.12430** - [Architecture, Acquisition, Security](https://arxiv.org/abs/2602.12430)
- **arXiv:2602.20156** - [Skill-Inject: Vulnerability](https://arxiv.org/abs/2602.20156)

### 커뮤니티 리소스
- **SkillsMP**: [skillsmp.com](https://skillsmp.com) - 400,000+ 스킬
- **SkillHub**: [skillhub.club](https://www.skillhub.club/) - 7,000+ AI 평가 스킬
- **Simon Willison**: [Claude Skills deep dive](https://simonwillison.net/2025/Oct/16/claude-skills/)
- **Lee Hanchung**: [First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)

### 연구 웹사이트
- **SkillsBench**: [skillsbench.ai](https://www.skillsbench.ai/)
- **Skill-Inject**: [skill-inject.com](https://www.skill-inject.com/)

---

*마지막 업데이트: 2026년 3월*

*Claude Skills에 대해 논의하고 싶으신가요? 댓글 남겨주세요!*

---

## 출처

이 블로그 포스트는 다음으로부터 정보를 종합했습니다:

- Anthropic. (2025). [Introducing Agent Skills](https://www.anthropic.com/news/skills). Anthropic News.
- Anthropic. (2025). [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills). Anthropic Engineering Blog.
- Ling, G., Zhong, S., & Huang, R. (2026). [Agent Skills: A Data-Driven Analysis of Claude Skills for Extending Large Language Model Functionality](https://arxiv.org/abs/2602.08004). arXiv:2602.08004.
- Li, X., et al. (2026). [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks](https://arxiv.org/abs/2602.12670). arXiv:2602.12670.
- Xu, R., & Yan, Y. (2026). [Agent Skills for Large Language Models: Architecture, Acquisition, Security, and the Path Forward](https://arxiv.org/abs/2602.12430). arXiv:2602.12430.
- Schmotz, D., Beurer-Kellner, L., Abdelnabi, S., & Andriushchenko, M. (2026). [Skill-Inject: Measuring Agent Vulnerability to Skill File Attacks](https://arxiv.org/abs/2602.20156). arXiv:2602.20156.
- [Agent Skills Open Standard](https://agentskills.io). Specification and Documentation.
- [Claude Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview). Anthropic Platform.
- Willison, S. (2025). [Claude Skills are awesome, maybe a bigger deal than MCP](https://simonwillison.net/2025/Oct/16/claude-skills/). Simon Willison's Weblog.
- Lee, H. (2025). [Claude Agent Skills: A First Principles Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/). Lee Hanchung's Blog.
- [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf). Anthropic Resources.
- [SkillsBench](https://www.skillsbench.ai/). Official Website.
- [Skill-Inject](https://www.skill-inject.com/). Official Website.
