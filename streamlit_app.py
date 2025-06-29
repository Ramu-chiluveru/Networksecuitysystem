import streamlit as st
import pandas as pd
import os
import csv

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from parseFeatures import ParseFeatures

# Paths
HISTORY_FILE = "prediction_history.csv"
PREPROCESSOR_PATH = "final_model/preprocessor.pkl"
MODEL_PATH = "final_model/model.pkl"

# Save prediction to history
def save_to_history(url, prediction):
    with open(HISTORY_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([url, "Safe" if prediction == 0 else "Unsafe"])

# Load history
def load_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE, names=["URL", "Prediction"])
    return pd.DataFrame(columns=["URL", "Prediction"])

# App UI
st.set_page_config(page_title="URL Safety Predictor", layout="centered")
st.title("🔍 URL Safety Prediction")
st.markdown("This app checks if a given URL is **safe or unsafe** based on machine learning.")

url = st.text_input("Enter a URL to test:", placeholder="https://example.com")

if st.button("Predict"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        try:
            # Extract features
            st.info("Extracting features...")
            features = ParseFeatures(url).extract_all()

            print(f"extract features: ",features)

            column_names = [
                "having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", 
                "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State",
                "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", 
                "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", 
                "Redirect", "on_mouseover", "RightClick", "popUpWidnow", "Iframe", 
                "age_of_domain", "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", 
                "Links_pointing_to_page", "Statistical_report"
            ]

            df = pd.DataFrame([features], columns=column_names)
            print(f"df: {df}")

            # Load model
            st.info("Loading model...")
            preprocessor = load_object(PREPROCESSOR_PATH)
            model = load_object(MODEL_PATH)
            network_model = NetworkModel(preprocessor=preprocessor, model=model)

            # Predict
            st.info("Predicting...")
            y_pred = network_model.predict(df)
            prediction = "Safe" if y_pred[0] == 0 else "Unsafe / Phishing url"
            st.success(f"Prediction: {prediction}")

            # Save to history
            save_to_history(url, y_pred[0])

        except Exception as e:
            st.error(f"Error: {e}")

# Show past predictions
st.markdown("---")
st.subheader("📈 Previous Predictions")

history = load_history()
if not history.empty:
    st.dataframe(history)
else:
    st.info("No predictions made yet.")
