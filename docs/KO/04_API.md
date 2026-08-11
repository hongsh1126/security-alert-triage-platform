# 3단계: FastAPI 서비스

## 목표

노트북 속 모델을 다른 프로그램이 호출할 수 있는 서비스로 바꿉니다.

터미널 1:

```bash
uvicorn triage.api:app --reload
```

브라우저에서 `http://localhost:8000/docs`를 열고 다음을 실행합니다.

1. `GET /health`
2. `POST /v1/triage`
3. 아래 JSON을 Request body에 입력

```json
{
  "alert_id": "lab-001",
  "title": "SSH anomaly",
  "description": "Repeated failures followed by a root login",
  "source": "SIEM"
}
```

터미널에서도 확인할 수 있습니다.

```bash
curl http://localhost:8000/health
```

## 코드 읽기

- `triage/api.py`: URL, 입력 schema, HTTP 오류
- `triage/service.py`: 모델과 feedback 저장소 연결
- `triage/model.py`: GPU 없이 실행되는 fallback 판단
- `tests/test_core.py`: 자동 회귀 테스트

## 완료 기준

- [ ] `/health`가 healthy를 반환한다.
- [ ] `/v1/triage`가 severity와 action을 반환한다.
- [ ] description을 바꾸면 결과가 달라지는지 확인했다.

