import mlflow
import mlflow.pyfunc
from ultralytics import YOLO
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("yolov8-object-detection")

with mlflow.start_run(run_name="model-registration-v1"):
    # Model parametrelerini kaydet
    mlflow.log_param("model_type", "yolov8n")
    mlflow.log_param("dataset", "COCO")
    mlflow.log_param("input_size", 640)
    
    # Model dosyasını artifact olarak kaydet
    mlflow.log_artifact("yolov8n.pt", artifact_path="model")
    
    mlflow.set_tag("mlflow.runName", "yolov8n-production-v1")
    mlflow.set_tag("stage", "production")
    
    print("✅ Model başarıyla MLflow'a kaydedildi!")