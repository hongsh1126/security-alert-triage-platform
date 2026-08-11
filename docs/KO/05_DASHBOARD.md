# 4단계: Analyst feedback dashboard

## 목표

AI 판단을 사람이 승인·거부·수정하고 그 결과를 다음 학습에 사용할 수 있게 합니다.

터미널 1에서 API를 실행합니다.

```bash
uvicorn triage.api:app --reload
```

터미널 2에서 dashboard를 실행합니다.

```bash
streamlit run dashboard/app.py
```

`http://localhost:8501`에서 다음을 수행합니다.

1. 경보 내용을 입력하고 `Run triage`
2. `approve`, `reject`, `correct` 중 선택
3. 수정이라면 올바른 severity와 note 입력
4. `Submit feedback`
5. `Refresh feedback metrics`

feedback은 `data/feedback.db` SQLite 파일에 저장되며 GitHub에는 올라가지 않습니다.

## 실무 확장 과제

- 분석가 ID와 검토 시간을 기록하기
- 최근 검토 목록을 표로 표시하기
- corrected label을 JSONL로 export하기
- 일정 수의 검토가 모이면 재학습을 요청하기

## 완료 기준

- [ ] approve 1건과 correct 1건을 저장했다.
- [ ] analyst agreement 값이 바뀌었다.
- [ ] feedback loop가 모델 개선에 어떻게 쓰이는지 설명할 수 있다.

