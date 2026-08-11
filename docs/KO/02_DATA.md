# 1단계: 보안 경보 데이터

## 목표

LLM fine-tuning 전에 입력과 정답 형식을 이해하고 데이터 누출을 피합니다.

## 실습

```bash
python scripts/generate_demo_data.py
python llm/fine_tune_lora.py --validate-only
```

`data/train.jsonl`의 한 줄은 다음 세 필드를 가집니다.

```json
{"instruction":"Classify the alert...","input":"Repeated failed SSH...","output":"{\"severity\":\"HIGH\"...}"}
```

- `instruction`: 모델이 수행할 과제
- `input`: SIEM/EDR 경보 내용
- `output`: 분석가가 만든 정답

## 직접 변경해 보기

`data/train.jsonl`에 가상의 LOW 또는 MEDIUM 경보 한 건을 추가하고 다시 검증합니다. 한 줄에 JSON 객체 하나만 작성해야 합니다.

## 보안·연구 원칙

- train/test에 같은 사건이나 거의 같은 문장을 동시에 넣지 않습니다.
- 실제 IP, 사용자명, token, 회사 로그를 공개 저장소에 넣지 않습니다.
- synthetic 6건의 성능을 논문 또는 résumé의 성능으로 주장하지 않습니다.
- 실제 연구에서는 데이터 라이선스와 class imbalance를 기록합니다.

## 완료 기준

- [ ] 검증 메시지에 레코드 수가 출력된다.
- [ ] 새 레코드를 추가해도 JSON 오류가 없다.
- [ ] instruction, input, output의 역할을 설명할 수 있다.

