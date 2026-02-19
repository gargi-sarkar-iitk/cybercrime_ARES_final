# Towards Dependable AI-Assisted Cybercrime Response

[![ARES 2024](https://img.shields.io/badge/ARES-2024-blue)](https://www.ares-conference.eu/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Paper](https://img.shields.io/badge/Paper-PDF-red)](link-to-paper)

> **Financial Intelligence Reconstruction and Intervention-Aware Evaluation Using Large-Scale Police Complaint Data**

Official repository for the ARES 2024 paper investigating the **intervention-data quality gap** in AI-assisted cybercrime response systems through large-scale analysis of 19,480 verified investment-fraud complaints.

---

## 📌 Paper Abstract

Digital investment fraud poses a large-scale threat to financial security, yet cybercrime response infrastructures frequently suffer from **incomplete complaint data**, **inconsistent financial reporting**, and **delayed intervention mechanisms**. This paper presents an **intervention-aware AI-assisted complaint-intelligence pipeline** evaluated on over 19,000 verified investment-fraud complaints, revealing a **counterintuitive trade-off**: improvements in semantic completeness do not always increase intervention probability, exposing an **intervention-data quality gap** in operational cybercrime response systems.

**Key Finding:** While LLM-based financial reconstruction achieves 84.9% tolerance accuracy @10%, Payment-on-Hold (POH) activation exhibits a **negative association** with semantic completeness (OR = 0.788, p < 0.001), indicating that data quality alone does not deterministically improve intervention outcomes—timing and institutional responsiveness dominate recovery effectiveness.

---

## 🎯 Core Contributions

### 1. **Data Quality–Intervention Link** (First Large-Scale Evidence)
- Empirically demonstrates that complaint-level data quality is **systematically associated** with financial intervention outcomes
- Reveals **counterintuitive negative relationship** between semantic completeness and POH activation probability
- Reframes cybercrime analytics as a **data-quality-driven operational problem** rather than purely predictive task

### 2. **Deterministic LLM Financial Reconstruction at Scale**
- **Context-aware methodology** recovering incomplete financial-loss information from unstructured narratives
- Evaluated on **19,480 complaints** with **84.9% tolerance accuracy @10%**
- Preserves **numerical magnitude ordering** and **bounded error behavior**
- Two-stage pipeline: weak LLM translation + deterministic rule-based normalization

### 3. **Intervention-Aware Modeling**
- Operationalizes **Payment-on-Hold (POH)** as measurable availability indicator
- Quantifies relationship between complaint attributes and financial recovery
- **POH activation increases recovery odds by 7.88× (β=2.0656, p<0.001)**
- Reveals **dominant effect of timing** over narrative completeness

---

## 🔬 Research Questions

| RQ | Question | Key Finding |
|----|----------|-------------|
| **RQ1** | What is field-level data availability in operational cybercrime databases? | 10.40% missing structured financial fields; 68.8% POH activation rate |
| **RQ2** | How consistent are victim-reported vs LLM-extracted amounts? | 92% align within 10% tolerance; Pearson r=0.959 (log-scale) |
| **RQ3** | What is LLM accuracy vs human-validated extractions? | MAE=Rs.107,534; MAPE=9.66%; Log-R²=0.844 |
| **RQ4** | What integrity anomalies exist across fields? | <3% severe anomalies after processing; dominated by multi-transaction aggregation |

---

## 📊 Dataset Overview

- **Source:** Anonymized state-level law-enforcement cybercrime portal
- **Timeframe:** 10 months of investment-fraud complaints
- **Scale:** 19,480 verified complaints (95.1% retention after deduplication)
- **Total Identifiable Loss:** Rs. 21.25 billion (~$255 million USD)
- **Avg Loss/Complaint:** Rs. 1,090,918 (~$13,100 USD)

### Key Statistics

| Metric | Value |
|--------|-------|
| Complaints with POH activation | 68.8% |
| Mean POH recovery ratio | 0.2344 (23.44%) |
| Median POH recovery ratio | 0.0780 (7.80%) |
| Records requiring semantic reconstruction | 4,764 (24.5%) |
| Cumulative upward adjustment from LLM | Rs. 13.03 billion |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: Data Intake & Anonymization                          │
│  Alignment: Confidentiality                                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2: Structural Cleaning & Normalization                  │
│  ├─ Stage 1: Composite key construction (name + age)           │
│  ├─ Stage 2: ROUGE-L similarity deduplication (threshold=0.70) │
│  └─ Stage 3: Completeness filtering & range validation         │
│  Alignment: Data Integrity                                      │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: Linguistic & Semantic Enhancement                    │
│  ├─ Meta-LLaMA-3-8B-Instruct (8-bit quantization)              │
│  ├─ Greedy decoding (deterministic, no sampling)               │
│  ├─ Rule-based normalization (9-stage ComplaintNormalizer)     │
│  └─ Human-in-the-loop validation (high-value cases)            │
│  Alignment: Semantic Reliability                               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: Intelligence Aggregation (Unsupervised)              │
│  ├─ K-means clustering (K=2, silhouette=0.9783)                │
│  ├─ Features: log(loss), delay, demographics, POH indicator    │
│  └─ Operational stratification (not simple high/low loss)      │
│  Alignment: Analytical Consistency                             │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 5: Intervention Modeling & Availability Analysis        │
│  ├─ Logistic regression: POH activation predictors             │
│  ├─ Beta regression: Recovery ratio modeling                   │
│  └─ Intervention-data quality gap quantification               │
│  Alignment: Intervention Availability                          │
└─────────────────────────────────────────────────────────────────┘
```

**Design Principle:** Each layer aligns with a **dependable computing attribute** (confidentiality, integrity, reliability, availability) rather than treating the pipeline as purely statistical.

---

## 🔑 Key Findings

### Finding 1: Intervention-Data Quality Gap

**Counterintuitive Result:** Higher semantic completeness is **negatively associated** with POH activation.

| Predictor | Odds Ratio | 95% CI | p-value | Interpretation |
|-----------|------------|--------|---------|----------------|
| log(Loss) | 1.264 | [1.242, 1.286] | <0.001 | Higher loss → Higher POH probability |
| Completeness Score | **0.788** | [0.763, 0.814] | <0.001 | **Richer narratives → Lower POH probability** |

**Explanation:** Complaints with richer narratives likely reflect:
- **Delayed reporting** (intervention window already closed)
- **Complex fraud scenarios** (multi-layered, harder to freeze)
- **Higher victim literacy** (longer narratives, but later reporting)

**Implication:** Data quality improvements must be coupled with **temporal optimization** and **institutional responsiveness** to achieve intervention effectiveness.

---

### Finding 2: POH Dominates Recovery Outcomes

**Beta Regression Results (Recovery Ratio):**

| Predictor | Coefficient (logit scale) | 95% CI | p-value |
|-----------|--------------------------|--------|---------|
| log(Loss) | -0.2031 | [-0.2125, -0.1937] | <0.001 |
| Completeness | -0.0698 | [-0.0878, -0.0518] | <0.001 |
| **POH Activation** | **+2.0656** | [2.0250, 2.1061] | <0.001 |

**Key Insight:** POH activation increases recovery odds by **exp(2.0656) ≈ 7.88×**, dwarfing the effect of data quality.

**Practical Takeaway:** Investment in **early-stage triage** and **rapid institutional response** yields greater recovery improvements than purely improving narrative completeness.

---

### Finding 3: LLM Reconstruction Reliability

**Performance Metrics (n=4,764 semantically reconstructed complaints):**

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Mean Absolute Error | Rs. 107,534 | ~10% of median loss |
| MAPE | 9.66% | Bounded proportional error |
| Log-scale R² | 0.844 | Strong magnitude preservation |
| Tolerance Accuracy @10% | 84.9% | Nearly 6 in 7 cases accurate |
| Tolerance Accuracy @20% | 86.8% | Robust to informal reporting |

**Comparison to Baselines:**

| Method | Coverage | Log-MAE | Acc@10% | Log-R² |
|--------|----------|---------|---------|--------|
| Direct Structured Field (B0) | 100% | 0.4057 | 68.3% | 0.7348 |
| Deterministic Token Extraction (B1) | 85.8% | 1.9689 | 47.3% | 0.0864 |
| Off-the-Shelf NER (B2) | 59.2% | 1.4619 | 45.6% | 0.1190 |
| Hybrid Rule+Context (B3) | 100% | 1.8821 | 48.6% | 0.1035 |
| **Contextual LLM (Ours, B4)** | **100%** | **0.2531** | **84.7%** | **0.8540** |

**Advantage:** 16–39 percentage point improvement in tolerance accuracy over deterministic/hybrid baselines.

---

### Finding 4: Stratification Reveals Institutional Heterogeneity

**K-means Clustering (K=2):**

| Cluster | N | Median Loss | P(POH) | Mean Recovery |
|---------|---|-------------|--------|---------------|
| 0 | 14,731 | Rs. 69,450 | 67.4% | 0.236 |
| 1 | 4,749 | Rs. 64,367 | **73.3%** | 0.229 |

**Key Observation:** Cluster 1 has **lower median loss** but **higher POH activation rate** → separation reflects **institutional responsiveness**, not just financial magnitude.

**Silhouette Score = 0.9783** → extremely strong macro-structural bifurcation.

---

## 🛠️ Repository Structure

```
.
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
│
├── translate.py                       # Two-stage LLM translation pipeline
│   ├── Meta-LLaMA-3-8B-Instruct (8-bit)
│   ├── ComplaintNormalizer (9-stage deterministic cleanup)
│   └── Validation framework
│
├── cybercrime_ARES_final.ipynb       # Analysis notebook
│   ├── Section 3: Data Availability & Completeness
│   ├── Section 4: Data Integrity
│   ├── Section 5: LLM Performance Evaluation
│   ├── Section 6: Intervention Modeling (Logistic + Beta Regression)
│   └── Section 7: Paper-Ready Tables & Figures
│
├── figures/                           # 11 publication-ready figures (300 DPI)
│   ├── fig01_completeness_scorecard.{png,pdf}
│   ├── fig02_nullity_matrix.{png,pdf}
│   ├── fig03_availability_heatmap.{png,pdf}
│   ├── fig04_suspect_intelligence.{png,pdf}
│   ├── fig05_poh_analysis.{png,pdf}
│   ├── fig06_amount_integrity.{png,pdf}
│   ├── fig07_anomaly_report.{png,pdf}
│   ├── fig08_llm_performance.{png,pdf}
│   ├── fig09_llm_vs_reported.{png,pdf}
│   ├── fig10_radar_quality.{png,pdf}
│   └── fig11_district_availability.{png,pdf}
│
└── outputs/
    ├── paper_summary_stats.csv
    └── table_summary.tex
```

---

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.8+, CUDA-capable GPU (for translation)
pip install -r requirements.txt

# Hugging Face token (for LLaMA-3 access)
export HF_TOKEN="your_hf_token_here"
```

### Option 1: Run Analysis Only (Pre-translated Data)

If you already have translated complaint data:

```bash
# 1. Update data path in cybercrime_ARES_final.ipynb
DATA_PATH = 'your_dataset.csv'  # Must have all 18 columns

# 2. Run notebook
jupyter notebook cybercrime_ARES_final.ipynb

# 3. Execute all cells → generates 11 figures + summary tables
```

**Required Columns:**
```
SI_No, Acknowledgement_No, District, Police_Station, Name_of_Victim,
Gender, Minor_Head, Amount_Loss, POH, Age, Age_Group, Profession,
Suspect_URL_Website, Suspect_Platform, English_Translation, Brief,
LLM_Predicted_Amount, Final_Amount_Loss
```

### Option 2: Full Pipeline (Translation + Analysis)

If you have raw Romanized Telugu/mixed-script complaints:

```bash
# 1. Configure translate.py
INPUT_XLSX = "your_raw_complaints.csv"
TEXT_COLUMN = "Brief"
MODE = "test"  # Start with test mode (10 rows)

# 2. Run test translation
python translate.py
# → Check terminal validation report

# 3. Switch to full mode
MODE = "full"
python translate.py

# 4. Run analysis notebook (as in Option 1)
```

---

## 📐 Two-Stage Translation Pipeline

### Stage 1: Weak LLM Translation

**Model:** Meta-LLaMA-3-8B-Instruct (8-bit quantization)

**Configuration:**
- Context window: 2,048 tokens
- Max generation: 512 tokens
- Decoding: **Greedy (deterministic, no sampling)**
- Temperature: Disabled
- Fine-tuning: **None** (zero-shot inference only)

**Prompt (minimalist):**
```
"Translate Romanized Telugu to English. Output only the translation."
```

**Why Weak Translation?**  
LLM provides **contextual interpretation** but may include:
- Meta-commentary ("Here is the translation:")
- Hallucinated category headers ("Online Investment Fraud:")
- Stylistic artifacts

**Solution:** Delegate semantic authority to deterministic post-processing.

---

### Stage 2: Deterministic Normalization (ComplaintNormalizer)

**9-stage rule-based cleanup:**

```python
class ComplaintNormalizer:
    """
    Deterministic normalizer for Romanized Telugu → English
    """
    def normalize(self, text: str) -> str:
        # Stage 1: Remove assistant/meta leakage
        text = remove_patterns("assistant:", "here is the translation:")
        
        # Stage 2: Remove hallucinated category headers
        text = remove_patterns("online investment fraud:", "business fraud:")
        
        # Stage 3: Remove boilerplate (preserve letter-style narratives)
        text = remove_patterns("respected sir/madam", "kindly investigate")
        
        # Stage 4: Fix grammar ("saying to invest" → "saying they would invest")
        text = fix_saying_to_constructions(text)
        
        # Stage 5: Normalize words (promised→said, claiming→saying, allegedly→∅)
        
        # Stage 6: Fix time (1930 hours → called 1930)
        
        # Stage 7: Cleanup whitespace & surrounding quotes
        
        # Stage 8: Drop meaningless remnants ("victim", "a person")
        
        # Stage 9: Capitalize first letter
        
        return text
```

**Validation Framework:**
```python
Forbidden Patterns Detected:
✓ META issues   : "here is", "note:"
✓ WORD issues   : "promised", "claiming", "allegedly"
✓ GRAMMAR issues: "saying to" (should be "saying they would")
✓ FORMAT issues : "1930 hours", "in 1930"
✓ LABEL issues  : Starts with category label

Validation Report:
Total rows: 19,480
Clean rows: 18,956 (97.3%)
Issues detected: 524 (2.7%)
```

---

## 📊 Reproducing Paper Results

### Table 1: Three-Stage Financial Integrity

```python
# Stage 1: Duplicate removal (ROUGE-L similarity)
# Stage 2: Amount validation (remove invalid records)
# Stage 3: AI fusion (LLM reconstruction)

Total Records:           20,474 → 19,480 (95.1% retention)
Total Identifiable Loss: Rs. 7.80B → Rs. 21.25B (semantic reconstruction)
LLM Amounts Extracted:   4,764 complaints
Cumulative Upward Adj:   Rs. 13.03B (row-wise correction potential)
```

### Table 2: LLM Performance Metrics

```python
Mean Absolute Error:     Rs. 107,534
MAPE:                    9.66%
Log-scale R²:            0.844
Tolerance Accuracy @10%: 84.9%
Tolerance Accuracy @20%: 86.8%
```

### Table 3: Logistic Regression (POH Activation)

```python
Predictor: log(Loss)
  Odds Ratio = 1.264 [1.242, 1.286], p < 0.001
  
Predictor: Completeness Score
  Odds Ratio = 0.788 [0.763, 0.814], p < 0.001  ← NEGATIVE!

Model Performance:
  Pseudo-R² = 0.0397
  AUC = 0.6324 (modest, institutional factors dominate)
```

### Table 4: Beta Regression (Recovery Ratio)

```python
Predictor: log(Loss)       β = -0.2031, p < 0.001
Predictor: Completeness    β = -0.0698, p < 0.001
Predictor: POH Activation  β = +2.0656, p < 0.001  ← DOMINANT!

Interpretation: POH increases recovery odds by exp(2.0656) ≈ 7.88×
```

---

## 🔬 Intervention-Data Quality Gap

### Conceptual Framework

```
Traditional Assumption:
  Better Data Quality → Better Intervention Outcomes

Empirical Reality (This Paper):
  Better Data Quality ⟿ Intervention Outcomes
  
  Where ⟿ denotes "complex, mediated relationship influenced by
           timing, institutional capacity, and fraud complexity"
```

### Why Richer Narratives Correlate with Lower POH Activation

**Hypothesis 1: Temporal Mediation**
- Victims who write detailed narratives may take longer to report
- By the time report is filed, funds already withdrawn
- **Intervention window closed** before complaint processing

**Hypothesis 2: Fraud Complexity**
- Complex fraud schemes → longer narratives (multi-step processes)
- Complex schemes → harder to freeze (layered mule accounts)
- Narrative richness is a **proxy for fraud sophistication**

**Hypothesis 3: Reporting Context**
- Higher-literacy victims write longer narratives
- But may not report faster (confidence in self-resolution)
- **Quality ≠ Urgency**

### Policy Implications

**What Doesn't Work:**
- ❌ Purely improving data completeness
- ❌ Encouraging longer, more detailed narratives
- ❌ Post-hoc semantic enhancement alone

**What Works:**
- ✅ **Early-stage triage** (flag time-sensitive cases immediately)
- ✅ **Temporal signals** (reporting delay as primary predictor)
- ✅ **Rapid institutional response** (POH within 24–48 hours)
- ✅ **Platform-level coordination** (bank/telecom real-time alerts)

---

## 🔐 Privacy & Ethics

### Data Protection Measures

1. **Full Anonymization:**
   - Victim names → `Victim_001`, `Victim_002`, ...
   - Police stations → `PS_01`, `PS_02`, ...
   - Phone numbers, emails, Aadhaar → **Removed**

2. **Institutional Approval:**
   - IRB approval obtained
   - Data sharing agreement with law enforcement
   - GDPR/local privacy law compliance

3. **Controlled Processing:**
   - LLM operates in **inference-only mode** (no training)
   - No external API calls (all local processing)
   - Original complaints retained as authoritative ground truth

4. **Aggregated Reporting:**
   - Paper reports **only aggregated statistics**
   - No individual case details published
   - Anonymized examples only

---

## 📖 Citation

**BibTeX:**

```bibtex
@inproceedings{ares2024cybercrime,
  title     = {Towards Dependable {AI}-Assisted Cybercrime Response:
               Financial Intelligence Reconstruction and 
               Intervention-Aware Evaluation Using Large-Scale 
               Police Complaint Data},
  author    = {[Authors - To Be Revealed Upon Acceptance]},
  booktitle = {Proceedings of the 19th International Conference on
               Availability, Reliability and Security (ARES)},
  year      = {2024},
  publisher = {ACM},
  note      = {Under Review}
}
```

---

## 📧 Contact

- **Correspondence:** [To be added upon acceptance]
- **Institution:** [To be added upon acceptance]
- **Conference:** ARES 2024

---

## 📜 License

**MIT License** - see [LICENSE](LICENSE) file.

**Third-Party Acknowledgments:**
- Meta-LLaMA-3 (Meta Community License)
- Hugging Face Transformers (Apache 2.0)
- PyTorch (BSD 3-Clause)

---

## 🙏 Acknowledgments

We thank:
- Law enforcement agencies for providing anonymized data
- ARES 2024 program committee and reviewers
- Hugging Face for model hosting infrastructure
- Open-source community for foundational libraries

---

## 📚 Related Work & References

**Key Papers:**

1. **Dependable Computing Foundations:**
   - Avizienis et al. (2004) - Basic concepts and taxonomy of dependable and secure computing
   - Laprie (1992, 2008) - Dependability terminology and resilience

2. **LLMs in Legal/Forensic Contexts:**
   - Devlin et al. (2019) - BERT pre-training
   - Brown et al. (2020) - GPT-3 few-shot learning
   - Katz et al. (2024) - GPT-4 passes the bar exam
   - Chalkidis et al. (2020) - LEGAL-BERT

3. **Fraud Detection & Analytics:**
   - Ngai et al. (2011) - Data mining in fraud detection
   - Huang et al. (2018) - CoDetect anomaly detection
   - Yang et al. (2025) - LLM4FD zero-shot fraud detection

4. **Data Quality & Information Systems:**
   - Wang & Strong (1996) - Beyond accuracy: data quality dimensions
   - Batini & Scannapieco (2016) - Data and information quality

**Full Bibliography:** See paper Section 7.

---

<div align="center">


</div>
