"""
도구(Tools) 정의 모듈
====================
LangGraph 에이전트가 사용할 도구들을 정의합니다.

포함된 도구:
1. 웹 검색 (Tavily)
2. 날씨 조회 (OpenWeatherMap)
3. 계산기 (Python eval)
4. 코드 실행 (Python)
5. 텍스트 요약
6. 날짜/시간 조회

각 도구는 LangChain의 @tool 데코레이터를 사용하여 정의됩니다.
"""

import os
import math
import json
import datetime
import subprocess
import tempfile
from typing import Optional
from dotenv import load_dotenv

from langchain_core.tools import tool

load_dotenv()

# -------------------------------------------------------
# 1. 웹 검색 도구 (Tavily)
# -------------------------------------------------------
@tool
def web_search(query: str) -> str:
    """
    인터넷에서 최신 정보를 검색합니다.
    최신 뉴스, 사실 확인, 실시간 정보가 필요할 때 사용하세요.

    Args:
        query: 검색할 쿼리 문자열 (한국어 또는 영어)

    Returns:
        검색 결과 요약 텍스트
    """
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not tavily_api_key or tavily_api_key.startswith("tvly-your"):
        # API 키 없으면 더미 결과 반환 (데모용)
        return (
            f"[웹 검색 시뮬레이션]\n"
            f"검색어: '{query}'\n"
            f"TAVILY_API_KEY가 설정되지 않아 실제 검색을 수행할 수 없습니다.\n"
            f".env 파일에 TAVILY_API_KEY를 설정하면 실제 검색이 가능합니다.\n"
            f"Tavily API는 https://tavily.com/ 에서 무료로 발급받을 수 있습니다."
        )

    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=tavily_api_key)
        response = client.search(
            query=query,
            max_results=5,
            search_depth="basic"
        )

        results = []
        for r in response.get("results", []):
            results.append(
                f"제목: {r.get('title', 'N/A')}\n"
                f"URL: {r.get('url', 'N/A')}\n"
                f"내용: {r.get('content', 'N/A')[:300]}..."
            )

        return f"검색 결과 ({len(results)}개):\n\n" + "\n\n---\n\n".join(results)

    except Exception as e:
        return f"검색 오류: {str(e)}"


# -------------------------------------------------------
# 2. 날씨 조회 도구 (OpenWeatherMap)
# -------------------------------------------------------
@tool
def get_weather(city: str) -> str:
    """
    특정 도시의 현재 날씨 정보를 가져옵니다.
    날씨, 기온, 습도, 풍속 등의 정보를 제공합니다.

    Args:
        city: 도시 이름 (예: Seoul, Tokyo, New York)

    Returns:
        날씨 정보 문자열
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key or api_key.startswith("your-openweather"):
        # API 키 없으면 더미 결과 반환 (데모용)
        import random
        temp = random.randint(5, 30)
        conditions = ["맑음", "구름 조금", "흐림", "비", "눈"]
        condition = random.choice(conditions)
        return (
            f"[날씨 시뮬레이션 - {city}]\n"
            f"현재 날씨: {condition}\n"
            f"기온: {temp}°C\n"
            f"습도: {random.randint(40, 80)}%\n"
            f"풍속: {random.uniform(1, 10):.1f} m/s\n\n"
            f"(OPENWEATHER_API_KEY 설정 시 실제 데이터를 사용합니다)"
        )

    try:
        import requests
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "lang": "kr"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            country = data["sys"]["country"]

            return (
                f"{city}, {country} 현재 날씨:\n"
                f"날씨: {weather}\n"
                f"기온: {temp:.1f}°C (체감: {feels_like:.1f}°C)\n"
                f"습도: {humidity}%\n"
                f"풍속: {wind_speed} m/s"
            )
        else:
            return f"날씨 조회 실패: {data.get('message', '알 수 없는 오류')}"

    except Exception as e:
        return f"날씨 조회 오류: {str(e)}"


# -------------------------------------------------------
# 3. 고급 계산기 도구
# -------------------------------------------------------
@tool
def calculate(expression: str) -> str:
    """
    수학 계산을 수행합니다.
    사칙연산, 제곱근, 삼각함수 등 다양한 수학 연산을 지원합니다.

    Args:
        expression: 계산할 수식 (예: "2 + 3 * 4", "sqrt(16)", "sin(pi/2)")

    Returns:
        계산 결과 문자열
    """
    # 안전한 수학 함수만 허용
    allowed_names = {
        name: getattr(math, name)
        for name in dir(math)
        if not name.startswith("_")
    }
    allowed_names.update({
        "abs": abs,
        "round": round,
        "int": int,
        "float": float,
        "pow": pow,
        "sum": sum,
        "min": min,
        "max": max,
    })

    try:
        # eval 사용 시 보안을 위해 허용된 이름만 사용
        result = eval(
            expression,
            {"__builtins__": {}},  # 내장 함수 비활성화
            allowed_names
        )
        return f"계산 결과: {expression} = {result}"
    except ZeroDivisionError:
        return "오류: 0으로 나눌 수 없습니다"
    except Exception as e:
        return f"계산 오류: {str(e)}\n유효한 수식을 입력하세요 (예: 2+3, sqrt(16))"


# -------------------------------------------------------
# 4. Python 코드 실행 도구
# -------------------------------------------------------
@tool
def execute_python_code(code: str) -> str:
    """
    Python 코드를 안전하게 실행합니다.
    데이터 처리, 알고리즘 구현, 간단한 스크립트 실행에 사용합니다.
    주의: 파일 시스템 접근이나 네트워크 호출은 제한됩니다.

    Args:
        code: 실행할 Python 코드 문자열

    Returns:
        코드 실행 결과 (출력 또는 오류 메시지)
    """
    # 보안을 위한 기본적인 위험 패턴 체크
    dangerous_patterns = [
        "import os", "import sys", "import subprocess",
        "open(", "exec(", "__import__",
        "eval(", "compile(", "globals()", "locals()"
    ]

    for pattern in dangerous_patterns:
        if pattern in code:
            return f"보안상 '{pattern}' 사용이 제한됩니다. 순수 Python 계산 코드만 실행 가능합니다."

    try:
        # 임시 파일에 코드 작성 후 실행
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=10  # 10초 타임아웃
        )

        os.unlink(temp_file)  # 임시 파일 삭제

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:
            return f"실행 결과:\n```\n{output}\n```" if output else "코드가 성공적으로 실행되었습니다 (출력 없음)"
        else:
            return f"실행 오류:\n```\n{error}\n```"

    except subprocess.TimeoutExpired:
        return "오류: 코드 실행 시간이 초과되었습니다 (10초 제한)"
    except Exception as e:
        return f"코드 실행 오류: {str(e)}"


# -------------------------------------------------------
# 5. 날짜/시간 조회 도구
# -------------------------------------------------------
@tool
def get_current_datetime(timezone: Optional[str] = None) -> str:
    """
    현재 날짜와 시간을 반환합니다.

    Args:
        timezone: 타임존 이름 (예: "Asia/Seoul", "UTC", "America/New_York")
                  None이면 로컬 시간 반환

    Returns:
        현재 날짜/시간 문자열
    """
    try:
        now = datetime.datetime.now()

        if timezone:
            try:
                import zoneinfo
                tz = zoneinfo.ZoneInfo(timezone)
                now = datetime.datetime.now(tz)
            except Exception:
                pass

        weekdays = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        weekday = weekdays[now.weekday()]

        return (
            f"현재 날짜/시간:\n"
            f"날짜: {now.year}년 {now.month}월 {now.day}일 ({weekday})\n"
            f"시간: {now.strftime('%H:%M:%S')}\n"
            f"타임존: {timezone or '로컬 시간'}"
        )
    except Exception as e:
        return f"시간 조회 오류: {str(e)}"


# -------------------------------------------------------
# 6. 단위 변환 도구
# -------------------------------------------------------
@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """
    다양한 단위를 변환합니다.
    길이, 무게, 온도, 면적 등의 단위 변환을 지원합니다.

    Args:
        value: 변환할 값 (숫자)
        from_unit: 원본 단위 (예: km, kg, celsius, m2)
        to_unit: 변환 대상 단위 (예: mile, lb, fahrenheit, feet2)

    Returns:
        변환 결과 문자열
    """
    conversions = {
        # 길이
        ("km", "mile"): lambda x: x * 0.621371,
        ("mile", "km"): lambda x: x * 1.60934,
        ("m", "feet"): lambda x: x * 3.28084,
        ("feet", "m"): lambda x: x / 3.28084,
        ("cm", "inch"): lambda x: x * 0.393701,
        ("inch", "cm"): lambda x: x * 2.54,

        # 무게
        ("kg", "lb"): lambda x: x * 2.20462,
        ("lb", "kg"): lambda x: x / 2.20462,
        ("g", "oz"): lambda x: x * 0.035274,
        ("oz", "g"): lambda x: x / 0.035274,

        # 온도
        ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("celsius", "kelvin"): lambda x: x + 273.15,
        ("kelvin", "celsius"): lambda x: x - 273.15,

        # 속도
        ("kmh", "mph"): lambda x: x * 0.621371,
        ("mph", "kmh"): lambda x: x * 1.60934,
        ("ms", "kmh"): lambda x: x * 3.6,
        ("kmh", "ms"): lambda x: x / 3.6,
    }

    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"변환 결과: {value} {from_unit} = {result:.4f} {to_unit}"
    else:
        supported = [f"{f} → {t}" for f, t in conversions.keys()]
        return (
            f"지원하지 않는 단위 변환입니다: {from_unit} → {to_unit}\n"
            f"지원 변환: {', '.join(supported)}"
        )


# 모든 도구 목록 (에이전트에 제공)
ALL_TOOLS = [
    web_search,
    get_weather,
    calculate,
    execute_python_code,
    get_current_datetime,
    convert_units,
]

# 도구 설명 맵 (UI 표시용)
TOOL_DESCRIPTIONS = {
    "web_search": "인터넷 검색",
    "get_weather": "날씨 조회",
    "calculate": "수학 계산",
    "execute_python_code": "Python 코드 실행",
    "get_current_datetime": "날짜/시간 조회",
    "convert_units": "단위 변환",
}
