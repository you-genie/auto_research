"""
OpenIntelligentUI 서베이 — 발표자료(.pptx) + 슬라이드 아웃라인(.md) 생성 스크립트

실행: uv run --with python-pptx python3 build_pptx.py
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "Malgun Gothic"

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
BLUE = RGBColor(0x4A, 0x7F, 0xB5)
LIGHT = RGBColor(0xEE, 0xF4, 0xFB)
ORANGE = RGBColor(0xD9, 0x82, 0x2B)
PALE_OR = RGBColor(0xFF, 0xF4, 0xE6)
GREEN = RGBColor(0x6A, 0x9A, 0x4A)
PALE_GR = RGBColor(0xF3, 0xF8, 0xEE)
RED = RGBColor(0xC7, 0x50, 0x50)
PALE_RD = RGBColor(0xFD, 0xEC, 0xEC)
GRAY = RGBColor(0x5A, 0x64, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1E, 0x25, 0x2E)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

OUTLINE = []  # (title, visual, points, notes)


# ---------- 도우미 ----------
def txt(slide, x, y, w, h, text, size=16, bold=False, color=INK, align=PP_ALIGN.LEFT,
        anchor=MSO_ANCHOR.TOP, font=FONT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = font
    return tb


def box(slide, x, y, w, h, text="", fill=LIGHT, line=BLUE, size=14, bold=False, color=NAVY,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE, align=PP_ALIGN.CENTER, lw=1.25):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.12
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    lines = text if isinstance(text, list) else [text]
    for i, line_t in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line_t
        r.font.size = Pt(size if i == 0 else max(size - 3, 10))
        r.font.bold = bold if i == 0 else False
        r.font.color.rgb = color
        r.font.name = FONT
    return s


def arrow(slide, x1, y1, x2, y2, color=BLUE, w=2.0, dashed=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    if dashed:
        d = etree.SubElement(ln, qn("a:prstDash"))
        d.set("val", "dash")
    tail = etree.SubElement(ln, qn("a:tailEnd"))
    tail.set("type", "triangle")
    return c


def base(title, section=None, notes=""):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    txt(s, 0.6, 0.35, 11.5, 0.8, title, size=28, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    if section:
        txt(s, 9.8, 7.02, 3.0, 0.3, section, size=10, color=GRAY, align=PP_ALIGN.RIGHT)
    n = len(prs.slides)
    txt(s, 0.6, 7.02, 1.0, 0.3, str(n), size=10, color=GRAY)
    s.notes_slide.notes_text_frame.text = notes
    return s


def record(title, visual, points, notes):
    OUTLINE.append((title, visual, points, notes))


# ---------- 1. 표지 ----------
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
acc = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.55), Inches(1.6), Inches(0.08))
acc.fill.solid(); acc.fill.fore_color.rgb = ORANGE; acc.line.fill.background()
txt(s, 0.8, 1.7, 11.5, 1.0, "OpenIntelligentUI 서베이", size=44, bold=True, color=WHITE)
txt(s, 0.8, 2.65, 11.5, 0.8, "ChatGPT Intelligent UI의 오픈소스 재현과 생성형 UI 포맷", size=22, color=RGBColor(0xDC, 0xE8, 0xF5))
txt(s, 0.8, 3.9, 11.5, 0.5, "CopilotKit 구현 · Thesys 구현 · OpenUI Lang · A2UI · json-render", size=16, color=RGBColor(0xB8, 0xCC, 0xE4))
txt(s, 0.8, 6.3, 11.5, 0.4, "2026-10-23", size=14, color=RGBColor(0xB8, 0xCC, 0xE4))
notes = ("안녕하십니까. 오늘은 OpenAI가 ChatGPT에 도입한 Intelligent UI를 오픈소스로 재현한 두 프로젝트, "
         "즉 CopilotKit의 OpenIntelligentUI와 Thesys의 open-intelligent-ui를 비교하고, 그 아래에 놓인 생성형 UI 포맷의 트레이드오프를 정리하겠습니다.")
s.notes_slide.notes_text_frame.text = notes
record("표지", "네이비 배경, 큰 제목과 부제, 주황 강조선", ["OpenIntelligentUI 서베이", "생성형 UI 포맷 비교"], notes)

# ---------- 2. 아젠다 ----------
notes = ("발표는 세 부분으로 구성됩니다. 먼저 배경과 스펙트럼, 다음으로 두 구현의 내부 구조, 마지막으로 비교와 한계, 선택 기준입니다.")
s = base("아젠다", None, notes)
items = [("01", "배경과 스펙트럼", "원본 · 이름 충돌 · 프로토콜 스택"),
         ("02", "두 구현 해부", "CopilotKit · Jev 라우터 · OpenUI Lang"),
         ("03", "비교와 선택", "포맷 · 한계 · 선택 기준")]
for i, (n, t, d) in enumerate(items):
    x = 0.9 + i * 4.0
    box(s, x, 2.0, 3.6, 3.4, "", fill=LIGHT, line=BLUE)
    txt(s, x + 0.3, 2.3, 3.0, 0.9, n, size=44, bold=True, color=ORANGE)
    txt(s, x + 0.3, 3.4, 3.0, 0.6, t, size=22, bold=True, color=NAVY)
    txt(s, x + 0.3, 4.2, 3.0, 0.9, d, size=14, color=GRAY)
record("아젠다", "세 개의 번호 카드 (01 02 03)", ["01 배경과 스펙트럼", "02 두 구현 해부", "03 비교와 선택"], notes)


def divider(num, title, sub, notes):
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid(); bg.fill.fore_color.rgb = LIGHT; bg.line.fill.background()
    txt(s, 0.9, 2.2, 3, 1.5, num, size=88, bold=True, color=ORANGE)
    txt(s, 0.9, 3.9, 11, 0.9, title, size=36, bold=True, color=NAVY)
    txt(s, 0.9, 4.8, 11, 0.6, sub, size=18, color=GRAY)
    s.notes_slide.notes_text_frame.text = notes
    record(f"섹션 {num}: {title}", "연한 파란 배경, 큰 번호", [title, sub], notes)


divider("01", "배경과 스펙트럼", "원본 · 이름 충돌 · 프로토콜 스택", "첫 번째 섹션입니다. 왜 오픈 재현이 나왔는지와 생성형 UI의 지도를 먼저 그리겠습니다.")

# ---------- 4. 원본 ----------
notes = ("OpenAI는 2026년 10월 7일 GPT-6와 함께 Intelligent UI를 공개했습니다. 구성은 네이티브 스트리밍 컴포넌트 라이브러리와, "
         "모델이 생성하는 동안 UI를 처리하는 컴파일러입니다. 다만 폐쇄형이고 외부에서 쓸 API가 확인되지 않아, 오픈 재현이 곧바로 등장했습니다. "
         "OpenAI 원문은 직접 열람하지 못해 검색 결과와 2차 보도를 근거로 했다는 점을 밝혀 둡니다.")
s = base("원본: ChatGPT Intelligent UI", "01 배경", notes)
box(s, 0.8, 1.9, 3.4, 1.6, ["네이티브 컴포넌트", "스트리밍 라이브러리"], fill=LIGHT, size=18, bold=True)
box(s, 4.95, 1.9, 3.4, 1.6, ["컴파일러", "생성 중 UI 처리"], fill=LIGHT, size=18, bold=True)
box(s, 9.1, 1.9, 3.4, 1.6, ["점진 렌더링", "차트 · 폼 · 도구"], fill=PALE_GR, line=GREEN, size=18, bold=True)
arrow(s, 4.2, 2.7, 4.95, 2.7)
arrow(s, 8.35, 2.7, 9.1, 2.7)
txt(s, 0.8, 3.75, 11.7, 0.4, "2026-10-07 · GPT-6와 함께 공개 · Chat 경험 한정", size=14, color=GRAY, align=PP_ALIGN.CENTER)
box(s, 0.8, 4.6, 11.7, 1.0, "폐쇄형 · 외부 API 미확인 · ChatGPT 안에서만 동작", fill=PALE_RD, line=RED, size=20, bold=True, color=RED)
arrow(s, 6.65, 5.6, 6.65, 6.2, color=ORANGE, w=3)
box(s, 3.2, 6.2, 6.9, 0.7, "오픈 재현 프로젝트 등장 (2026-10-08, 10-09)", fill=PALE_OR, line=ORANGE, size=16, bold=True, color=INK)
record("원본: ChatGPT Intelligent UI", "3단계 흐름(라이브러리 → 컴파일러 → 점진 렌더링)과 아래에 폐쇄형 경고 띠, 화살표로 오픈 재현 등장",
       ["네이티브 스트리밍 컴포넌트", "생성 중 UI 처리 컴파일러", "폐쇄형 · API 미확인"], notes)

# ---------- 5. 이름 충돌 ----------
notes = ("같은 이름을 쓰지만 서로 다른 두 저장소입니다. CopilotKit 쪽은 모델이 HTML과 CSS, JavaScript를 직접 스트리밍하고 격리 iframe에서 실행합니다. "
         "Thesys 쪽은 OpenUI Lang이라는 DSL을 스트리밍하고 컴포넌트 라이브러리로 렌더링합니다. 이후 비교에서는 각각 CK 구현, TS 구현이라 부르겠습니다.")
s = base("이름은 같고 설계는 다른 두 프로젝트", "01 배경", notes)
for i, (head, col, fill, rows) in enumerate([
    ("CopilotKit / OpenIntelligentUI", ORANGE, PALE_OR,
     ["모델 산출물: HTML · CSS · JS", "격리: iframe 샌드박스", "스택: Next.js + FastAPI", "라우터: Jev", "MIT"]),
    ("Thesys / open-intelligent-ui", GREEN, PALE_GR,
     ["모델 산출물: OpenUI Lang", "격리: 어휘 한정 (선언형)", "스택: Next.js 단일 앱", "라우터: 없음 (문서상)", "MIT"])]):
    x = 0.8 + i * 6.0
    box(s, x, 1.7, 5.6, 0.9, head, fill=col, line=col, size=20, bold=True, color=WHITE)
    box(s, x, 2.6, 5.6, 3.9, "", fill=fill, line=col)
    for j, r in enumerate(rows):
        txt(s, x + 0.35, 2.85 + j * 0.72, 5.0, 0.6, r, size=18, color=INK)
record("이름은 같고 설계는 다른 두 프로젝트", "좌우 두 카드: CK 구현(주황) vs TS 구현(초록), 산출물/격리/스택/라우터/라이선스 비교",
       ["CK: HTML·CSS·JS + iframe + Jev", "TS: OpenUI Lang + 선언형", "둘 다 MIT"], notes)

# ---------- 6. 스펙트럼 ----------
notes = ("CopilotKit의 분류에 따르면 생성형 UI는 에이전트가 쥐는 통제권의 스펙트럼입니다. 왼쪽 Controlled에서 오른쪽 Open으로 갈수록 표현력은 커지고 예측 가능성은 낮아집니다. "
         "아래 층은 전송 프로토콜입니다. AG-UI는 UI 명세가 아니라 이벤트 전송 프로토콜이며, A2UI와 MCP Apps 같은 명세가 그 위나 옆에 놓입니다. "
         "OpenUI Lang과 json-render를 Declarative에 놓은 것은 본 연구의 분류입니다.")
s = base("생성형 UI 스펙트럼과 프로토콜 스택", "01 배경", notes)
labels = [("Controlled", "등록 컴포넌트 선택", LIGHT, BLUE), ("Declarative", "A2UI · OpenUI Lang · json-render", LIGHT, BLUE),
          ("MCP Apps", "서드파티 iframe", LIGHT, BLUE), ("Open", "HTML/JS 샌드박스", PALE_OR, ORANGE)]
for i, (a, b, f, l) in enumerate(labels):
    x = 0.8 + i * 3.1
    box(s, x, 1.7, 2.8, 1.5, [a, b], fill=f, line=l, size=18, bold=True, color=NAVY)
    if i < 3:
        arrow(s, x + 2.8, 2.45, x + 3.1, 2.45)
txt(s, 0.8, 3.3, 12, 0.4, "통제 ◀──────────────────────────▶ 표현력", size=14, color=GRAY, align=PP_ALIGN.CENTER)
box(s, 0.8, 4.2, 5.7, 0.9, "A2UI · OpenUI Lang · json-render", fill=LIGHT, line=BLUE, size=15, bold=True)
box(s, 6.7, 4.2, 2.8, 0.9, "MCP Apps (ui://)", fill=LIGHT, line=BLUE, size=15, bold=True)
box(s, 9.7, 4.2, 2.8, 0.9, "원시 HTML/JS", fill=PALE_OR, line=ORANGE, size=15, bold=True)
box(s, 0.8, 5.5, 8.7, 0.8, "AG-UI · 에이전트 ↔ 앱 이벤트 전송 (UI 명세 아님)", fill=PALE_GR, line=GREEN, size=15, bold=True)
box(s, 9.7, 5.5, 2.8, 0.8, "MCP · 에이전트 ↔ 툴", fill=PALE_GR, line=GREEN, size=15, bold=True)
txt(s, 0.8, 6.4, 12, 0.4, "윗줄: 무엇을 그릴 것인가   /   아랫줄: 어떻게 나를 것인가", size=12, color=GRAY, align=PP_ALIGN.CENTER)
record("생성형 UI 스펙트럼과 프로토콜 스택", "상단: Controlled→Declarative→MCP Apps→Open 4단 화살표. 하단: 명세 층 위, 전송 층(AG-UI, MCP) 아래",
       ["통제 ↔ 표현력", "AG-UI는 전송 프로토콜", "A2UI · MCP Apps는 UI 기술"], notes)

divider("02", "두 구현 해부", "CopilotKit · Jev 라우터 · OpenUI Lang", "두 번째 섹션입니다. 먼저 CopilotKit 구현의 구조와 요청 흐름, 그리고 Jev의 역할을 보겠습니다. 이어서 Thesys 구현과 OpenUI Lang을 살펴봅니다.")

# ---------- 8. CK 아키텍처 ----------
notes = ("CK 구현은 Turborepo 모노레포입니다. 프런트엔드는 Next.js이고, /api/copilotkit 런타임이 LangGraphHttpAgent로 FastAPI의 Deep Agent에 연결됩니다. "
         "에이전트는 답변 모델 chat-latest와 라우터 Jev를 호출합니다. 선택적 MCP 서버는 assemble_document로 HTML을 텍스트로 반환할 뿐이고, 렌더링은 호스트의 몫입니다.")
s = base("구현 A: CopilotKit 아키텍처", "02 구현", notes)
box(s, 0.6, 1.6, 4.0, 4.6, "", fill=None, line=BLUE)
txt(s, 0.7, 1.65, 3.8, 0.4, "브라우저 · Next.js", size=13, bold=True, color=BLUE)
box(s, 0.9, 2.2, 3.4, 0.9, "CopilotKit 채팅", size=15)
box(s, 0.9, 3.35, 3.4, 1.1, ["activity 렌더러", "Idiomorph → Websandbox"], size=15, bold=True)
box(s, 0.9, 4.7, 3.4, 1.0, ["A2UI Table", "카탈로그"], size=15)
box(s, 5.2, 3.0, 2.3, 1.5, ["/api/copilotkit", "openGenerativeUI"], size=14, bold=True)
box(s, 8.0, 1.6, 2.4, 2.0, ["FastAPI :8123", "Deep Agent", "메모리 체크포인트"], size=14, bold=True)
box(s, 10.9, 1.6, 2.0, 0.95, ["Jev", "jev-latest"], fill=PALE_OR, line=ORANGE, size=15, bold=True)
box(s, 10.9, 2.75, 2.0, 0.95, ["chat-latest", "OpenAI"], fill=PALE_GR, line=GREEN, size=15, bold=True)
box(s, 8.0, 4.3, 2.4, 1.2, ["apps/mcp (선택)", "assemble_document"], fill=PALE_GR, line=GREEN, size=13)
arrow(s, 4.3, 2.65, 5.2, 3.5)
arrow(s, 7.5, 3.5, 8.0, 2.8)
arrow(s, 10.4, 2.05, 10.9, 2.05, color=ORANGE)
arrow(s, 10.4, 3.2, 10.9, 3.2, color=GREEN)
arrow(s, 5.2, 4.2, 4.3, 3.9, dashed=True)
txt(s, 0.6, 6.4, 12, 0.5, "Node 22+ · Python 3.12+ · uv · make setup → make dev", size=13, color=GRAY)
record("구현 A: CopilotKit 아키텍처", "좌: 브라우저 박스(채팅/활동 렌더러/A2UI 표), 중: /api/copilotkit, 우: FastAPI Deep Agent와 Jev·chat-latest, 하단 MCP",
       ["Next.js ↔ FastAPI (AG-UI 계열)", "Deep Agent + Jev + chat-latest", "체크포인트: 프로세스 메모리"], notes)

# ---------- 9. CK 요청 흐름 ----------
notes = ("요청 한 번의 흐름입니다. 사용자가 질문하면 Jev가 최근 메시지 최대 네 개를 보고 시각화 유형을 먼저 고릅니다. 그 선택에서 렌더러가 도출되고, 답변 모델에는 해당 렌더링 계약만 전달됩니다. "
         "모델은 generateSandboxedUi를 스트리밍하고, 미들웨어가 이를 activity 이벤트로 바꿔 프런트에 보냅니다. 사용자가 버튼을 누르면 sendPrompt로 새로운 턴이 시작됩니다.")
s = base("요청 한 번의 흐름", "02 구현", notes)
steps = [("1", "Jev 분류", "최근 메시지 ≤4개"), ("2", "렌더러 도출", "선택 → 렌더러"), ("3", "모델 생성", "계약만 전달"),
         ("4", "툴 호출 스트림", "generateSandboxedUi"), ("5", "점진 렌더링", "프리뷰 → 샌드박스"), ("6", "후속 질문", "sendPrompt → 새 턴")]
for i, (n, a, b) in enumerate(steps):
    col, row = i % 3, i // 3
    x, y = 0.8 + col * 4.1, 1.8 + row * 2.4
    fill, line = (PALE_OR, ORANGE) if i in (0, 1) else (LIGHT, BLUE)
    box(s, x, y, 3.7, 1.8, "", fill=fill, line=line)
    txt(s, x + 0.2, y + 0.1, 0.8, 0.8, n, size=32, bold=True, color=line)
    txt(s, x + 1.0, y + 0.25, 2.6, 0.5, a, size=18, bold=True, color=NAVY)
    txt(s, x + 1.0, y + 0.85, 2.6, 0.8, b, size=13, color=GRAY)
    if col < 2:
        arrow(s, x + 3.7, y + 0.9, x + 4.1, y + 0.9)
record("요청 한 번의 흐름", "6개 단계 카드(2행×3열), 화살표 연결: Jev 분류 → 렌더러 도출 → 모델 → 툴 스트림 → 렌더링 → 후속 질문",
       ["Jev가 모델보다 먼저", "툴 스트림 → activity 이벤트", "후속은 새 턴 (패치 API 없음)"], notes)

# ---------- 10. 파라미터 순서 ----------
notes = ("generateSandboxedUi의 인자 순서는 곧 사용자 경험 설계입니다. 높이와 플레이스홀더가 먼저 오고, CSS가 HTML보다 앞서야 스타일 없는 화면이 보이지 않습니다. "
         "표현식은 마지막에 도착해 동작이 하나씩 붙는 모습을 사용자가 지켜보게 됩니다. html이 스트리밍되는 동안에는 Idiomorph로 프리뷰 iframe을 깜빡임 없이 갱신합니다.")
s = base("스트리밍 순서가 곧 UX다", "02 구현", notes)
params = [("initialHeight", "자리 확보"), ("placeholder\nMessages", "대기 문구"), ("css", "스타일 먼저"),
          ("html", "morph 프리뷰"), ("jsFunctions", "함수 정의"), ("jsExpressions", "동작이 차례로")]
for i, (a, b) in enumerate(params):
    x = 0.55 + i * 2.1
    hot = i in (2, 5)
    box(s, x, 2.3, 1.95, 1.3, a.split("\n"), fill=PALE_OR if hot else LIGHT, line=ORANGE if hot else BLUE,
        size=14, bold=True, shape=MSO_SHAPE.CHEVRON if False else MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, x, 3.75, 1.95, 0.5, b, size=13, color=GRAY, align=PP_ALIGN.CENTER)
    if i < 5:
        arrow(s, x + 1.95, 2.95, x + 2.1, 2.95)
box(s, 0.8, 5.0, 11.7, 1.3, ["CSS가 먼저 → 스타일 없는 UI 노출 방지", "표현식이 마지막 → 동작이 하나씩 붙는 모습 노출"],
    fill=PALE_GR, line=GREEN, size=18, bold=True, color=INK)
record("스트리밍 순서가 곧 UX다", "6개 상자를 화살표로 연결: initialHeight → placeholderMessages → css → html → jsFunctions → jsExpressions. css와 jsExpressions 강조",
       ["CSS 먼저", "표현식 마지막", "html은 morph 프리뷰"], notes)

# ---------- 11. Jev ----------
notes = ("Jev는 TypeSafe의 System One 모델입니다. 새 사용자 메시지마다 타입이 있는 시각화 선택 하나를 만듭니다. 선택에서 렌더러가 도출되므로 모순된 조합이 생기지 않습니다. "
         "현재 선언형 경로는 기본 표뿐이고 나머지 시각화는 샌드박스 경로입니다. 인증 실패나 타임아웃은 턴 실패로 드러나며 조용한 폴백은 없습니다. Jev와 결정 모델 자체는 자매 글에서 자세히 다룹니다.")
s = base("Jev의 역할: 포맷을 먼저 고르는 라우터", "02 구현", notes)
box(s, 0.6, 2.6, 2.8, 1.6, ["새 메시지", "+ 최근 텍스트 ≤4개"], size=15, bold=True)
box(s, 4.2, 2.6, 2.4, 1.6, ["Jev", "선택지 분류"], fill=PALE_OR, line=ORANGE, size=20, bold=True)
arrow(s, 3.4, 3.4, 4.2, 3.4)
outs = [("text", "일반 채팅 답변", 1.6), ("table", "A2UI 표 (≤12열 · ≤200행)", 3.0), ("chart · diagram\ncalculator · map", "Open Generative UI", 4.4)]
for a, b, y in outs:
    box(s, 7.3, y - 0.45, 2.3, 0.9, a.split("\n"), size=13, bold=True)
    box(s, 10.2, y - 0.45, 2.7, 0.9, b, fill=PALE_GR, line=GREEN, size=13, bold=True)
    arrow(s, 6.6, 3.4, 7.3, y)
    arrow(s, 9.6, y, 10.2, y)
box(s, 0.6, 5.5, 12.3, 0.9, "실패는 턴 실패로 노출 · 조용한 폴백 없음 · 라우팅은 판단이지 보증이 아님", fill=PALE_RD, line=RED, size=16, bold=True, color=RED)
txt(s, 0.6, 6.65, 12, 0.35, "Jev 자체는 자매 글: jev-decision-models", size=12, color=GRAY)
record("Jev의 역할: 포맷을 먼저 고르는 라우터", "좌: 메시지 → Jev → 우: text/table/차트·다이어그램·계산기·지도 → 각 렌더러. 하단 경고 띠",
       ["턴마다 타입 있는 선택 1개", "선택에서 렌더러 도출", "실패 시 턴 실패"], notes)

# ---------- 12. TS 아키텍처 ----------
notes = ("TS 구현은 Next.js 단일 앱입니다. /api/chat이 컴포넌트 라이브러리에서 시스템 프롬프트를 만들어 세 가지 경로 중 하나로 보냅니다. "
         "OpenUI Gateway는 OpenUI Lang을 검증하고 자동 수정합니다. 직접 OpenAI 호환 엔드포인트나 Ollama를 쓰면 수정 단계가 없어 출력이 쓴 그대로 렌더링됩니다. "
         "스레드는 브라우저 localStorage에 저장됩니다.")
s = base("구현 B: Thesys 아키텍처", "02 구현", notes)
box(s, 0.6, 1.8, 3.8, 3.8, "", fill=None, line=BLUE)
txt(s, 0.7, 1.85, 3.6, 0.4, "브라우저", size=13, bold=True, color=BLUE)
box(s, 0.9, 2.4, 3.2, 1.3, ["OpenUI 렌더러", "라이브러리(Zod)"], size=15, bold=True)
box(s, 0.9, 3.95, 3.2, 1.3, ["$variables · @functions", "스레드 localStorage"], size=14)
box(s, 5.0, 3.1, 2.2, 1.2, ["/api/chat", "프롬프트 생성"], size=15, bold=True)
arrow(s, 4.4, 3.7, 5.0, 3.7)
box(s, 8.0, 1.8, 4.7, 1.2, ["OpenUI Gateway", "검증 + 자동 수정"], fill=PALE_GR, line=GREEN, size=16, bold=True)
box(s, 8.0, 3.2, 4.7, 1.0, ["OpenAI 호환 엔드포인트", "수정 단계 없음"], fill=PALE_OR, line=ORANGE, size=15, bold=True)
box(s, 8.0, 4.4, 4.7, 1.0, ["Ollama · LM Studio", "수정 단계 없음"], fill=PALE_OR, line=ORANGE, size=15, bold=True)
arrow(s, 7.2, 3.5, 8.0, 2.4)
arrow(s, 7.2, 3.7, 8.0, 3.7)
arrow(s, 7.2, 3.9, 8.0, 4.9)
txt(s, 0.6, 5.85, 12, 0.4, "서버 엔드포인트: /api/street-route (OSRM) · /api/wiki · /api/image-search", size=13, color=GRAY)
txt(s, 0.6, 6.3, 12, 0.4, "기본 모델 openai/gpt-6.1-sol · Node 24 · 채팅은 라이트 테마 전용", size=13, color=GRAY)
record("구현 B: Thesys 아키텍처", "좌: 브라우저(렌더러/상태), 중: /api/chat, 우: 3개 모델 경로(Gateway=검증, 직접·Ollama=수정 없음)",
       ["/api/chat → 3경로", "Gateway만 자동 수정", "스레드는 localStorage"], notes)

# ---------- 13. OpenUI Lang ----------
notes = ("OpenUI Lang의 핵심은 생성과 실행의 분리입니다. 모델은 배선을 한 번 생성하고, 런타임이 Query와 Mutation, 반응형 변수를 실행합니다. "
         "필터와 클릭은 모델 호출 없이 처리됩니다. 후속 요청에서는 바뀐 문장만 출력해 파서가 병합하며, 문서의 대략적 수치로 전체 약 400토큰 대 패치 약 60토큰입니다. "
         "토큰 절감 비율은 제작사 자체 측정이므로 재측정을 권합니다.")
s = base("OpenUI Lang: 생성은 한 번, 실행은 런타임", "02 구현", notes)
code = ['$title = ""', '$priority = "medium"', 'tickets = Query("list_tickets", {}, {rows: []})',
        'createResult = Mutation("create_ticket", {title: $title, priority: $priority})',
        'submitBtn = Button("Create", Action([@Run(createResult), @Run(tickets)]), "primary")']
cb = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.6), Inches(6.6), Inches(2.6))
cb.fill.solid(); cb.fill.fore_color.rgb = RGBColor(0x1E, 0x25, 0x2E); cb.line.fill.background(); cb.adjustments[0] = 0.05
txt(s, 0.8, 1.75, 6.3, 2.4, code, size=13, color=RGBColor(0xE6, 0xEE, 0xF7), font="Menlo")
box(s, 0.6, 4.5, 3.2, 1.3, ["생성 (LLM)", "프로그램 1회"], fill=PALE_OR, line=ORANGE, size=16, bold=True)
box(s, 4.0, 4.5, 3.2, 1.3, ["실행 (런타임)", "모델 호출 0회"], fill=PALE_GR, line=GREEN, size=16, bold=True)
txt(s, 7.6, 1.6, 5.2, 0.5, "증분 편집 (문서 기준 대략치)", size=16, bold=True, color=NAVY)
txt(s, 7.6, 2.3, 2.0, 0.4, "전체 20줄", size=13, color=GRAY)
bar1 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.6), Inches(2.7), Inches(5.0), Inches(0.5))
bar1.fill.solid(); bar1.fill.fore_color.rgb = BLUE; bar1.line.fill.background()
txt(s, 7.6, 2.72, 5.0, 0.46, "≈ 400 토큰", size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 7.6, 3.4, 2.0, 0.4, "패치 2~3줄", size=13, color=GRAY)
bar2 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.6), Inches(3.8), Inches(0.75), Inches(0.5))
bar2.fill.solid(); bar2.fill.fore_color.rgb = ORANGE; bar2.line.fill.background()
txt(s, 8.5, 3.82, 2.5, 0.46, "≈ 60 토큰", size=14, bold=True, color=ORANGE, anchor=MSO_ANCHOR.MIDDLE)
box(s, 7.6, 4.7, 5.0, 1.1, ["JSON 대비 합산 52% 적음 (제작사 측정)", "7개 시나리오: 4,800 vs 10,180"], fill=PALE_RD, line=RED, size=14, bold=True, color=RED)
txt(s, 0.6, 6.1, 12, 0.5, "$variables 변경 → 의존 쿼리 재실행 → 모델 없이 화면 갱신", size=15, bold=True, color=NAVY)
record("OpenUI Lang: 생성은 한 번, 실행은 런타임", "좌: OpenUI Lang 코드 4줄과 생성/실행 두 칸. 우: 400토큰 vs 60토큰 막대와 벤더 수치 경고",
       ["모델은 배선만 1회 생성", "클릭·필터는 모델 호출 없음", "증분 편집 ≈ 60토큰 (대략치)", "52% 절감은 제작사 측정"], notes)

divider("03", "비교와 선택", "포맷 · 한계 · 선택 기준", "마지막 섹션입니다. 두 구현을 비교하고, 포맷 간 트레이드오프와 한계, 선택 기준을 정리하겠습니다.")


# ---------- 표 도우미 ----------
def table(slide, x, y, w, h, data, col_w, size=12, head_fill=NAVY):
    rows, cols = len(data), len(data[0])
    gs = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gs.table
    tblPr = tbl._tbl.tblPr
    # 기본 스타일 줄무늬 제거
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(cw)
    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.07)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = head_fill
            else:
                cell.fill.fore_color.rgb = LIGHT if r % 2 == 1 else WHITE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER if (r == 0 or c == 0) and False else PP_ALIGN.LEFT
            run = p.add_run()
            run.text = data[r][c]
            run.font.name = FONT
            run.font.size = Pt(size)
            run.font.bold = (r == 0 or c == 0)
            run.font.color.rgb = WHITE if r == 0 else (NAVY if c == 0 else INK)
    return tbl


# ---------- 15. 두 구현 비교 ----------
notes = ("두 구현을 여덟 축으로 비교했습니다. CK 구현은 모델에게 화면을 통째로 맡기고 가두는 방식이고, TS 구현은 모델에게 화면을 기술하게 하고 런타임이 실행하는 방식입니다. "
         "그래서 보안의 중심이 전자는 격리, 후자는 어휘 한정입니다. 상태 측면에서는 CK의 체크포인트가 프로세스 메모리이고 TS는 브라우저 localStorage라는 점이 모두 운영상의 제약입니다.")
s = base("두 구현 비교", "03 비교", notes)
data = [["축", "CK 구현 (CopilotKit)", "TS 구현 (Thesys)"],
        ["렌더링 포맷", "HTML·CSS·JS + A2UI 표", "OpenUI Lang 1.0 (+HtmlView)"],
        ["검증", "iframe 격리 + Zod 브리지", "Gateway 검증·자동 수정"],
        ["답변 모델", "chat-latest (교체 가능)", "gpt-6.1-sol · OpenAI 호환 · Ollama"],
        ["라우터", "Jev (턴마다)", "문서상 없음"],
        ["상호작용", "iframe 내부 JS · sendPrompt=새 턴", "$variables · @functions · Query"],
        ["상태", "프로세스 메모리 체크포인트", "localStorage 스레드"],
        ["샌드박싱", "모든 Open 출력", "HtmlView만"],
        ["키", "서버 또는 BYOK 헤더", "서버 환경 변수"]]
table(s, 0.6, 1.5, 12.1, 5.2, data, [2.1, 5.0, 5.0], size=13)
record("두 구현 비교", "3열 표: 축 / CK 구현 / TS 구현 (포맷, 검증, 모델, 라우터, 상호작용, 상태, 샌드박싱, 키)",
       ["CK: 가두기(격리)", "TS: 어휘 한정", "상태는 둘 다 시연 수준"], notes)

# ---------- 16. 포맷 비교 ----------
notes = ("네 가지 포맷을 비교한 표입니다. 선언형 세 가지는 카탈로그에 있는 것만 말할 수 있다는 점에서 같고, 원시 HTML은 무엇이든 말할 수 있어 격리가 필수입니다. "
         "토큰 수치는 OpenUI 제작사의 자체 측정이며 경쟁 구현을 평가하는 비교표와 같은 문서에 있어 편향 가능성이 있습니다. 방향은 납득되지만 배율은 직접 재측정하시기 바랍니다.")
s = base("포맷 트레이드오프", "03 비교", notes)
data = [["", "OpenUI Lang", "A2UI", "json-render", "원시 HTML"],
        ["표현", "줄 지향 DSL", "ID 참조 평면 JSON", "root + elements JSON", "완결 프로그램"],
        ["토큰*", "1x (4,800)", "3x", "3x (10,180)", "4x"],
        ["안전 모델", "어휘 한정", "데이터, 코드 아님", "카탈로그·액션 한정", "임의 코드 → 격리"],
        ["디자인 일치", "높음", "높음", "높음", "낮음 (유도)"],
        ["모델 없는 상호작용", "$variables · Query", "클라이언트 함수", "선언된 액션", "내부 JS"],
        ["표현 한계", "라이브러리+HtmlView", "카탈로그", "카탈로그", "사실상 없음"]]
table(s, 0.6, 1.5, 12.1, 4.3, data, [2.5, 2.4, 2.4, 2.4, 2.4], size=13)
txt(s, 0.6, 6.0, 12.1, 0.6, "* OpenUI 제작사의 자체 측정 · 경쟁 구현 평가 포함. 배율은 직접 재측정 필요", size=13, bold=True, color=RED)
record("포맷 트레이드오프", "5열 표: 항목 / OpenUI Lang / A2UI / json-render / 원시 HTML. 하단에 벤더 수치 경고",
       ["선언형 3종 = 어휘 한정", "원시 HTML = 격리 필수", "토큰 수치는 제작사 측정"], notes)

# ---------- 17. 리스크 ----------
notes = ("한계는 여섯 가지로 정리됩니다. 첫째 그럴듯한 환각, 둘째 비용, 셋째 샌드박스 탈출 표면, 넷째 상태, 다섯째 라우팅과 가용성, 여섯째 검증 공백입니다. "
         "특히 sendPrompt는 생성된 코드가 에이전트에게 말을 거는 통로이므로 프롬프트 인젝션 관점의 검토가 필요하다고 판단합니다. 이는 본 연구의 분석이며 문서가 직접 위험으로 규정한 것은 아닙니다.")
s = base("한계와 리스크", "03 비교", notes)
risks = [("① 그럴듯한 환각", "숫자가 차트의 외형을 입음"), ("② 비용", "Open 경로 토큰 · 고정 프롬프트 ≈8,000"),
         ("③ 탈출 표면", "브리지 · CDN · sendPrompt"), ("④ 상태", "프로세스 메모리 · localStorage"),
         ("⑤ 라우팅 의존", "Jev 판단 오류 · 외부 가용성"), ("⑥ 검증 공백", "벤치마크·비용 수치 미공개")]
for i, (a, b) in enumerate(risks):
    col, row = i % 3, i // 3
    x, y = 0.8 + col * 4.1, 1.7 + row * 2.5
    box(s, x, y, 3.8, 2.2, "", fill=PALE_RD if i in (0, 2) else LIGHT, line=RED if i in (0, 2) else BLUE)
    txt(s, x + 0.25, y + 0.35, 3.3, 0.6, a, size=20, bold=True, color=NAVY)
    txt(s, x + 0.25, y + 1.15, 3.3, 0.9, b, size=14, color=GRAY)
record("한계와 리스크", "6개 카드(3×2): 환각 · 비용 · 탈출 표면 · 상태 · 라우팅 의존 · 검증 공백",
       ["그럴듯한 환각", "sendPrompt = 주입 통로(분석)", "벤치마크 미공개"], notes)

# ---------- 18. 선택 가이드 ----------
notes = ("선택 기준입니다. 고정된 브랜드 화면은 Controlled로, 정형 UI가 많고 모델 없이 계산과 재조회가 필요하면 OpenUI Lang, 여러 클라이언트가 필요하면 A2UI, React 중심이면 json-render가 후보입니다. "
         "3D나 게임 같은 자유 형식은 강한 격리를 전제로 한 샌드박스 HTML입니다. 가장 중요한 권고는 한 포맷으로 통일하지 말고 구간을 섞으라는 것입니다.")
s = base("무엇을 고를 것인가", "03 비교", notes)
box(s, 4.9, 1.5, 3.5, 0.9, "무엇을 만드는가", fill=NAVY, line=NAVY, size=18, bold=True, color=WHITE)
cases = [("고정 브랜드 화면", "Controlled", LIGHT, BLUE, 0.5), ("정형 UI + 모델 없는 계산·재조회", "OpenUI Lang", PALE_GR, GREEN, 3.6),
         ("멀티 클라이언트 (Flutter 등)", "A2UI", PALE_GR, GREEN, 6.7), ("자유 형식 (3D·게임)", "Open + 강한 격리", PALE_OR, ORANGE, 9.8)]
for a, b, f, l, x in cases:
    box(s, x, 3.0, 3.0, 1.2, a, fill=WHITE, line=GRAY, size=14, bold=True, color=INK)
    arrow(s, 6.65, 2.4, x + 1.5, 3.0, color=GRAY)
    arrow(s, x + 1.5, 4.2, x + 1.5, 4.9, color=l)
    box(s, x, 4.9, 3.0, 1.0, b, fill=f, line=l, size=16, bold=True)
txt(s, 0.5, 6.2, 12.3, 0.6, "React 중심 · Zod 카탈로그 → json-render   /   구간을 섞어 쓰는 것이 기본", size=14, color=GRAY, align=PP_ALIGN.CENTER)
record("무엇을 고를 것인가", "상단 '무엇을 만드는가' 에서 4갈래 분기: Controlled / OpenUI Lang / A2UI / Open+격리, 하단에 json-render 주석",
       ["정형 + 모델 없는 상호작용 → OpenUI Lang", "멀티 클라이언트 → A2UI", "자유 형식 → Open + 격리", "구간을 섞어라"], notes)

# ---------- 19. 결론 ----------
notes = ("정리하겠습니다. 첫째, 두 구현은 스펙트럼의 반대편에 있습니다. 둘째, 포맷은 곧 신뢰 경계이므로 격리와 어휘 검증 중 무엇이 보안의 중심인지 먼저 정해야 합니다. "
         "셋째, 두 프로젝트 모두 시연 수준의 상태 관리와 공개 벤치마크 부재라는 한계가 있습니다. Jev와 결정 모델은 자매 글에서 다룹니다. 질문 받겠습니다.")
s = base("결론 / Q&A", None, notes)
takeaways = [("1", "스펙트럼의 양 끝", "CK = Open(격리), TS = Declarative(어휘 한정)"),
             ("2", "포맷 = 신뢰 경계", "보안의 중심을 먼저 정하고 포맷을 고른다"),
             ("3", "시연 수준 레퍼런스", "상태·벤치마크·비용 수치 공백. 직접 측정 필요")]
for i, (n, a, b) in enumerate(takeaways):
    y = 1.6 + i * 1.5
    box(s, 0.8, y, 11.7, 1.25, "", fill=LIGHT, line=BLUE)
    txt(s, 1.0, y + 0.15, 0.9, 0.9, n, size=36, bold=True, color=ORANGE)
    txt(s, 2.0, y + 0.12, 10, 0.5, a, size=20, bold=True, color=NAVY)
    txt(s, 2.0, y + 0.65, 10, 0.5, b, size=15, color=GRAY)
box(s, 4.4, 6.2, 4.5, 0.7, "Q & A", fill=NAVY, line=NAVY, size=22, bold=True, color=WHITE)
record("결론 / Q&A", "3개 요약 카드와 하단 Q&A 버튼", ["스펙트럼의 양 끝", "포맷 = 신뢰 경계", "시연 수준 레퍼런스"], notes)

pptx_path = os.path.join(HERE, "open-intelligent-ui-presentation.pptx")
prs.save(pptx_path)
print("saved", pptx_path, "slides:", len(prs.slides))

# ---------- 아웃라인 마크다운 ----------
lines = ["> 📊 **발표자료(PPTX)**: [open-intelligent-ui-presentation.pptx](./open-intelligent-ui-presentation.pptx)",
         "",
         "# OpenIntelligentUI 서베이 — 발표 슬라이드 아웃라인",
         "",
         "본 문서는 [블로그](./open-intelligent-ui-blog.md)의 발표용 슬라이드 구성안이다. 슬라이드 본문은 최소한의 문구와 도식 중심이며, 상세는 스피커 노트에 둔다.",
         ""]
for i, (t, v, pts, nt) in enumerate(OUTLINE, 1):
    lines += [f"## Slide {i}: {t}", "", f"**Visual**: {v}", "", "**Key Points**:"]
    lines += [f"- {p}" for p in pts]
    lines += ["", f"**Speaker Notes**: {nt}", ""]
md_path = os.path.join(HERE, "open-intelligent-ui-presentation.md")
open(md_path, "w", encoding="utf-8").write("\n".join(lines))
print("saved", md_path)
