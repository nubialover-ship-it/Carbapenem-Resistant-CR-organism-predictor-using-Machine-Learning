# 🧬 Carbapenem Resistance Predictor

A Machine Learning tool to predict 
carbapenem antibiotic resistance in 
bacterial isolates using clinical and 
microbiological hospital data from Middle East.

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-red)](https://carbapenem-resistance-predictor-using-machine-learn.streamlit.app/)

---

## 📋 Background

Carbapenem antibiotics represent the last 
line of defence against severe bacterial 
infections. The emergence of carbapenem-
resistant organisms (CRO) poses a critical 
global health threat, limiting treatment 
options and increasing mortality.

This tool uses machine learning to predict 
carbapenem resistance from clinical and 
microbiological data, enabling earlier 
clinical decision-making and targeted 
infection control measures.

---

## 📊 Dataset

| Feature | Detail |
|---------|--------|
| Total isolates | 1,654 |
| Original features | 43 |
| Final features | 53 |
| Target | Binary (ESBL vs CR) |
| Class 0 | ESBL (80.4%) |
| Class 1 | Carbapenem Resistant (19.6%) |
| Source | Saudi Arabian hospital data |

---

## 🔧 Pre-Processing
✅ Removed 19 duplicate records
✅ Target variable created from:
→ TORE column (resistance type)
→ IMP (Imipenem) MIC values
→ MEM (Meropenem) MIC values
✅ Intermediate (I) treated as Resistant
✅ Age encoded as ordinal groups (1-5)
✅ Hospital level extracted from ward codes
✅ CAHA typos standardised
✅ Blank antibiotic values imputed with mode
✅ AMP dropped (single unique value)
✅ IMP and MEM excluded (data leakage!)
✅ TORE excluded (answer key!)
 
 ---

## ⚙️ Feature Engineering

Demographics:
→ GENDER: Male=1, Female=0
→ AGE: Ordinal 1-5
1=Paediatric (0-18)
2=Young Adult (19-35)
3=Middle Aged (36-50)
4=Older Adult (51-65)
5=Elderly (66+)
Hospital Level:
→ Ward extracted from codes
(L1T1, L2T2 → Level 1, Level 2)
→ ICU=9, NICU=10, General=0
Encoding:
→ Antibiotics: S=0, I=1, R=2
→ Categoricals: One-hot encoded
(SAMPLE, ORGANISM, CAHA, CDIG, Ward)
Multicollinearity Reduction:
→ VIF analysis performed
→ 11 correlated features removed:
Cephalosporins: CTX, CRO, CTIN, CXM, ATZ, CAZ
Fluoroquinolones: LEV, NOR, OFL
Aminoglycosides: TOB
Penicillins: PEP
→ Final: 64 → 53 features
→ All VIF < 10 

---

## 📈 Exploratory Data Analysis

### Key Findings

| Variable | Finding |
|----------|---------|
| Organism | Acinetobacter baumannii 99.1% CR |
| Organism | Pseudomonas aeruginosa 85.6% CR |
| CAHA | Hospital transfers 42.2% CR |
| Ward | Level 6 (long-term) 49.4% CR |
| Ward | ICU 46.3% CR |
| Gender | Males 28.8% vs Females 9.7% |
| Age | Elderly 31.4% vs Paediatric 9.3% |
| Sample | Respiratory 40.1% CR |

### Statistical Analysis

| Variable | Chi-square | p-value |
|----------|-----------|---------|
| ORGANISM | 1278.77 | <0.0001 |
| CAHA | 242.32 | <0.0001 |
| CDIG | 173.71 | <0.0001 |
| SAMPLE | 149.82 | <0.0001 |
| GENDER | 94.11 | <0.0001 |

### Correlation Analysis
### Key Findings

| Variable | Finding |
|----------|---------|
| Organism | Acinetobacter baumannii 99.1% CR |
| Organism | Pseudomonas aeruginosa 85.6% CR |
| CAHA | Hospital transfers 42.2% CR |
| Ward | Level 6 (long-term) 49.4% CR |
| Ward | ICU 46.3% CR |
| Gender | Males 28.8% vs Females 9.7% |
| Age | Elderly 31.4% vs Paediatric 9.3% |
| Sample | Respiratory 40.1% CR |

### Statistical Analysis

| Variable | Chi-square | p-value |
|----------|-----------|---------|
| ORGANISM | 1278.77 | <0.0001 |
| CAHA | 242.32 | <0.0001 |
| CDIG | 173.71 | <0.0001 |
| SAMPLE | 149.82 | <0.0001 |
| GENDER | 94.11 | <0.0001 |

### Correlation Analysis
High correlations found (r > 0.9):
→ CTX ↔ CRO: r=0.992
→ CIP ↔ LEV: r=0.962
→ CTIN ↔ CXM: r=0.956
→ VIF scores: CRO=1217, CTX=1108
→ Action: removed correlated features
## 🤖 Modelling Pipeline

Train/Test Split: 80/20 stratified
SMOTE applied to training only
→ Balanced: 1063/1063 (50/50)
Three models trained and compared
5-Fold Stratified Cross Validation
Best model selected and deployed

# 🏆 Model Results

### Test Set Performance

| Model | Macro F1 | CR Recall | ROC AUC |
|-------|---------|-----------|---------|
| **Random Forest** | **0.958** | **95.4%** | **0.980** |
| SVC | 0.952 | 92.3% | 0.978 |
| Logistic Regression | 0.948 | 92.3% | 0.976 |

### Cross Validation Results

| Model | CV F1 Mean | CV F1 Std |
|-------|-----------|-----------|
| **Random Forest** | **0.969** | **±0.009** |
| SVC | 0.972 | ±0.014 |
| Logistic Regression | 0.964 | ±0.013 |

### Best Model — Random Forest
Confusion Matrix:
[[260   6]
[  3  62]]
True Negatives:  260/266 = 97.7% ✅
False Positives:   6/266 =  2.3%
False Negatives:   3/65  =  4.6% ✅
True Positives:   62/65  = 95.4% ✅
Only 3 CR cases missed out of 65!

# 🏆 Model Results

### Test Set Performance

| Model | Macro F1 | CR Recall | ROC AUC |
|-------|---------|-----------|---------|
| **Random Forest** | **0.958** | **95.4%** | **0.980** |
| SVC | 0.952 | 92.3% | 0.978 |
| Logistic Regression | 0.948 | 92.3% | 0.976 |

### Cross Validation Results

| Model | CV F1 Mean | CV F1 Std |
|-------|-----------|-----------|
| **Random Forest** | **0.969** | **±0.009** |
| SVC | 0.972 | ±0.014 |
| Logistic Regression | 0.964 | ±0.013 |

## 🔍 Feature Importance

| Category | Importance |
|----------|-----------|
| Antibiotics | 43.0% |
| Organism | 32.6% |
| Ward | 6.9% |
| Infection Source | 6.9% |
| Demographics | 5.6% |
| Sample Type | 2.8% |
| Diagnosis | 2.1% |

### Top 5 Features

ORGANISM_Escherchia coli    13.5%
(negative predictor of CR)
F (Nitrofurantoin)          10.0%
(paradoxical CR predictor)
ORGANISM_Pseudomonas        8.7%
TZP (Pip-Tazobactam)        7.9%
AMC (Amoxicillin-Clav)      5.4%

## 🛠️ Tools and Technologies
Language:     Python 3.13
ML Library:   scikit-learn 1.8.0
Imbalancing:  imbalanced-learn (SMOTE)
Data:         pandas, numpy
Visualisation: matplotlib, seaborn
Deployment:   Streamlit
Version Control: Git, GitHub