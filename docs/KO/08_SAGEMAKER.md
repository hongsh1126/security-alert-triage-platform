# 7단계: AWS SageMaker

## 비용 경고

GPU training instance와 endpoint는 비용이 발생합니다. 먼저 dry-run만 실행하고, 실습이 끝나면 endpoint를 삭제하세요. AWS Console의 Billing/Budgets에서 예산 경보를 먼저 설정하는 것이 안전합니다.

## 1. 비용 없는 dry-run

```bash
pip install -r requirements-aws.txt
python aws/launch_training.py --dry-run
```

출력에서 instance type, entry point, output S3 path를 확인합니다.

## 2. AWS 준비

- SageMaker execution role
- 개인 S3 bucket
- 로컬 AWS credentials 또는 SageMaker Studio
- 학습 데이터 업로드

예시 환경변수는 실제 bucket으로 바꿉니다.

```bash
export SM_TRAIN_DATA=s3://YOUR-BUCKET/security-triage/data
export SM_OUTPUT_PATH=s3://YOUR-BUCKET/security-triage/models
export SM_TRAIN_INSTANCE=ml.g5.2xlarge
python aws/launch_training.py
```

Windows PowerShell에서는 `$env:SM_TRAIN_DATA="s3://..."` 형식을 사용합니다.

## 3. Endpoint 배포

학습 작업이 만든 정확한 `model.tar.gz` S3 URI를 사용합니다.

```bash
python aws/deploy_endpoint.py --model-data s3://YOUR-BUCKET/path/model.tar.gz --endpoint-name security-alert-triage-lab
```

## 4. 반드시 삭제

```bash
python aws/deploy_endpoint.py --model-data s3://unused --endpoint-name security-alert-triage-lab --delete
```

AWS Console에서도 endpoint 상태가 사라졌는지 확인합니다. S3 artifact와 CloudWatch log에는 별도 저장비가 있을 수 있습니다.

## résumé에 정직하게 기록하기

실제로 training job과 endpoint를 실행한 뒤에만 `deployed on SageMaker`라고 씁니다. dry-run만 했다면 `implemented SageMaker deployment scripts and validated configuration with dry-run`이라고 씁니다.

## 완료 기준

- [ ] dry-run spec을 읽고 각 항목을 설명할 수 있다.
- [ ] 실제 실행 시 job status와 log를 확인했다.
- [ ] endpoint 호출을 테스트했다.
- [ ] endpoint를 삭제하고 비용 발생이 중단됐는지 확인했다.

