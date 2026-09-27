
import streamlit as st
import joblib

model = joblib.load("spam_model.pkl")
tfidf = joblib.load("tfidf.pkl")

st.title("Spam SMS Detector")
st.write("Check whether a message is spam or normal.")

message = st.text_area("Enter your message")

if st.button("Check Message"):
    if message.strip():
        message_vector = tfidf.transform([message])
        prediction = model.predict(message_vector)[0]

        if prediction == "spam":
            st.error("Spam message detected!")
        else:
            st.success("Normal message detected!")
    else:
        st.warning("Please enter a message.")
