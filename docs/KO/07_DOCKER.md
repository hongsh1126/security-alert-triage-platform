# 6단계: Docker deployment

## 목표

개발 PC의 Python 환경과 무관하게 동일한 서비스를 재현합니다.

Docker Desktop을 실행한 뒤:

```bash
docker compose up --build
```

확인 주소:

- API 문서: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8501`

상태 확인:

```bash
docker compose ps
docker compose logs api
```

종료:

```bash
docker compose down
```

## Production과의 차이

이 데모에 다음을 추가해야 실제 production에 가까워집니다.

- 인증·권한과 TLS
- AWS Secrets Manager 같은 비밀 관리
- rate limiting
- 중앙집중식 로그와 alert
- managed database와 backup
- model/data drift monitoring
- container vulnerability scan

## 완료 기준

- [ ] 두 container가 정상 상태다.
- [ ] 로컬 Python 가상환경을 끄고도 API가 동작한다.
- [ ] `docker compose down`으로 자원을 정리했다.

