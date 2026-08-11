"""LoRA/QLoRA supervised fine-tuning for structured alert triage.

Install requirements-llm.txt and use a CUDA GPU for the default 4-bit path.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def format_example(example: dict) -> str:
    return ("<|user|>\n" + example["instruction"] + "\nAlert: " + example["input"] +
            "\n<|assistant|>\n" + example["output"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/llm_config.json")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    cfg_path = Path(args.config)
    cfg = json.loads(cfg_path.read_text())
    train_file = Path(os.getenv("SM_CHANNEL_TRAIN", cfg["train_file"]))
    if train_file.is_dir():
        candidates = sorted(train_file.glob("*.jsonl"))
        if not candidates:
            raise SystemExit(f"No JSONL training file found in {train_file}")
        train_file = candidates[0]
    rows = [json.loads(line) for line in train_file.read_text().splitlines() if line.strip()]
    if args.validate_only:
        assert rows and all({"instruction", "input", "output"} <= row.keys() for row in rows)
        print(f"Validated {len(rows)} SFT records for {cfg['model_name']}")
        return

    import torch
    from datasets import Dataset
    from peft import LoraConfig, prepare_model_for_kbit_training
    from transformers import (AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,
                              DataCollatorForLanguageModeling, Trainer, TrainingArguments)

    quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                               bnb_4bit_compute_dtype=torch.bfloat16) if cfg["use_4bit"] else None
    tokenizer = AutoTokenizer.from_pretrained(cfg["model_name"])
    tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(cfg["model_name"], quantization_config=quant,
                                                 device_map="auto")
    if quant:
        model = prepare_model_for_kbit_training(model)
    lora = LoraConfig(r=cfg["lora_rank"], lora_alpha=cfg["lora_alpha"],
                      lora_dropout=cfg["lora_dropout"], task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    from peft import get_peft_model
    model = get_peft_model(model, lora)
    dataset = Dataset.from_list([{"text": format_example(row)} for row in rows])
    dataset = dataset.map(lambda batch: tokenizer(batch["text"], truncation=True,
                                                   max_length=cfg["max_length"]), batched=True)
    train_args = TrainingArguments(output_dir=cfg["output_dir"], num_train_epochs=cfg["epochs"],
        per_device_train_batch_size=cfg["batch_size"], gradient_accumulation_steps=cfg["gradient_accumulation_steps"],
        learning_rate=cfg["learning_rate"], logging_steps=5, save_strategy="epoch", report_to="none")
    trainer = Trainer(model=model, args=train_args, train_dataset=dataset,
                      data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False))
    trainer.train()
    model.save_pretrained(cfg["output_dir"])
    tokenizer.save_pretrained(cfg["output_dir"])
    print(f"Saved LoRA adapter to {cfg['output_dir']}")


if __name__ == "__main__":
    main()
