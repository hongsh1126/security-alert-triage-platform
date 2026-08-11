# 5단계: LoRA/QLoRA fine-tuning

## 개념

- Full fine-tuning: 원래 모델의 대부분 또는 전체 파라미터를 수정합니다.
- LoRA: 작은 저랭크 adapter만 학습해 메모리와 저장공간을 줄입니다.
- QLoRA: base model을 4-bit로 양자화하고 LoRA adapter를 학습합니다.

설정 파일 `configs/llm_config.json`에서 `use_4bit`가 `true`이면 QLoRA 경로입니다.

## 먼저 CPU에서 데이터만 검증

```bash
pip install -r requirements-llm.txt
python llm/fine_tune_lora.py --validate-only
```

## GPU에서 학습

NVIDIA GPU가 있는 Linux 또는 Google Colab에서 실행하는 것을 권장합니다.

```bash
nvidia-smi
python llm/fine_tune_lora.py --config configs/llm_config.json
```

완료되면 `artifacts/lora_adapter/`에 adapter와 tokenizer가 저장됩니다. 이 폴더는 용량 때문에 GitHub에 올리지 않도록 설정되어 있습니다.

## 반드시 비교할 항목

1. base model과 fine-tuned model에 동일한 test alert 사용
2. JSON 형식 준수율
3. severity macro F1
4. 위험 경보 recall
5. latency와 GPU memory
6. 사람이 평가한 근거·조치의 유용성

## 오류 해결

- CUDA out of memory: batch size 또는 max length를 줄이고 gradient accumulation을 늘립니다.
- bitsandbytes 오류: CUDA가 있는 Linux/Colab인지 확인합니다.
- gated model 오류: Hugging Face 사용 승인을 받고 로그인합니다.
- 학습은 되지만 출력이 이상함: 데이터 형식, EOS token, class balance를 확인합니다.

## 완료 기준

- [ ] LoRA와 QLoRA 차이를 설명할 수 있다.
- [ ] trainable parameter가 전체보다 훨씬 적음을 확인했다.
- [ ] adapter 폴더가 생성되었다.
- [ ] base와 fine-tuned 결과를 같은 test set으로 비교했다.

