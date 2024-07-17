from sensor.configuration.mongodb_connection import MongoDBClient
from sensor.exception import SensorException
import os, sys
from sensor.logger import logging
from sensor.pipline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import load_object, read_yaml_file
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.constants.training_pipeline import SAVED_MODEL_DIR

from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.responses import Response
from uvicorn import run as app_run
import pandas as pd

from sensor.constants.application import APP_HOST, APP_PORT

app = FastAPI()

origins = ["*"]
# Cross-Origin Resource Sharing (CORS) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        training_pipeline = TrainPipeline()
        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        training_pipeline.run_pipeline()
        return Response("Training successfully completed!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict():
    try:
        # get data and from the csv file 
        # convert it into dataframe 
        df = None
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping, inplace=True)
        # get the prediction output as you want 
        return Response(df.to_json())
    except Exception as e:
        raise SensorException(e, sys)

def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__ == "__main__":
    # Uncomment and modify the following lines if needed for database operations
    # file_path="/Users/myhome/Downloads/sensorlive/aps_failure_training_set1.csv"
    # database_name="ineuron"
    # collection_name ="sensor"
    # dump_csv_file_to_mongodb_collection(file_path,database_name,collection_name)
    app_run(app, host=APP_HOST, port=APP_PORT)
