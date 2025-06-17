import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# 使用NLLB-200模型（600M参数的小版本）
model_name = "facebook/nllb-200-distilled-600M"

# NLLB需要指定源语言和目标语言的代码
# 中文简体: zho_Hans, 英文: eng_Latn, 法文: fra_Latn
# 全部代码列表: https://huggingface.co/facebook/nllb-200-distilled-600M
tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang="zho_Hans", tgt_lang="fra_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)

text_to_translate = "今天天气真好，我们去公园散步吧。"

inputs = tokenizer(text_to_translate, return_tensors="pt").to(device)

translated_tokens = model.generate(
    **inputs,
    forced_bos_token_id=tokenizer.lang_code_to_id["fra_Latn"], # 强制指定目标语言
    max_length=128
)

translated_text = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]

print("-" * 30)
print(f"原文 (Original): {text_to_translate}")
print(f"译文 (Translated to French): {translated_text}")
print("-" * 30)