import streamlit as st
import joblib

# Extra safety checks for suspicious messages
import re

def check_warning_signs(message):

    text = message.lower()
    warnings = []

    # Prize / lottery scams
    prize_words = [
        "you won",
        "you have won",
        "winner",
        "free prize",
        "lottery",
        "claim your prize",
        "lucky winner",
        "cash prize",
        "reward",
        "congratulations"
    ]

    if any(word in text for word in prize_words):
        warnings.append("Unexpected prize or reward")

    # Banking / payment scams
    banking_words = [
        "bank account",
        "credit card",
        "debit card",
        "upi",
        "payment",
        "transaction",
        "refund",
        "kyc",
        "account blocked",
        "account suspended",
        "account will be blocked",
        "account will be closed",
        "bank details",
        "financial details"
    ]

    if any(word in text for word in banking_words):
        warnings.append("Possible banking or payment scam")

    # OTP / password / security scams
    security_words = [
        "otp",
        "one time password",
        "password",
        "verification code",
        "login code",
        "security code",
        "pin",
        "verify your identity",
        "verify your account"
    ]

    if any(word in text for word in security_words):
        warnings.append(
            "Requests or mentions sensitive security information"
        )

    # Urgent / threatening language
    urgent_words = [
        "urgent",
        "immediately",
        "act now",
        "within 24 hours",
        "account will be blocked",
        "account will be closed",
        "last chance",
        "verify now",
        "take action",
        "without delay",
        "avoid interruption",
        "service will stop",
        "services will continue"
    ]

    if any(word in text for word in urgent_words):
        warnings.append("Uses urgent or threatening language")

    # Account / service manipulation
    account_words = [
        "important update",
        "account update",
        "account activity",
        "account information",
        "service update",
        "service interruption",
        "linked to your account",
        "registered number",
        "confirm your details",
        "update your details",
        "review it today"
    ]

    if any(word in text for word in account_words):
        warnings.append("Contains suspicious account or service language")

    # Suspicious links
    if re.search(r"https?://|www\.", text):
        warnings.append("Contains a website link")

    # Suspicious call to action
    action_words = [
        "click here",
        "click the link",
        "claim now",
        "verify your account",
        "open this link",
        "download now",
        "login now",
        "confirm now",
        "update now",
        "check the link"
    ]

    if any(word in text for word in action_words):
        warnings.append("Contains a suspicious call to action")

    # Phone number detection
    if re.search(r"\b\d{10}\b", text):
        warnings.append("Contains a phone number")

    return warnings
def get_risk_info(prediction, warnings):
    if prediction == "spam":
        score = 70
    else:
        score = 10

    score += min(len(warnings) * 5, 25)
    score = min(score, 100)

    warning_text = " ".join(warnings).lower()
    if "banking" in warning_text or "payment" in warning_text:
        category = "Banking / Payment Scam"
    elif "security" in warning_text or "otp" in warning_text:
        category = "Phishing / Account Scam"
    elif "prize" in warning_text or "reward" in warning_text:
        category = "Prize / Lottery Scam"
    elif "website link" in warning_text:
        category = "Suspicious Link"
    elif "urgent" in warning_text or "threatening" in warning_text:
        category = "Urgency-Based Scam"
    else:
        category = "General Spam"

    if score >= 70:
        risk_level = "HIGH RISK"
    elif score >= 40:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "LOW RISK"

    return score, risk_level, category
st.set_page_config(
    page_title="SpamGuard AI | Smart SMS Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

model = joblib.load("spam_model.pkl")
tfidf = joblib.load("tfidf.pkl")

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.18), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(56,189,248,.12), transparent 25%),
        linear-gradient(145deg, #070b19 0%, #101632 48%, #0a1228 100%);
    color: #f8fafc;
}
.block-container { max-width: 1050px; padding-top: 1.5rem; padding-bottom: 2rem; }
.hero { text-align: center; padding: 42px 15px 28px; }
.logo { font-size: 62px; filter: drop-shadow(0 0 18px rgba(96,165,250,.35)); }
.hero h1 {
    margin: 12px 0 8px; font-size: clamp(42px, 7vw, 70px);
    font-weight: 850; letter-spacing: -2px;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.subtitle { color: #b8c3dc; font-size: 18px; line-height: 1.7; }
.tag {
    display: inline-block; padding: 8px 17px; border: 1px solid rgba(139,92,246,.7);
    border-radius: 999px; color: #ddd6fe; background: rgba(124,58,237,.13);
    font-size: 12px; font-weight: 700; letter-spacing: .7px;
}
.section-title { font-size: 24px; font-weight: 800; margin: 14px 0 8px; }
.helper { color: #94a3b8; font-size: 14px; margin-bottom: 12px; }
div[data-testid="stTextArea"] textarea {
    background: rgba(21,29,56,.92); color: white; border: 1px solid #4f5f91;
    border-radius: 16px; font-size: 16px; padding: 16px;
}
div.stButton > button {
    width: 100%; min-height: 50px; padding: 12px 18px; border: 1px solid rgba(255,255,255,.12);
    border-radius: 14px; background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white; font-weight: 800; font-size: 16px; box-shadow: 0 10px 25px rgba(37,99,235,.18);
}
div.stButton > button:hover {
    transform: translateY(-1px); background: linear-gradient(90deg, #8b5cf6, #3b82f6);
    color: white; border-color: rgba(255,255,255,.25);
}
.risk-card {
    background: linear-gradient(135deg, rgba(30,41,75,.88), rgba(15,23,42,.88));
    border: 1px solid rgba(129,140,248,.28); border-radius: 20px; padding: 24px; margin-top: 18px;
}
.risk-high { border-color: rgba(251,113,133,.55); box-shadow: 0 0 28px rgba(244,63,94,.10); }
.risk-medium { border-color: rgba(251,191,36,.45); }
.risk-low { border-color: rgba(52,211,153,.45); }
.risk-label { color: #94a3b8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }
.risk-value { font-size: 30px; font-weight: 850; margin-top: 4px; }
.score-number {
    font-size: 42px; font-weight: 850;
    background: linear-gradient(90deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.progress { height: 9px; border-radius: 999px; background: #202a44; overflow: hidden; margin: 10px 0 2px; }
.progress-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #8b5cf6, #38bdf8); }
.warning-box {
    background: rgba(245,158,11,.08); border: 1px solid rgba(245,158,11,.22);
    border-radius: 16px; padding: 16px 18px; margin-top: 15px;
}
.warning-item { padding: 8px 0; color: #e2e8f0; border-bottom: 1px solid rgba(148,163,184,.10); }
.warning-item:last-child { border-bottom: none; }
.info-card {
    background: rgba(15,23,42,.58); border: 1px solid rgba(148,163,184,.14);
    border-radius: 18px; padding: 20px; height: 100%;
}
.info-card h4 { margin: 0 0 8px; }
.info-card p { color: #aab5ca; font-size: 14px; line-height: 1.6; }
.footer { text-align: center; color: #71809c; padding: 35px 0 12px; font-size: 12px; letter-spacing: .4px; }
div[data-testid="stMetric"] {
    background: rgba(15,23,42,.58); border: 1px solid rgba(148,163,184,.14);
    padding: 16px; border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="logo">🛡️</div>
    <span class="tag">✦ MACHINE LEARNING • NLP • SMS SECURITY</span>
    <h1>SpamGuard AI</h1>
    <p class="subtitle">
        Smart SMS Spam Detection<br>
        Detect suspicious messages, links and scam patterns in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-title">🔍 Analyze Your Message</div>
<div class="helper">Paste an SMS below and let SpamGuard AI check it for spam and suspicious warning signs.</div>
""", unsafe_allow_html=True)
message = st.text_area(
    "Paste your SMS below",
    placeholder="Enter or paste a message here...",
    height=160
)


if st.button("✦ Analyze Message"):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        vector = tfidf.transform([message])
        prediction = model.predict(vector)[0]
        warnings = check_warning_signs(message)
        score, risk_level, category = get_risk_info(prediction, warnings)

        risk_class = "risk-high" if score >= 70 else ("risk-medium" if score >= 40 else "risk-low")
        st.markdown(f"""
        <div class="risk-card {risk_class}">
            <div class="risk-label">🛡️ Risk Assessment</div>
            <div class="risk-value">{risk_level}</div>
            <div style="color:#aab5ca;margin-top:6px;">
                Category: <strong style="color:#e2e8f0;">{category}</strong>
            </div>
            <div class="score-number">{score}<span style="font-size:18px;color:#94a3b8;"> / 100</span></div>
            <div class="progress">
                <div class="progress-fill" style="width:{score}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if prediction == "spam":
            st.error("🚨 Spam Detected!")

            st.write(
                "Our AI classified this message as spam. "
                "Avoid clicking suspicious links or sharing sensitive information."
            )

            if warnings:
                st.markdown("""
                <div class="warning-box">
                    <strong>⚠️ Warning Signs Found</strong>
                """, unsafe_allow_html=True)

                for warning in warnings:
                    st.markdown(
                        f'<div class="warning-item">• {warning}</div>',
                        unsafe_allow_html=True
                    )

                st.markdown("</div>", unsafe_allow_html=True)

        elif warnings:
            st.warning("⚠️ Potential Spam Detected!")

            st.write(
                "The ML model classified this message as normal, "
                "but additional safety checks found warning signs."
            )

            st.markdown("""
            <div class="warning-box">
                <strong>⚠️ Safety Checks</strong>
            """, unsafe_allow_html=True)

            for warning in warnings:
                st.markdown(
                    f'<div class="warning-item">• {warning}</div>',
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.success("✓ No Spam Detected")

            st.write(
                "No obvious spam patterns were detected. "
                "This does not guarantee the message is safe."
            )
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
    🛡️ SPAMGUARD AI • BUILT WITH PYTHON, STREAMLIT & MACHINE LEARNING
    <br>Stay alert. Think before you click.
</div>
""", unsafe_allow_html=True)

