.PHONY: demo evaluate test api dashboard fine-tune sagemaker-dry-run

demo:
	python scripts/generate_demo_data.py
	python scripts/train_baseline.py

evaluate:
	python scripts/evaluate_baseline.py

test:
	python -m unittest discover -s tests -v

api:
	uvicorn triage.api:app --host 0.0.0.0 --port 8000

dashboard:
	streamlit run dashboard/app.py

fine-tune:
	python llm/fine_tune_lora.py --config configs/llm_config.json

sagemaker-dry-run:
	python aws/launch_training.py --dry-run
