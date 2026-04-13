"""
Meta HyperAgents 개념 데모
============================
이 데모는 HyperAgents의 핵심 아이디어인 "자기 참조적 자기 개선"을
간단하게 시뮬레이션합니다.

실제 HyperAgents(facebookresearch/HyperAgents)는 수천 줄의 코드와
여러 LLM API, Docker 환경이 필요하지만, 이 데모는
그 핵심 개념을 이해하기 위한 최소한의 구현을 보여줍니다.

핵심 개념:
- 태스크 에이전트(Task Agent): 실제 문제를 풀어요
- 메타 에이전트(Meta Agent): 태스크 에이전트를 개선해요
- HyperAgents의 혁신: 메타 에이전트도 스스로 수정 가능!

실행 방법:
  pip install -r requirements.txt
  python hyperagent_demo.py

주의: OpenAI API 키가 없어도 Mock 모드로 실행됩니다.
"""

import json
import os
import random
import time
from dataclasses import dataclass, field
from typing import Optional

# 시각적 출력을 위한 rich 라이브러리 (없으면 기본 출력)
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


# ──────────────────────────────────────────────────────────────────
# 유틸리티 함수
# ──────────────────────────────────────────────────────────────────

def print_header(text: str) -> None:
    """섹션 헤더를 출력합니다."""
    if RICH_AVAILABLE:
        console.print(f"\n[bold navy_blue]{'='*60}[/bold navy_blue]")
        console.print(f"[bold white]  {text}[/bold white]")
        console.print(f"[bold navy_blue]{'='*60}[/bold navy_blue]\n")
    else:
        print(f"\n{'='*60}")
        print(f"  {text}")
        print(f"{'='*60}\n")


def print_step(label: str, content: str, color: str = "cyan") -> None:
    """단계별 정보를 출력합니다."""
    if RICH_AVAILABLE:
        console.print(f"[{color}]{label}:[/{color}] {content}")
    else:
        print(f"{label}: {content}")


# ──────────────────────────────────────────────────────────────────
# 코어 데이터 클래스
# ──────────────────────────────────────────────────────────────────

@dataclass
class AgentConfig:
    """에이전트의 설정을 담는 클래스입니다.

    HyperAgents에서 이 설정 자체가 수정 가능한 코드로 존재합니다.
    메타 에이전트가 이 설정을 분석하고 개선합니다.
    """
    # 태스크 에이전트 설정
    max_attempts: int = 3          # 최대 시도 횟수
    temperature: float = 0.7       # 생성 다양성
    use_chain_of_thought: bool = False  # 단계적 추론 사용 여부

    # 메타 에이전트 설정 (HyperAgents의 핵심!)
    meta_strategy: str = "basic"   # 개선 전략 타입
    memory_enabled: bool = False   # 영구 메모리 활성화 여부

    # 성능 추적
    iteration: int = 0             # 현재 반복 횟수
    performance_history: list = field(default_factory=list)


@dataclass
class TaskResult:
    """태스크 실행 결과를 담는 클래스입니다."""
    task: str
    answer: str
    score: float          # 0.0 ~ 1.0
    attempts: int
    reasoning: str = ""   # 추론 과정


@dataclass
class MetaImprovement:
    """메타 에이전트가 적용한 개선사항을 기록합니다."""
    iteration: int
    previous_score: float
    new_score: float
    changes: dict         # 변경된 설정들
    insight: str          # 개선의 근거


# ──────────────────────────────────────────────────────────────────
# 태스크 에이전트 (Task Agent)
# ──────────────────────────────────────────────────────────────────

class TaskAgent:
    """태스크 에이전트: 실제 문제를 풀어요.

    현재 구성(config)에 따라 다른 방식으로 문제를 해결합니다.
    메타 에이전트가 config를 수정하면 성능이 달라집니다.
    """

    def __init__(self, config: AgentConfig, memory: Optional[dict] = None):
        self.config = config
        # 메모리가 활성화된 경우 이전 실행의 인사이트를 활용
        self.memory = memory or {}

    def solve(self, task: str, expected_keywords: list[str]) -> TaskResult:
        """주어진 태스크를 현재 설정으로 해결합니다."""

        # 메모리에서 유사한 태스크 검색 (HyperAgents가 자율 개발한 영구 메모리 흉내)
        memory_hint = ""
        if self.config.memory_enabled and self.memory:
            for past_task, past_info in self.memory.items():
                if any(kw in task for kw in past_info.get("keywords", [])):
                    memory_hint = f"[메모리 힌트] 유사 태스크 '{past_task}'에서 학습: {past_info.get('insight', '')}"
                    break

        # 단계적 추론(Chain-of-Thought) 적용 여부에 따라 답변 품질 결정
        if self.config.use_chain_of_thought:
            reasoning = self._chain_of_thought_reasoning(task, memory_hint)
        else:
            reasoning = self._basic_reasoning(task, memory_hint)

        # 실제 HyperAgents는 LLM API를 호출하지만
        # 이 데모에서는 규칙 기반으로 점수를 시뮬레이션합니다
        score = self._simulate_score(task, expected_keywords, reasoning)

        return TaskResult(
            task=task,
            answer=f"{reasoning}\n→ 답변 생성 완료",
            score=score,
            attempts=1,
            reasoning=reasoning
        )

    def _basic_reasoning(self, task: str, memory_hint: str) -> str:
        """기본 추론 방식: 단순 처리."""
        return f"[기본 방식] 태스크 분석 중... {memory_hint or '메모리 없음'}"

    def _chain_of_thought_reasoning(self, task: str, memory_hint: str) -> str:
        """단계적 추론: 더 정확한 처리."""
        steps = [
            f"Step 1: 태스크 파싱 - '{task[:30]}...'",
            f"Step 2: 관련 지식 검색 {'(메모리 활용)' if memory_hint else '(메모리 없음)'}",
            f"Step 3: 단계별 추론 적용",
            f"Step 4: 답변 검증",
        ]
        return " | ".join(steps)

    def _simulate_score(self, task: str, expected_keywords: list[str], reasoning: str) -> float:
        """
        실제 LLM 없이 점수를 시뮬레이션합니다.

        실제 HyperAgents는:
        1. LLM이 답변을 생성하고
        2. 평가 루브릭(rubric)으로 점수를 매기고
        3. 이 점수를 기반으로 자기 개선을 수행합니다
        """
        base_score = 0.3  # 기본 점수

        # Chain-of-Thought 사용 시 보너스
        if self.config.use_chain_of_thought:
            base_score += 0.25

        # 메모리 사용 시 보너스
        if self.config.memory_enabled and self.memory:
            base_score += 0.15

        # temperature가 낮을수록 (더 결정론적) 정확한 태스크에 유리
        if self.config.temperature < 0.5:
            base_score += 0.1

        # 약간의 무작위성 추가 (현실감)
        noise = random.uniform(-0.05, 0.1)

        return min(1.0, max(0.0, base_score + noise))


# ──────────────────────────────────────────────────────────────────
# 메타 에이전트 (Meta Agent)
# ──────────────────────────────────────────────────────────────────

class MetaAgent:
    """메타 에이전트: 태스크 에이전트의 설정을 개선해요.

    HyperAgents의 핵심 혁신:
    이 메타 에이전트 자체도 수정 가능합니다!
    meta_strategy 설정이 바뀌면 개선 방식 자체가 달라집니다.
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        # 영구 메모리: 도메인 간 전이 가능한 인사이트 저장
        self.persistent_memory: dict = {}
        self.improvement_log: list[MetaImprovement] = []

    def analyze_and_improve(
        self,
        results: list[TaskResult],
        current_config: AgentConfig
    ) -> tuple[AgentConfig, MetaImprovement]:
        """성능 결과를 분석하고 설정을 개선합니다.

        HyperAgents에서는 이 메서드 자체의 코드도 LLM이 수정할 수 있습니다.
        meta_strategy가 'advanced'로 바뀌면 더 정교한 분석을 수행합니다.
        """

        # 현재 평균 점수 계산
        avg_score = sum(r.score for r in results) / len(results) if results else 0.0

        # 개선 전략에 따라 다른 분석 수행
        if current_config.meta_strategy == "basic":
            changes, insight = self._basic_improvement(results, current_config)
        elif current_config.meta_strategy == "advanced":
            changes, insight = self._advanced_improvement(results, current_config)
        else:
            # 메타 메커니즘 자체의 자기 개선 시뮬레이션
            # (실제 HyperAgents에서는 LLM이 이 부분의 코드를 재작성합니다)
            changes, insight = self._meta_meta_improvement(results, current_config)

        # 새로운 설정 적용
        new_config = self._apply_changes(current_config, changes)

        # 영구 메모리 업데이트 (도메인 간 전이 가능)
        self._update_memory(results, insight)

        improvement = MetaImprovement(
            iteration=current_config.iteration,
            previous_score=avg_score,
            new_score=avg_score + random.uniform(0.05, 0.15),  # 예상 개선
            changes=changes,
            insight=insight
        )
        self.improvement_log.append(improvement)

        return new_config, improvement

    def _basic_improvement(
        self,
        results: list[TaskResult],
        config: AgentConfig
    ) -> tuple[dict, str]:
        """기본 개선 전략: 단순한 하이퍼파라미터 조정."""
        changes = {}

        avg_score = sum(r.score for r in results) / len(results) if results else 0.0

        if avg_score < 0.5 and not config.use_chain_of_thought:
            # 점수가 낮으면 CoT 활성화
            changes["use_chain_of_thought"] = True
            insight = "성능 부족 감지 → Chain-of-Thought 추론 활성화"
        elif avg_score < 0.6:
            # temperature 조정
            changes["temperature"] = max(0.1, config.temperature - 0.2)
            insight = "일관성 개선 필요 → temperature 낮춤"
        else:
            insight = "성능 양호 → 현재 설정 유지"

        # 메타 전략 자체를 업그레이드! (HyperAgents의 핵심 차별점)
        if config.iteration >= 2 and avg_score > 0.5:
            changes["meta_strategy"] = "advanced"
            insight += " + 메타 전략을 'advanced'로 업그레이드!"

        return changes, insight

    def _advanced_improvement(
        self,
        results: list[TaskResult],
        config: AgentConfig
    ) -> tuple[dict, str]:
        """고급 개선 전략: 더 정교한 분석.

        이 전략 자체가 'basic'에서 자동으로 진화한 결과입니다.
        """
        changes = {}

        # 성능 트렌드 분석
        if len(config.performance_history) >= 2:
            trend = config.performance_history[-1] - config.performance_history[-2]
            if trend < 0:
                # 성능이 하락하면 메모리 활성화
                changes["memory_enabled"] = True

        # 모든 결과의 reasoning 패턴 분석
        all_use_cot = all("Step" in r.reasoning for r in results)
        if not all_use_cot:
            changes["use_chain_of_thought"] = True

        avg_score = sum(r.score for r in results) / len(results) if results else 0.0

        # 충분히 좋으면 메타 전략 자체를 다시 진화
        if avg_score > 0.7 and config.iteration >= 4:
            changes["meta_strategy"] = "self_referential"
            insight = "고성능 달성 → 메타 전략을 'self_referential'로 최종 진화!"
        else:
            insight = f"고급 분석 완료 (점수: {avg_score:.2f}) → 메모리 및 CoT 최적화"

        return changes, insight

    def _meta_meta_improvement(
        self,
        results: list[TaskResult],
        config: AgentConfig
    ) -> tuple[dict, str]:
        """메타-메타 개선: 메타 에이전트 자체의 자기 수정.

        HyperAgents의 핵심 혁신을 가장 잘 표현하는 부분입니다.
        이 전략은 메타 에이전트가 자신의 개선 방식 자체를 수정합니다.

        실제 HyperAgents에서는 LLM이 이 함수의 Python 코드를 직접 재작성하고,
        재작성된 코드를 실행 가능한 환경에서 테스트한 후 아카이브에 저장합니다.
        """
        insight = (
            "[자기 참조적 개선] 메타 에이전트가 자신의 전략을 분석하고 재설계했습니다.\n"
            "  - 영구 메모리 시스템 도입 (자율 발견)\n"
            "  - 2단계 처리 파이프라인 구축 (자율 발견)\n"
            "  - 크로스도메인 인사이트 전이 활성화"
        )
        changes = {
            "memory_enabled": True,
            "use_chain_of_thought": True,
            "temperature": 0.3,
        }
        return changes, insight

    def _apply_changes(self, config: AgentConfig, changes: dict) -> AgentConfig:
        """변경사항을 새로운 설정에 적용합니다."""
        import copy
        new_config = copy.deepcopy(config)
        new_config.iteration += 1

        for key, value in changes.items():
            setattr(new_config, key, value)

        return new_config

    def _update_memory(self, results: list[TaskResult], insight: str) -> None:
        """영구 메모리를 업데이트합니다.

        이 인사이트는 다른 도메인의 태스크에도 전이됩니다.
        (HyperAgents의 크로스도메인 전이 능력 시뮬레이션)
        """
        for result in results:
            # 태스크 키워드 추출 (단순화)
            keywords = result.task.split()[:3]
            self.persistent_memory[result.task[:30]] = {
                "score": result.score,
                "keywords": keywords,
                "insight": insight[:50],
            }


# ──────────────────────────────────────────────────────────────────
# HyperAgent 오케스트레이터
# ──────────────────────────────────────────────────────────────────

class HyperAgentOrchestrator:
    """HyperAgents의 전체 실행 루프를 관리합니다.

    실제 HyperAgents의 generate_loop.py에 해당합니다.
    태스크 에이전트 실행 → 메타 에이전트 분석 → 설정 업데이트 → 반복
    """

    def __init__(self):
        self.config = AgentConfig()
        self.meta_agent = MetaAgent(self.config)
        self.all_results: list[dict] = []

    def run(self, tasks: list[dict], n_iterations: int = 5) -> None:
        """지정된 반복 횟수만큼 자기 개선 루프를 실행합니다."""

        print_header("Meta HyperAgents 자기 개선 데모 시작")

        if RICH_AVAILABLE:
            console.print("[dim]실제 HyperAgents는 LLM API와 Docker 환경에서 실행됩니다.[/dim]")
            console.print("[dim]이 데모는 핵심 개념을 Python으로 시뮬레이션합니다.\n[/dim]")

        for iteration in range(n_iterations):
            print_header(f"반복 {iteration + 1}/{n_iterations} — 도메인: 코딩 태스크")

            # 1단계: 태스크 에이전트 실행
            task_agent = TaskAgent(
                config=self.config,
                memory=self.meta_agent.persistent_memory  # 영구 메모리 전달
            )

            print_step("현재 설정",
                f"CoT={self.config.use_chain_of_thought}, "
                f"Memory={self.config.memory_enabled}, "
                f"MetaStrategy={self.config.meta_strategy}, "
                f"Temp={self.config.temperature:.1f}",
                "yellow"
            )

            # 태스크 실행
            iteration_results = []
            for task_info in tasks:
                time.sleep(0.3)  # 실행 시뮬레이션
                result = task_agent.solve(
                    task=task_info["task"],
                    expected_keywords=task_info["keywords"]
                )
                iteration_results.append(result)
                print_step(
                    f"  태스크",
                    f"'{task_info['task'][:40]}...' → 점수: {result.score:.3f}",
                    "green" if result.score > 0.6 else "red"
                )

            # 현재 평균 점수
            avg_score = sum(r.score for r in iteration_results) / len(iteration_results)
            self.config.performance_history.append(avg_score)

            print_step("평균 점수", f"{avg_score:.3f}", "bold")

            # 2단계: 메타 에이전트가 설정 개선 (HyperAgents의 핵심!)
            print(f"\n  [메타 에이전트] 분석 중... (전략: {self.config.meta_strategy})")
            time.sleep(0.5)

            new_config, improvement = self.meta_agent.analyze_and_improve(
                results=iteration_results,
                current_config=self.config
            )

            # 메타 개선사항 출력
            if improvement.changes:
                print_step("적용된 개선사항", str(improvement.changes), "cyan")
            print_step("메타 인사이트", improvement.insight, "magenta")

            # 3단계: 설정 업데이트
            self.config = new_config

            # 결과 기록
            self.all_results.append({
                "iteration": iteration + 1,
                "avg_score": avg_score,
                "meta_strategy": self.config.meta_strategy,
                "changes": improvement.changes,
            })

        # 최종 결과 출력
        self._print_final_report()

    def _print_final_report(self) -> None:
        """전체 실행 결과 요약을 출력합니다."""
        print_header("자기 개선 결과 요약")

        if RICH_AVAILABLE:
            table = Table(title="반복별 성능 향상", show_header=True)
            table.add_column("반복", style="cyan", justify="center")
            table.add_column("평균 점수", justify="center")
            table.add_column("메타 전략", style="magenta")
            table.add_column("주요 변경", style="yellow")

            for r in self.all_results:
                score = r["avg_score"]
                score_str = f"[green]{score:.3f}[/green]" if score > 0.6 else f"[red]{score:.3f}[/red]"
                changes = ", ".join(f"{k}={v}" for k, v in r["changes"].items()) if r["changes"] else "없음"
                table.add_row(
                    str(r["iteration"]),
                    score_str,
                    r["meta_strategy"],
                    changes[:50]
                )

            console.print(table)
        else:
            for r in self.all_results:
                print(f"  반복 {r['iteration']}: 점수={r['avg_score']:.3f}, 전략={r['meta_strategy']}")

        # 시작 vs 종료 비교
        if len(self.all_results) >= 2:
            start_score = self.all_results[0]["avg_score"]
            end_score = self.all_results[-1]["avg_score"]
            improvement_pct = ((end_score - start_score) / start_score) * 100

            print()
            print_step(
                "성능 향상",
                f"{start_score:.3f} → {end_score:.3f} (+{improvement_pct:.1f}%)",
                "bold green"
            )

        # 메모리에 저장된 인사이트 출력
        if self.meta_agent.persistent_memory:
            print()
            print_step(
                "영구 메모리 (자율 개발된 기능)",
                f"{len(self.meta_agent.persistent_memory)}개 태스크 인사이트 저장됨",
                "bold cyan"
            )
            print("  → 다른 도메인에서도 이 인사이트를 활용할 수 있습니다.")

        # HyperAgents 핵심 메시지
        print()
        if RICH_AVAILABLE:
            console.print(Panel(
                "[bold]HyperAgents의 핵심 혁신[/bold]\n\n"
                "메타 전략이 'basic' → 'advanced' → 'self_referential'로 자동 진화했습니다.\n"
                "이는 태스크 성능 개선뿐 아니라, [bold cyan]개선 방법 자체가 진화[/bold cyan]했음을 의미합니다.\n\n"
                "[dim]실제 HyperAgents: arxiv.org/abs/2603.19461[/dim]",
                border_style="gold1",
                title="Meta HyperAgents Demo"
            ))


# ──────────────────────────────────────────────────────────────────
# 샘플 태스크 데이터
# ──────────────────────────────────────────────────────────────────

SAMPLE_TASKS = [
    {
        "task": "Python으로 피보나치 수열을 동적 프로그래밍으로 구현하고 시간복잡도를 분석하세요.",
        "keywords": ["피보나치", "동적", "O(n)", "메모이제이션"],
    },
    {
        "task": "주어진 논문의 실험 방법론을 평가하고 통계적 유의성을 검토하세요.",
        "keywords": ["방법론", "통계", "유의성", "샘플"],
    },
    {
        "task": "로봇 팔의 보상 함수를 설계하여 목표 지점까지의 최적 경로를 학습하도록 하세요.",
        "keywords": ["보상", "강화학습", "경로", "최적화"],
    },
]


# ──────────────────────────────────────────────────────────────────
# 메인 실행
# ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print()
    if RICH_AVAILABLE:
        console.print("[bold gold1]Meta HyperAgents 개념 데모[/bold gold1]")
        console.print("[dim]arXiv:2603.19461 | ICLR 2026 | Meta FAIR & Superintelligence Labs[/dim]")
    else:
        print("Meta HyperAgents 개념 데모")
        print("arXiv:2603.19461 | ICLR 2026")

    # 재현성을 위한 랜덤 시드 설정
    random.seed(42)

    # HyperAgent 오케스트레이터 초기화 및 실행
    orchestrator = HyperAgentOrchestrator()
    orchestrator.run(
        tasks=SAMPLE_TASKS,
        n_iterations=5  # 실제 HyperAgents는 수십~수백 회 반복
    )

    print()
    print("데모 완료. 실제 HyperAgents를 사용하려면:")
    print("  https://github.com/facebookresearch/Hyperagents")
