import streamlit as st
import joblib

st.set_page_config(
    page_title="SpamGuard AI",
    page_icon="🛡️",
    layout="centered"
)

model = joblib.load("spam_model.pkl")
tfidf = joblib.load("tfidf.pkl")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #090e20, #17143b, #0c1630);
    color: #f8fafc;
}
.block-container {
    max-width: 850px;
    padding-top: 3rem;
}
.hero {
    text-align: center;
    padding: 35px 10px 25px;
}
.logo {
    font-size: 55px;
}
.hero h1 {
    font-size: clamp(38px, 8vw, 62px);
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    color: #b9c3da;
    font-size: 17px;
}
.tag {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #7959d8;
    border-radius: 30px;
    color: #c4b5fd;
    background: #8b5cf622;
    font-size: 13px;
}
div[data-testid="stTextArea"] textarea {
    background: #151d38;
    color: white;
    border: 1px solid #60538e;
    border-radius: 15px;
    font-size: 16px;
}
div.stButton > button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white;
    font-weight: 700;
    font-size: 17px;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #6d28d9, #1d4ed8);
    color: white;
}
.result {
    padding: 24px;
    border-radius: 16px;
    margin-top: 20px;
    text-align: center;
}
.spam {
    background: #451b35;
    border: 1px solid #fb7185;
    color: #fecdd3;
}
.safe {
    background: #123b36;
    border: 1px solid #34d399;
    color: #a7f3d0;
}
.footer {
    text-align: center;
    color: #94a3b8;
    padding: 30px 0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="logo">🛡️</div>
    <span class="tag">✦ MACHINE LEARNING POWERED</span>
    <h1>SpamGuard AI</h1>
    <p class="subtitle">
        Smart SMS Spam Detection<br>
        Analyze suspicious messages instantly.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔍 Analyze Your Message")
message = st.text_area(
    "Paste your SMS below",
    placeholder="Enter or paste a message here...",
    height=160
)

if st.button("✦ Analyze Message"):
    if message.strip():
        vector = tfidf.transform([message])
        prediction = model.predict(vector)[0]

        if prediction == "spam":
            st.markdown("""
            <div class="result spam">
                <h2>⚠️ Spam Detected</h2>
                <p>This message may be suspicious.
                Avoid clicking unknown links.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="result safe">
                <h2>✓ Looks Safe</h2>
                <p>This message was classified
                as a normal SMS.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please enter a message first.")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.metric("Model Accuracy", "98.39%")
with c2:
    st.metric("AI Model", "Linear SVM")

st.caption(
    "Predictions are automated and not a guarantee "
    "that a message is safe."
)

st.markdown("""
<div class="footer">
    SPAMGUARD AI • BUILT WITH PYTHON & STREAMLIT
</div>
""", unsafe_allow_html=True)
