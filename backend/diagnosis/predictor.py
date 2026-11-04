from django.test import TestCase
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import os

# --------------------------------
# Paths to both models and classes
# --------------------------------
MODEL_DIR = os.path.join(settings.BASE_DIR, "ml_models")  # Absolute path

MODELS = {
    "best": {
        "model_path": os.path.join(MODEL_DIR, "plant_disease_best.keras"),
        "class_path": os.path.join(MODEL_DIR, "class_names.json"),
        "disease_info_path":os.path.join(MODEL_DIR, "disease_info.json"),
}
}

# --------------------------------
# Load models and class names once
# --------------------------------
loaded_models = {}
loaded_classes = {}
disease_infos = {}

for key, paths in MODELS.items():
    # Load Keras model
    loaded_models[key] =tf.keras.models.load_model(paths["model_path"])
    # Load class names
    with open(paths["class_path"], "r") as f:
        loaded_classes[key] = json.load(f)
    with open(paths["disease_info_path"], "r") as f:
        disease_infos[key] = json.load(f)
IMG_SIZE = (128,128 )  # must match what you used during training

def predict_disease(img_path, model_choice="best"):
    """
    Predicts disease using the chosen model.
    model_choice can be 'best' or 'final'.
    """
    model = loaded_models.get(model_choice)
    class_names = loaded_classes.get(model_choice)

    if model is None or class_names is None:
        raise ValueError("Invalid model choice")

    img = load_img(img_path, target_size=IMG_SIZE)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)   # normalize
    img_array = preprocess_input(img_array)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = np.max(predictions)

    return class_names[str(predicted_class)], float(confidence)

# --------------------------------
# API Endpoint
# --------------------------------
@csrf_exempt
def detect_disease(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        model_choice = request.POST.get('model', 'best')
        print("DEBUG - Model choice received:", model_choice)  # <-- DEBUG
        print("DEBUG - Files received:", request.FILES)   # defaults to 'best'

        # Save temporarily to MEDIA_ROOT
        saved_file_path = default_storage.save(uploaded_file.name, uploaded_file)
        absolute_path = os.path.join(settings.MEDIA_ROOT, saved_file_path)

        try:
            # Run prediction
            disease_name, confidence = predict_disease(absolute_path, model_choice=model_choice)
            extra_info = disease_infos.get(model_choice, {}).get(disease_name, {
                "fertilizers": [],
                "remedies": []
            })    
            # Clean up the file after prediction
            if os.path.exists(absolute_path):
                os.remove(absolute_path)
            
            return JsonResponse({
                "disease": disease_name,
                "confidence": f"{confidence*100:.2f}%",
                "fertilizers": extra_info.get("fertilizers", []),
                "remedies": extra_info.get("remedies", []),
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Please upload an image"}, status=400)
