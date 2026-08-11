# 0단계: 환경 준비

## 1. 저장소 내려받기

```bash
git clone https://github.com/hongsh1126/security-alert-triage-platform.git
cd security-alert-triage-platform
```

## 2. 가상환경 만들기

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. 설치 확인

```bash
python --version
python -m unittest discover -s tests -v
```

예상 결과는 `OK`이며 테스트 3개 이상이 통과해야 합니다.

## 자주 발생하는 오류

- PowerShell 실행정책 오류: 관리자 권한이 아닌 현재 창에서 `Set-ExecutionPolicy -Scope Process Bypass`를 실행합니다.
- `python`을 찾지 못함: Windows에서는 `py`를 사용합니다.
- 패키지 충돌: `.venv`를 새로 만들고 다시 설치합니다.

## 완료 기준

- [ ] 가상환경 이름 `(.venv)`가 터미널에 표시된다.
- [ ] 테스트가 모두 통과한다.
- [ ] 비밀번호나 API 키를 저장소에 넣지 않았다.

