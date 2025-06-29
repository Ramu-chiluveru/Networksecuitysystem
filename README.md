# 🛡️ PhishScan

**PhishScan** is a real-time phishing URL detection system built using Machine Learning. It extracts 30+ handcrafted features from a given URL and uses a trained ML model to classify it as **Safe** or **Unsafe**.

---

## ⚙️ How It Works

1. **Feature Engineering**  
   The system extracts over 30 features from the input URL including:
   - Presence of IP address  
   - Length of URL  
   - Use of `@`, `//`, `-`, `https`  
   - Number of subdomains  
   - Domain age, and more

2. **Model Training & Selection**  
   - Trained multiple ML models: Random Forest, Gradient Boosting, AdaBoost, Logistic Regression, and Decision Tree  
   - Tuned using GridSearchCV  
   - Best model selected based on accuracy, precision, recall, and F1-score

3. **Prediction Workflow**  
   - URL entered via the Streamlit UI  
   - Features extracted using the `ParseFeatures` class  
   - Passed through the preprocessor and trained ML model  
   - Output: **Safe** ✅ or **Unsafe** ❌

---

## 🚀 Getting Started

### 🧪 Installation

```bash
git clone https://github.com/Ramu-chiluveru/PhishScan.git
cd phishscan
pip install -r requirements.txt

streamlit run streamlit_app.py


```

# folder structure
```
phishscan/
├── final_models/          # Trained models and preprocessor (model.pkl, preprocessor.pkl)
├── networkSecurity/components/         # ML pipeline steps (data_ingestion,data_validation,data_transformation, model_trainer)
├── constant/           # Project-wide constants
├── Network_Data/               # Raw and processed dataset
├── networkSecurity/exception/          # Custom exception handling
├── networkSecurity/logging/            # Logging setup
├── networkSecurity/utils/              # Utility functions
|--networkSecurity/entity # artifact_entity , config_entity
├── streamlit_app.py    # Streamlit-based front-end for URL prediction
├── main.py             # Script for training and saving models
├── app.py              # FastAPI app for batch predictions
└── requirements.txt    # Python dependencies
```
