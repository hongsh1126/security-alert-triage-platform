from __future__ import annotations

import argparse
import json
import os


def build_spec() -> dict:
    return {
        "entry_point": "llm/fine_tune_lora.py",
        "source_dir": ".",
        "instance_type": os.getenv("SM_TRAIN_INSTANCE", "ml.g5.2xlarge"),
        "instance_count": 1,
        "framework_version": "2.6.0",
        "py_version": "py312",
        "hyperparameters": {"config": "configs/llm_config.json"},
        "output_path": os.getenv("SM_OUTPUT_PATH", "s3://REPLACE-ME/security-triage/models"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    spec = build_spec()
    if args.dry_run:
        print(json.dumps(spec, indent=2))
        return
    if "REPLACE-ME" in spec["output_path"]:
        raise SystemExit("Set SM_OUTPUT_PATH to an S3 URI before launching training")
    import sagemaker
    from sagemaker.huggingface import HuggingFace
    estimator = HuggingFace(role=sagemaker.get_execution_role(), **spec)
    estimator.fit({"training": os.environ["SM_TRAIN_DATA"]})


if __name__ == "__main__":
    main()
