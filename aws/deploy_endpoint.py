from __future__ import annotations

import argparse
import os


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-data", required=True, help="S3 URI of model.tar.gz")
    parser.add_argument("--endpoint-name", default="security-alert-triage")
    parser.add_argument("--delete", action="store_true", help="Delete endpoint to stop charges")
    args = parser.parse_args()
    import boto3
    if args.delete:
        boto3.client("sagemaker").delete_endpoint(EndpointName=args.endpoint_name)
        print(f"Deletion requested for {args.endpoint_name}")
        return
    import sagemaker
    from sagemaker.huggingface import HuggingFaceModel
    model = HuggingFaceModel(model_data=args.model_data, role=sagemaker.get_execution_role(),
                             transformers_version="4.49", pytorch_version="2.6", py_version="py312")
    predictor = model.deploy(initial_instance_count=1, instance_type=os.getenv("SM_ENDPOINT_INSTANCE", "ml.g5.xlarge"),
                             endpoint_name=args.endpoint_name)
    print(f"Deployed endpoint: {predictor.endpoint_name}")


if __name__ == "__main__":
    main()

