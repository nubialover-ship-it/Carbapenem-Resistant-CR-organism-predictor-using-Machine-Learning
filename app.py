import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Carbapenem Resistance Predictor",
    page_icon="🧬",
    layout="wide")

st.title("🧬 Carbapenem Resistance Predictor")
st.markdown("Predict carbapenem resistance from clinical and microbiological data.")
st.markdown("---")

@st.cache_resource
def load_model():
    with open('RF_carbapenem.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('RF_features.pkl', 'rb') as f:
        features = pickle.load(f)
    return model, features

model, feature_cols = load_model()
st.success(f"Model loaded successfully! ({len(feature_cols)} features)")

st.header("Patient Information")
col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender",
        ["Male", "Female"])
    age = st.selectbox("Age Group",
        [1, 2, 3, 4, 5],
        format_func=lambda x: {
            1: "1 - Paediatric (0-18)",
            2: "2 - Young Adult (19-35)",
            3: "3 - Middle Aged (36-50)",
            4: "4 - Older Adult (51-65)",
            5: "5 - Elderly (66+)"}[x])

with col2:
    organism = st.selectbox("Organism", [
        "Escherchia coli",
        "Klebsiella pneumonia",
        "Pseudomonas aeruginosa",
        "Acinetobacter baumannii",
        "Proteus mirabilis",
        "Providencia stuartii",
        "Citrobacter koseri",
        "Morganella morganii",
        "Serratia marcescens",
        "Enterobacter cloacae",
        "Enterobacter aerogenes",
        "Citrobacter freundii"])
    sample = st.selectbox("Sample Type", [
        "Urine",
        "Respiratory infection",
        "swab", "Blood",
        "Body fluid", "Tip"])

with col3:
    caha = st.selectbox("Infection Source", [
        "Community_Acquired",
        "Hospital_Acquired",
        "Transfer_Other_Hospital"])
    ward = st.selectbox("Ward", [
        "General_IPD", "ICU", "NICU",
        "Level_1", "Level_2", "Level_3",
        "Level_4", "Level_5", "Level_6",
        "Level_7", "Level_8"])
    cdig = st.selectbox("Diagnosis", [
        "Urinary tract infection",
        "Pneumonia", "Abscess",
        "Wound", "Bacteremia",
        "Gastroctomy feeding",
        "Vaginitis",
        "Respiratory infection",
        "Ear infection",
        "Eye infection"])

st.markdown("---")
st.header("Antibiotic Susceptibility")
st.markdown("**0** = Sensitive | **1** = Intermediate | **2** = Resistant")

col1, col2 = st.columns(2)
with col1:
    amc = st.selectbox("AMC - Amoxicillin-Clavulanate", [0,1,2])
    tzp = st.selectbox("TZP - Piperacillin-Tazobactam", [0,1,2])
    fep = st.selectbox("FEP - Cefepime",                [0,1,2])
    ak  = st.selectbox("AK  - Amikacin",                [0,1,2])
    cn  = st.selectbox("CN  - Gentamicin",              [0,1,2])

with col2:
    cip = st.selectbox("CIP - Ciprofloxacin",           [0,1,2])
    sxt = st.selectbox("SXT - Co-trimoxazole",          [0,1,2])
    f   = st.selectbox("F   - Nitrofurantoin",          [0,1,2])
    pep = st.selectbox("PEP - Piperacillin",            [0,1,2])

st.markdown("---")

if st.button("🔬 Predict Resistance",
             type="primary",
             use_container_width=True):

    input_dict = {col: 0 for col in feature_cols}

    input_dict['GENDER'] = 1 if gender == "Male" else 0
    input_dict['AGE'] = age
    input_dict['level_number'] = {
        'General_IPD': 0, 'Level_1': 1,
        'Level_2': 2,    'Level_3': 3,
        'Level_4': 4,    'Level_5': 5,
        'Level_6': 6,    'Level_7': 7,
        'Level_8': 8,    'ICU': 9,
        'NICU': 10}[ward]

    input_dict['AMC'] = amc
    input_dict['TZP'] = tzp
    input_dict['FEP'] = fep
    input_dict['AK']  = ak
    input_dict['CN']  = cn
    input_dict['CIP'] = cip
    input_dict['SXT'] = sxt
    input_dict['F']   = f
    input_dict['PEP'] = pep

    sample_key = f'SAMPLE_{sample}'
    if sample_key in input_dict:
        input_dict[sample_key] = 1

    org_key = f'ORGANISM_{organism}'
    if org_key in input_dict:
        input_dict[org_key] = 1

    caha_key = f'CAHA_{caha}'
    if caha_key in input_dict:
        input_dict[caha_key] = 1

    cdig_key = f'CDIG_{cdig}'
    if cdig_key in input_dict:
        input_dict[cdig_key] = 1

    ward_key = f'ward_category_{ward}'
    if ward_key in input_dict:
        input_dict[ward_key] = 1

    input_df = pd.DataFrame(
        [input_dict])[feature_cols]

    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0]

    st.markdown("---")
    st.header("Prediction Result")

    col1, col2 = st.columns(2)
    with col1:
        if pred == 1:
            st.error(
                "## 🚨 CARBAPENEM RESISTANT\n\n"
                "This isolate is predicted **Carbapenem Resistant**.\n\n"
                "Consider alternative therapy!")
        else:
            st.success(
                "## ✅ ESBL / Carbapenem Sensitive\n\n"
                "This isolate is predicted **sensitive to Carbapenems**.\n\n"
                "Carbapenem therapy may be effective!")

    with col2:
        st.metric("ESBL Probability",
                  f"{prob[0]*100:.1f}%")
        st.metric("Carbapenem R Probability",
                  f"{prob[1]*100:.1f}%")
        cr_prob = prob[1] * 100
        if cr_prob >= 70:
            risk = "🔴 HIGH RISK"
        elif cr_prob >= 40:
            risk = "🟡 MODERATE RISK"
        else:
            risk = "🟢 LOW RISK"
        st.metric("Risk Level", risk)

st.markdown("---")
with st.expander("Model Information"):
    st.markdown("""
    - **Model:** Random Forest Classifier
    - **Features:** 53 clinical and microbiological
    - **CR Recall:** 95.4%
    - **ROC AUC:** 0.980
    - **CV F1:** 0.969
    
    *For research purposes only.*
    """)

    