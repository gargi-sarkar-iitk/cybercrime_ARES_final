#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime

# =====================================================
# CONFIG
# =====================================================

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

MODE = "full"  # "test" or "full"

INPUT_XLSX = "investment_fraud_raw.csv"
OUTPUT_XLSX = "investment_fraud_translated.xlsx"

TEXT_COLUMN = "Brief"
OUTPUT_COLUMN = "English_Translation"

MAX_INPUT_TOKENS = 2048
MAX_NEW_TOKENS = 512
do_sample = False
load_in_8bit = True

# =====================================================
# LOAD MODEL
# =====================================================

HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN not set")

if not torch.cuda.is_available():
    raise RuntimeError("CUDA not available")

print("✅ CUDA OK — GPU:", torch.cuda.get_device_name(0))
print("📥 Loading model (8-bit)...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=HF_TOKEN)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    load_in_8bit=True,
    device_map="auto",
    token=HF_TOKEN
)
model.eval()

print("✅ Model loaded!")

# =====================================================
# MINIMAL PROMPT - JUST TRANSLATE
# =====================================================

def build_messages(text: str):
    """Ultra-simple prompt - let post-processing handle the rest"""
    return [
        {
            "role": "system",
            "content": "Translate Romanized Telugu to English. Output only the translation."
        },
        {
            "role": "user",
            "content": text
        }
    ]
import re

class ComplaintNormalizer:
    """
    Deterministic normalizer for Romanized Telugu → English police complaint translations.
    Letter-style complaints are preserved; only hallucinated boilerplate is removed.
    """

    def __init__(self):
        self.patterns = self._compile_patterns()

    def _compile_patterns(self):
        return {
            # Assistant / meta leakage
            "assistant_prefix": re.compile(
                r'^\s*assistant\s*[:\-]?\s*',
                re.IGNORECASE
            ),

            "meta_translation": re.compile(
                r'^(here is|this is|below is).{0,40}?(translation|translated text|english version)\s*[:\-]?\s*',
                re.IGNORECASE
            ),

            # Hallucinated category headers
            "category_header": re.compile(
                r'^(business|online|investment|financial).{0,120}?(fraud|scam|job|trading).*?:\s*',
                re.IGNORECASE
            ),

            # Boilerplate phrases to REMOVE but NOT truncate
            "boilerplate_phrases": re.compile(
                r'\b(respected sir/madam|respected sir|kindly investigate|'
                r'thank you for your assistance|yours sincerely)\b[:,]*',
                re.IGNORECASE
            ),

            # Saying-to grammar
            "saying_to": re.compile(
                r'\bsaying to ([a-z]+(?:\s+[a-z]+)?)\b',
                re.IGNORECASE
            ),

            # Word replacements
            "promised": re.compile(r'\bpromis(e|ed|ing|es)\b', re.IGNORECASE),
            "claiming": re.compile(r'\bclaim(s|ed|ing)?\b', re.IGNORECASE),
            "assured": re.compile(r'\bassur(e|ed|ing|es)\b', re.IGNORECASE),
            "allegedly": re.compile(r'\ballegedly\b\s*', re.IGNORECASE),

            # Time normalization
            "time_1930": re.compile(
                r'\b(at|around|in)?\s*1930\s*(hours)?\b',
                re.IGNORECASE
            ),

            # Cleanup
            "multi_space": re.compile(r'\s+'),
            "surrounding_quotes": re.compile(r'^[\'"](.*)[\'"]$', re.DOTALL),
        }

    def normalize(self, text: str, original_text: str = "") -> str:
        if not isinstance(text, str) or not text.strip():
            return ""

        # =====================================================
        # Stage 0: Initial cleanup
        # =====================================================
        text = text.strip()

        # =====================================================
        # Stage 1: Remove assistant / meta hallucinations
        # =====================================================
        text = self.patterns["assistant_prefix"].sub("", text)
        text = self.patterns["meta_translation"].sub("", text)

        # =====================================================
        # Stage 2: Remove hallucinated category headers
        # =====================================================
        text = self.patterns["category_header"].sub("", text)

        # =====================================================
        # Stage 3: Remove boilerplate politely (DO NOT TRUNCATE)
        # =====================================================
        text = self.patterns["boilerplate_phrases"].sub("", text)

        # =====================================================
        # Stage 4: Fix "saying to" constructions
        # =====================================================
        text = self.patterns["saying_to"].sub(
            r'saying they would \1',
            text
        )

        # =====================================================
        # Stage 5: Word normalization
        # =====================================================
        text = self._replace_word(text, self.patterns["promised"], "say")
        text = self._replace_word(text, self.patterns["claiming"], "say")
        text = self._replace_word(text, self.patterns["assured"], "say")
        text = self.patterns["allegedly"].sub("", text)

        # =====================================================
        # Stage 6: Time normalization
        # =====================================================
        text = self.patterns["time_1930"].sub("called 1930", text)

        # =====================================================
        # Stage 7: Cleanup whitespace & quotes
        # =====================================================
        text = self.patterns["multi_space"].sub(" ", text).strip()

        for _ in range(2):
            m = self.patterns["surrounding_quotes"].match(text)
            if m:
                text = m.group(1).strip()
            else:
                break

        # =====================================================
        # Stage 8: Drop meaningless remnants
        # =====================================================
        if text.lower() in {"victim", "a person", "the victim"}:
            return ""

        # =====================================================
        # Stage 9: Capitalize first letter
        # =====================================================
        if text and text[0].islower():
            text = text[0].upper() + text[1:]

        return text

    def _replace_word(self, text, pattern, base_word):
        def replacer(match):
            word = match.group(0).lower()
            if word.endswith("ed"):
                return "said"
            if word.endswith("ing"):
                return "saying"
            if word.endswith("s"):
                return "says"
            return base_word
        return pattern.sub(replacer, text)

# =====================================================
# COMPREHENSIVE NORMALIZATION RULES
# =====================================================


# Initialize normalizer globally
normalizer = ComplaintNormalizer()

# =====================================================
# TRANSLATE FUNCTION
# =====================================================

def translate_brief(text: str) -> str:
    """
    Two-stage approach:
    1. Let LLM translate (even if imperfect)
    2. Apply deterministic normalization rules
    """
    # Stage 1: Get raw translation
    messages = build_messages(text)
    
    encoded = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_INPUT_TOKENS
    )
    
    with torch.no_grad():
        output = model.generate(
            encoded,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id
        )
    
    decoded = tokenizer.decode(
        output[0][encoded.shape[-1]:],
        skip_special_tokens=True
    )
    
    # Stage 2: Normalize with rules
    normalized = normalizer.normalize(decoded, original_text=text)
    
    return normalized

# =====================================================
# VALIDATION
# =====================================================

def validate_translation(original_text, translated_text):
    """Check if normalization worked"""
    issues = []
    
    forbidden_patterns = {
        'promis': 'WORD: Contains "promised/promising"',
        'claim': 'WORD: Contains "claiming/claimed"',
        'assur': 'WORD: Contains "assured/assuring"',
        'allegedly': 'WORD: Contains "allegedly"',
        'here is': 'META: Contains "here is"',
        'note:': 'META: Contains "Note:"',
        'saying to': 'GRAMMAR: Contains "saying to" (should be "saying they would")',
        '1930 hours': 'FORMAT: Contains "1930 hours" (should be "called 1930")',
        'in 1930': 'FORMAT: Contains "in 1930"',
        'around 1930': 'FORMAT: Contains "around 1930"',
    }
    
    text_lower = translated_text.lower()
    for phrase, issue_msg in forbidden_patterns.items():
        if phrase in text_lower:
            issues.append(issue_msg)
    
    # Check if starts with category label
    category_starts = [
        'business & investment fraud',
        'business and investment fraud',
        'online fraud',
        'investment fraud',
        'business investment'
    ]
    for cat in category_starts:
        if text_lower.startswith(cat):
            issues.append('LABEL: Starts with category label')
            break
    
    return issues
def validate_batch(df, original_col, translated_col):
    """Batch validation with statistics"""
    results = []
    
    for idx, row in df.iterrows():
        original = str(row[original_col])
        translated = str(row[translated_col])
        
        if not translated or translated == 'nan':
            continue
        
        issues = validate_translation(original, translated)
        if issues:
            results.append({
                'row': idx,
                'issues': '; '.join(issues),
                'original': original[:200],
                'translated': translated[:200]
            })
    
    print("="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print(f"Total rows: {len(df)}")
    print(f"Rows with issues: {len(results)}")
    print(f"Clean rows: {len(df) - len(results)}")
    if len(df) > 0:
        print(f"Success rate: {((len(df)-len(results))/len(df)*100):.2f}%")
    
    if results:
        # Issue frequency
        issue_counts = {}
        for r in results:
            for issue in r['issues'].split('; '):
                issue_type = issue.split(':')[0]
                issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        print(f"\n{'ISSUE TYPE':<20} {'COUNT':<10}")
        print("-"*30)
        for issue, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{issue:<20} {count:<10}")
    
    return pd.DataFrame(results) if results else pd.DataFrame()

# =====================================================
# MAIN
# =====================================================

def main():
    print("="*80)
    print(f"TWO-STAGE TRANSLATION PIPELINE")
    print(f"Mode: {MODE.upper()} | Started: {datetime.now().strftime('%H:%M:%S')}")
    print("="*80)
    
    # Load data
    if INPUT_XLSX.endswith('.csv'):
        df = pd.read_csv(INPUT_XLSX, dtype=str)
    else:
        df = pd.read_excel(INPUT_XLSX, engine="openpyxl", dtype=str)
    
    if OUTPUT_COLUMN not in df.columns:
        df[OUTPUT_COLUMN] = ""
    
    # Determine limit
    limit = min(TEST_ROWS, len(df)) if MODE == "test" else len(df)
    output_file = TEST_OUTPUT if MODE == "test" else OUTPUT_XLSX
    
    print(f"\n📊 Processing {limit} rows...")
    
    # Process rows
    for idx in range(limit):
        text = df.at[idx, TEXT_COLUMN]
        
        if not isinstance(text, str) or not text.strip():
            df.at[idx, OUTPUT_COLUMN] = ""
            continue
        
        print(f"[{idx + 1}/{limit}]", end=" ", flush=True)
        try:
            translation = translate_brief(text)
            df.at[idx, OUTPUT_COLUMN] = translation
            print("✔")
        except Exception as e:
            print(f"✗ {e}")
            df.at[idx, OUTPUT_COLUMN] = f"[ERROR]"
    
    # Save
    df_output = df.head(limit)
    df_output.to_excel(output_file, index=False, engine="openpyxl")
    print(f"\n✅ Saved: {output_file}")
    
    # Validate
    print("\n🔍 Validating...")
    issues_df = validate_batch(df_output, TEXT_COLUMN, OUTPUT_COLUMN)
    
    if len(issues_df) > 0:
        issues_df.to_excel("issues.xlsx", index=False, engine="openpyxl")
        print("⚠️  Issues exported to: issues.xlsx")
    else:
        print("✅ All clear!")
        if MODE == "test":
            print("\n🎉 Ready for full run: MODE = 'full'")
    
    print(f"\nCompleted: {datetime.now().strftime('%H:%M:%S')}")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

