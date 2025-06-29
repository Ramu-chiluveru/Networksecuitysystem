import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from fastapi.responses import FileResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from parseFeatures import ParseFeatures 

load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL")
print(mongo_db_url)

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e: 
        raise NetworkSecurityException(e,sys)
    
@app.post("/url")
async def url_route(request: Request, url: str):
    print(f"Request received for {url} url")

    features = ParseFeatures(url).extract_all()
    print(f"Features extracted: {features}")

    # Convert to DataFrame and save as CSV for prediction
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

    csv_path = "features.csv"
    df.to_csv(csv_path, index=False)

    # Open the file and create a fake UploadFile-like object
    class DummyFile:
        def __init__(self, file):
            self.file = file

    with open(csv_path, "rb") as f:
        dummy_upload = DummyFile(f)
        return await predict_route(request, dummy_upload)


    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred

        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv('prediction_output/output.csv', index=False)

        table_html = df.to_html(classes='table table-bordered table-hover')

        return templates.TemplateResponse("success.html", {
            "request": request,
            "table": table_html
        })

    except Exception as e:
        raise NetworkSecurityException(e, sys)


@app.get("/download-prediction")
async def download_prediction():
    return FileResponse(path="prediction_output/output.csv", filename="output.csv", media_type='text/csv')

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
