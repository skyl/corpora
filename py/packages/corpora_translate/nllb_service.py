from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = FastAPI()

model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


class TranslationRequest(BaseModel):
    text: str
    source_lang: str  # e.g. "eng_Latn"
    target_lang: str  # e.g. "fra_Latn"


@app.post("/translate")
def translate(req: TranslationRequest):
    tokenizer.src_lang = req.source_lang
    encoded = tokenizer(req.text, return_tensors="pt")

    output_tokens = model.generate(
        **encoded,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids(req.target_lang),
        max_length=100,
        num_beams=4,
    )

    decoded = tokenizer.batch_decode(output_tokens, skip_special_tokens=True)
    return {"translation": decoded[0]}
