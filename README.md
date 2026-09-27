
# 🛡️ SpamGuard AI
### AI-Powered SMS Spam Detection

SpamGuard AI is a machine learning web application that classifies SMS messages as spam or normal. It also includes additional safety checks to flag potentially suspicious messages that the AI model might miss.
## 🌐 Live Demo

[🚀 Launch SpamGuard AI](https://spam-sms-detector-jyqnmsujuuwhwgiw3vuzw7.streamlit.app/)
## 🚀 Features

- Instant SMS spam detection
- Additional safety checks for suspicious prizes, links and urgent requests
- Three clear results:
  - 🚨 Spam Detected
  - ⚠️ Potential Spam Detected
  - ✅ No Spam Detected
- Modern, responsive Streamlit interface
- Simple and easy to use

## 🧠 Machine Learning

**Dataset:** SMS Spam Collection (5,572 messages)

**Text Processing:** TF-IDF Vectorization

**Models Trained:**
- Multinomial Naive Bayes
- Linear Support Vector Machine (SVM)

**Selected Model:** Linear SVM

**Test Accuracy:** 98.39%

The accuracy is measured on the held-out test dataset. Predictions are not guaranteed to be correct for every real-world message.

## 🛠️ Technologies Used

- Python
- Pandas
- Scikit-learn
- TF-IDF
- Linear SVM
- Streamlit
- Joblib
- Google Colab
- GitHub

## ⚙️ How It Works

1. The user enters an SMS message.
2. TF-IDF converts the text into numerical features.
3. The trained Linear SVM predicts spam or normal.
4. Additional safety checks look for suspicious patterns.
5. The application displays the appropriate result.

## 📂 Project Files

| File | Description |
|------|-------------|
| `app.py` | Streamlit web application |
| `spam_model.pkl` | Trained Linear SVM model |
| `tfidf.pkl` | Saved TF-IDF vectorizer |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |

## 💻 Run Locally

Clone the repository:

```bash
git clone https://github.com/Mudassira10/Spam-sms-detector.git
cd Spam-sms-detector
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

## 🧪 Example Tests

| Message | Result |
|---------|--------|
| Unexpected laptop prize with "click here" | Potential Spam Detected |
| Normal delivery update | No Spam Detected |
| Urgent $5,000 cash reward message | Spam Detected |

These are manual examples, not a comprehensive evaluation of the combined system.

## ⚠️ Disclaimer

SpamGuard AI is an educational machine learning project. A "No Spam Detected" result does not guarantee that a message is safe. Always verify unexpected messages, links and offers.

## 👩‍💻 Developed By

**Mudassira**

GitHub: [Mudassira10](https://github.com/Mudassira10)

