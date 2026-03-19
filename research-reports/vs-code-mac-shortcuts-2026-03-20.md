# VS Code macOS 단축키 종합 보고서

## 📋 목차
1. [기본 단축키](#기본-단축키)
2. [편집 단축키](#편집-단축키)
3. [네비게이션 단축키](#네비게이션-단축키)
4. [검색 & 바꾸기](#검색--바꾸기)
5. [디버깅](#디버깅)
6. [Git 관련 단축키](#git-관련-단축키)
7. [터미널](#터미널)
8. [선택 & 멀티커서](#선택--멀티커서)
9. [코드 접기](#코드-접기)
10. [커스터마이징](#커스터마이징)

---

## 기본 단축키

| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⇧⌘P` | 명령 팔레트 | 모든 명령에 접근 (F1 동일) |
| `⌘P` | 빠른 파일 열기 | 파일명 검색 후 열기 |
| `⌘K ⌘S` | 단축키 설정 | 키바인딩 편집기 열기 |
| `⌘,` | 설정 | 사용자 설정 열기 |
| `⌘K ⌘T` | 테마 변경 | 색상 테마 선택 |
| `⌘\` | 에디터 분할 | 현재 에디터를 옆에 분할 |
| `⌘1, ⌘2, ⌘3` | 에디터 그룹 전환 | 각 그룹으로 이동 |
| `⌘W` | 탭 닫기 | 현재 탭 종료 |
| `⌘B` | 사이드바 토글 | 탐색기 표시/숨김 |
| `⌘J` | 패널 토글 | 아래 패널(터미널, 출력 등) 표시/숨김 |
| `⌘K Z` | Zen 모드 | 집중 모드 진입 (Esc 2번으로 종료) |
| `⌃⌘↑` | 위로 줄 복사 | 현재 줄을 위로 복사 |
| `⌃⌘↓` | 아래로 줄 복사 | 현재 줄을 아래로 복사 |
| `⌘S` | 저장 | 파일 저장 |
| `⌘⇧S` | 다른 이름으로 저장 | 새 파일명으로 저장 |

---

## 편집 단축키

### 기본 편집
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌘X` | 잘라내기 | 선택된 텍스트 제거 및 클립보드에 복사 |
| `⌘C` | 복사 | 선택된 텍스트를 클립보드에 복사 |
| `⌘V` | 붙여넣기 | 클립보드 내용 붙여넣기 |
| `⌘⇧V` | 형식 제거하고 붙여넣기 | 평문으로 붙여넣기 |
| `⌘⇧K` | 줄 삭제 | 현재 줄 전체 삭제 |
| `⌘K ⌘X` | 뒷부분 공백 제거 | 줄의 끝 공백 제거 |
| `⌘/` | 주석 토글 | 선택된 코드를 주석 처리/해제 |
| `⌘↑` | 파일 시작으로 | 파일의 처음으로 이동 |
| `⌘↓` | 파일 끝으로 | 파일의 끝으로 이동 |

### 들여쓰기
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌘]` | 들여쓰기 증가 | 선택된 텍스트 들여쓰기 |
| `⌘[` | 들여쓰기 감소 | 선택된 텍스트 내어쓰기 |
| `⌘↵` (Enter) | 줄 삽입 | 새로운 줄 삽입 |

### 선택 및 이동
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌘L` | 줄 선택 | 현재 줄 전체 선택 |
| `⌘D` | 단어 선택 | 현재 단어 또는 다음 같은 단어 선택 |
| `⌘K ⌘D` | 선택 건너뛰기 | 다음 일치 건너뛰고 선택 |
| `⌘U` | 커서 실행 취소 | 마지막 커서 위치로 이동 |
| `⌥↑` | 줄 위로 이동 | 현재 줄을 위로 이동 |
| `⌥↓` | 줄 아래로 이동 | 현재 줄을 아래로 이동 |

### 포맷팅
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⇧⌥F` | 문서 포맷 | 전체 파일 포맷팅 |
| `⌘K ⌘F` | 선택 포맷 | 선택된 부분만 포맷팅 |
| `⌃Space` | IntelliSense | 자동완성 제안 표시 |

---

## 네비게이션 단축키

### 파일 및 기호 탐색
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌘P` | 파일 열기 | 파일명 검색으로 열기 |
| `⌘T` | 기호로 이동 (워크스페이스) | 전체 워크스페이스에서 기호 검색 |
| `⇧⌘O` | 기호로 이동 (파일) | 현재 파일에서 기호 검색 |
| `⌃G` | 줄로 이동 | 특정 줄 번호로 이동 |
| `⌘K ⌘G` | 다음 문제로 | 다음 오류/경고로 이동 |

### 정의 및 참조
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `F12` | 정의로 이동 | 함수/변수 정의 위치로 이동 |
| `⌘K F12` | 정의를 옆에 열기 | 옆 탭에서 정의 표시 |
| `⌥F12` | 정의 미리보기 | 팝업 창에서 정의 표시 |
| `⇧F12` | 모든 참조 찾기 | 기호가 사용되는 모든 위치 표시 |
| `⇧⌥F12` | 참조 뷰 열기 | 전용 참조 뷰 열기 |

### 탐색 이력
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌃-` | 뒤로 가기 | 이전 커서 위치로 이동 |
| `⌃⇧-` | 앞으로 가기 | 다음 커서 위치로 이동 |
| `⌃Tab` | 이력 탐색 | 열려있는 파일 이력 표시 |
| `⌃R` | 최근 폴더/워크스페이스 | 최근 열었던 프로젝트 열기 |

---

## 검색 & 바꾸기

| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌘F` | 찾기 | 현재 파일에서 검색 |
| `⌘H` | 찾기 및 바꾸기 | 검색 및 대체 기능 |
| `⇧Enter` | 이전 일치 | 검색 결과에서 이전 항목으로 |
| `Enter` | 다음 일치 | 검색 결과에서 다음 항목으로 |
| `⌘⇧F` | 파일에서 찾기 | 전체 워크스페이스 검색 |
| `⌘⇧H` | 파일에서 바꾸기 | 전체 워크스페이스 검색/바꾸기 |
| `⌥⌘L` | 선택 항목에서만 찾기 | 선택된 텍스트 내에서만 검색 |
| `⌘K ⌘W` | 모든 에디터 종료 | 모든 탭 닫기 |

### 고급 검색 옵션
- `Alt+C` - 대소문자 구분 토글
- `Alt+W` - 전체 단어 일치 토글
- `Alt+R` - 정규식 토글

---

## 디버깅

### 기본 디버깅
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `F5` | 시작/계속 | 디버깅 세션 시작 또는 계속 진행 |
| `⇧F5` | 중지 | 디버깅 세션 종료 |
| `⌘⇧F5` | 다시 시작 | 디버깅 세션 재시작 |
| `F6` | 일시 중지 | 실행 중단 |
| `F9` | 중단점 설정/해제 | 현재 줄에 중단점 토글 |
| `⇧F9` | 인라인 중단점 | 인라인 중단점 추가/제거 |

### 단계별 실행
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `F10` | 단계 실행 (Step Over) | 현재 줄 실행 후 다음 줄로 |
| `F11` | 단계 진입 (Step Into) | 함수 내부로 진입 |
| `⇧F11` | 단계 나가기 (Step Out) | 현재 함수에서 나가기 |

### 런 및 디버그 뷰
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⇧⌘D` | 런 및 디버그 뷰 | 디버깅 패널 열기 |
| `⌘K ⌘I` | 호버 정보 표시 | 변수/함수 정보 표시 |

⚠️ **Mac 사용자 주의**: Mac의 Function 키는 시스템 기능(밝기, 볼륨 등)으로 기본 설정되어 있습니다. F5를 사용하려면 `Fn+F5`를 눌러야 합니다. 이를 해결하려면:
- System Settings > Keyboard > Function keys에서 설정 변경
- 또는 단축키를 직접 커스터마이징

---

## Git 관련 단축키

### 기본 Git 작업
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌃⇧G` | 소스 제어 뷰 열기 | Git 패널 표시 |
| `⌘K ⌘C` | 클립보드와 비교 | 현재 파일을 클립보드 내용과 비교 |
| `⌘K ⌘D` | 저장된 파일과 비교 | 현재 파일과 마지막 저장 버전 비교 |

### 소스 제어 작업
- **변경 사항 확인**: 소스 제어 뷰에서 파일 선택
- **스테이징**: 파일 옆 `+` 버튼 클릭
- **언스테이징**: 파일 옆 `-` 버튼 클릭
- **커밋**: 메시지 입력 후 `Ctrl+Enter` (또는 커밋 버튼)
- **푸시**: 소스 제어 메뉴에서 "Push" 선택

### 고급 Git 작업
- **병합 충돌 해결**: 소스 제어 뷰에서 충돌 파일 열기 → 인라인 CodeLens로 선택
  - "Accept Current Change" - 현재 변경 수용
  - "Accept Incoming Change" - 들어오는 변경 수용
  - "Accept Both Changes" - 둘 다 수용
  - "Compare Changes" - 변경사항 비교

### Git 명령줄 설정
```bash
# VS Code를 기본 병합 도구로 설정
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# VS Code를 기본 Diff 도구로 설정
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'
```

---

## 터미널

| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌃\`` | 통합 터미널 표시/숨김 | 터미널 패널 토글 |
| `⌃⇧\`` | 새 터미널 | 새로운 터미널 인스턴스 생성 |
| `⌘C` | 복사 | 선택된 텍스트 복사 |
| `⌘V` | 붙여넣기 | 클립보드에서 붙여넣기 |

### 터미널 내 단축키
- Alt+click: 임의의 위치에 커서 추가
- Ctrl+D: 터미널 닫기
- Cmd+K: 터미널 삭제

---

## 선택 & 멀티커서

### 멀티커서 선택
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌘D` | 다음 일치 선택 | 현재 단어의 다음 일치 항목 선택 |
| `⌘K ⌘D` | 다음 일치 건너뛰기 | 일치 항목 선택 건너뛰기 |
| `⇧⌘L` | 모든 일치 선택 | 현재 선택과 일치하는 모든 항목 선택 |
| `⌥⌘↓` | 아래에 커서 추가 | 현재 아래에 새로운 커서 추가 |
| `⌥⌘↑` | 위에 커서 추가 | 현재 위에 새로운 커서 추가 |
| `⌥Click` | 위치에 커서 추가 | 클릭한 위치에 커서 추가 |

### 선택 확장/축소
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌃⇧⌘→` | 선택 확장 | 선택 범위를 오른쪽으로 확장 |
| `⌃⇧⌘←` | 선택 축소 | 선택 범위를 왼쪽으로 축소 |

### 칼럼(박스) 선택
- `Shift+Alt`를 누르고 드래그: 직사각형 선택
- 각 선택된 줄의 끝에 커서 추가

---

## 코드 접기

| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌥⌘[` | 접기 | 커서가 있는 영역 접기 |
| `⌥⌘]` | 펴기 | 접힌 영역 펴기 |
| `⌘K ⌘L` | 접기/펴기 토글 | 영역 토글 |
| `⌘K ⌘[` | 재귀 접기 | 영역 및 내부 모든 영역 접기 |
| `⌘K ⌘]` | 재귀 펴기 | 영역 및 내부 모든 영역 펴기 |
| `⌘K ⌘0` | 모두 접기 | 전체 파일의 모든 영역 접기 |
| `⌘K ⌘J` | 모두 펴기 | 전체 파일의 모든 영역 펴기 |
| `⌘K ⌘2` | 레벨 2 접기 | 2단계 깊이까지의 영역 접기 |

### 사용자 정의 폴딩
| 단축키 | 기능 | 설명 |
|--------|------|------|
| `⌘K ⌘,` | 선택에서 폴딩 범위 생성 | 선택된 텍스트를 접힘 범위로 변환 |
| `⌘K ⌘.` | 수동 폴딩 범위 제거 | 생성한 폴딩 범위 삭제 |

---

## 커스터마이징

### 단축키 커스터마이징

#### 열기
1. **메뉴**: File → Preferences → Keyboard Shortcuts
2. **단축키**: `⌘K ⌘S`
3. **검색**: 명령 검색 후 수정

#### 직접 편집
```bash
⌘K ⌘K  # Define Keybinding 실행 후 원하는 키 입력
```

#### keybindings.json 편집
```json
// 예: Ctrl+H를 테스트 실행에 바인딩
{
  "key": "ctrl+h",
  "command": "workbench.action.tasks.runTask",
  "args": "Run tests"
}

// 예: 기본 단축키 제거
{
  "key": "tab",
  "command": "-jumpToNextSnippetPlaceholder"
}
```

### 일반 커스터마이징 설정

```json
// 폰트 크기
"editor.fontSize": 14,

// 탭 크기
"editor.tabSize": 4,

// 스페이스 사용
"editor.insertSpaces": true,

// 저장 시 포맷팅
"editor.formatOnSave": true,

// 타이핑 시 포맷팅
"editor.formatOnType": true,

// 붙여넣기 시 포맷팅
"editor.formatOnPaste": true,

// 자동 저장
"files.autoSave": "afterDelay",
"files.autoSaveDelay": 1000,

// 단어 줄 바꿈
"editor.wordWrap": "on",

// 공백 표시
"editor.renderWhitespace": "all",

// 함수 서명 도움말 자동 표시
"editor.parameterHints.enabled": true,

// 자동완성 설정
"editor.quickSuggestions": {
  "other": true,
  "comments": false,
  "strings": false
}
```

### 언어별 설정

```json
// Python 설정
"[python]": {
  "editor.defaultFormatter": "ms-python.python",
  "editor.formatOnSave": true,
  "editor.tabSize": 4
},

// JavaScript 설정
"[javascript]": {
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.tabSize": 2
},

// Markdown 설정
"[markdown]": {
  "editor.wordWrap": "on",
  "editor.formatOnPaste": false
}
```

### Keymap 확장 (다른 에디터의 단축키 사용)

| 에디터 | 확장명 | 마켓플레이스 |
|--------|--------|-------------|
| Vim | Vim | ms-vscode.vim |
| Sublime Text | Sublime Text Keybindings | ms-vscode.sublime-keybindings |
| Emacs | Emacs Keymap | hiro-sun.vscode-emacs |
| Atom | Atom Keybindings | ms-vscode.atom-keybindings |
| Visual Studio | VS Keybindings | ms-vscode.vs-keybindings |

---

## 추가 팁 & 트릭

### IntelliSense 활용
```
⌃Space   # 자동완성 제안 표시
Tab/Enter # 제안 수용
⌃⇧Space  # 함수 매개변수 힌트 표시
```

### 빠른 찾기/바꾸기 팁
- **정규식 사용**: `Alt+R` 또는 `.*` 아이콘 클릭
- **대소문자 무시**: `Alt+C` 클릭
- **전체 단어만**: `Alt+W` 클릭
- **선택 내에서**: `Alt+L` 클릭

### 단어 변환
명령 팔레트에서 "Transform" 입력:
- Transform to Uppercase: 대문자로
- Transform to Lowercase: 소문자로
- Transform to Title Case: 제목 형식으로

### 파일 비교
```
⌘K C    # 클립보드와 비교
⌘K D    # 저장된 파일과 비교
```

### Word Wrap 토글
- **단축키**: `⌥Z`
- **설정**: `"editor.wordWrap": "on"`

### 상태 표시줄
오른쪽 하단 상태 표시줄에서:
- 줄:열 위치 클릭 → 특정 줄로 이동
- 들여쓰기 설정 클릭 → 탭/스페이스 전환
- 언어 모드 클릭 → 파일 형식 변경

---

## 자주 사용하는 단축키 TOP 10

1. **⌘P** - 파일 빠르게 열기 (가장 유용!)
2. **⇧⌘P** - 명령 실행
3. **⌘F** - 현재 파일에서 찾기
4. **⌘H** - 찾기 및 바꾸기
5. **F12** - 정의로 이동
6. **⌃⇧G** - Git 소스 제어
7. **⌃\`` - 통합 터미널
8. **⌥↑/↓** - 줄 이동
9. **⌘D** - 다음 일치 선택
10. **⇧⌥F** - 전체 문서 포맷팅

---

## 고급 활용

### 작업(Tasks) 정의
`Ctrl+Shift+P` → "Configure Tasks" → 작업.json 편집

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Python",
      "type": "shell",
      "command": "python",
      "args": ["${file}"],
      "group": {
        "kind": "test",
        "isDefault": true
      }
    }
  ]
}
```

작업 실행: `Ctrl+Shift+B` (기본값) 또는 `Ctrl+Shift+P` → "Run Task"

### 스니펫 생성
File → Preferences → Configure Snippets → 언어 선택

```json
{
  "Create Component": {
    "prefix": "comp",
    "body": [
      "function ${1:ComponentName}() {",
      "  return (",
      "    <div>${2:content}</div>",
      "  );",
      "}",
      "",
      "export default ${1:ComponentName};"
    ],
    "description": "React Component Template"
  }
}
```

### 원격 개발
VS Code Remote Extensions 사용:
- Remote - SSH
- Remote - Containers
- Remote - WSL

---

## 문제 해결

### F 키가 작동하지 않을 때
- **원인**: Mac의 시스템 단축키 우선순위
- **해결**: 
  1. System Preferences → Keyboard → Function Keys
  2. "Use F1, F2, etc. as standard function keys" 체크
  3. 또는 `Fn + F키` 사용

### 단축키 충돌 확인
`⌘K ⇧K` → "Show Same Keybindings" → 충돌하는 바인딩 확인

### 단축키 문제 디버깅
1. `Ctrl+Shift+P` → "Developer: Toggle Keyboard Shortcuts Troubleshooting"
2. 단축키 입력 후 출력 창에서 로그 확인
3. 인식되는 키 조합과 실행되는 명령 확인

---

## 참고 자료

- **공식 VS Code 단축키 PDF**: 
  - macOS: https://go.microsoft.com/fwlink/?linkid=832143
  
- **공식 문서**:
  - Keybindings: https://code.visualstudio.com/docs/configure/keybindings
  - Tips & Tricks: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
  - Basic Editing: https://code.visualstudio.com/docs/editor/codebasics

- **설정 파일 위치**:
  - `~/Library/Application Support/Code/User/keybindings.json`
  - `~/Library/Application Support/Code/User/settings.json`

---

## 요약

VS Code의 단축키 마스터는 개발 효율성을 크게 향상시킵니다. 가장 자주 사용하는 단축키부터 시작해서 점진적으로 확장하는 것을 추천합니다. 필요한 단축키는 `⌘K ⌘S`로 언제든 커스터마이징할 수 있으며, 다른 에디터에서 왔다면 Keymap 확장으로 익숙한 단축키를 사용할 수 있습니다.

**핵심**: 마우스를 적게 사용할수록 더 빠르고 효율적으로 코딩할 수 있습니다! 🚀

---

*Last Updated: 2026-03-20*
*VS Code Version: Latest*
