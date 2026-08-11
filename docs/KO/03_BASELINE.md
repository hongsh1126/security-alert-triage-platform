# 2단계: Baseline 모델 학습과 평가

## 목표

LLM이 실제로 가치가 있는지 비교할 기준선을 만듭니다. 복잡한 모델은 단순 모델보다 좋아야 합니다.

```bash
python scripts/generate_demo_data.py
python scripts/train_baseline.py
python scripts/evaluate_baseline.py
```

생성되는 `artifacts/baseline.joblib`은 TF-IDF와 Logistic Regression 기반 모델입니다. 평가는 accuracy뿐 아니라 precision, recall, F1과 confusion matrix를 출력합니다.

## 생각할 문제

- 공격 recall이 낮으면 어떤 사고를 놓칠 수 있는가?
- false positive가 많으면 분석가에게 어떤 문제가 생기는가?
- 클래스가 불균형할 때 accuracy가 왜 오해를 만드는가?

데모 데이터가 매우 작으므로 출력 숫자는 학습 기능 확인용일 뿐, 모델 품질의 증거가 아닙니다.

## 완료 기준

- [ ] 모델 파일이 생성된다.
- [ ] macro F1과 confusion matrix를 확인했다.
- [ ] LLM 결과와 비교할 baseline의 필요성을 설명할 수 있다.

