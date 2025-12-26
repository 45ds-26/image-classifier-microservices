import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image

db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
)


model = ResNet50(weights="imagenet")


def predict(image_name):
    image_path = os.path.join(settings.UPLOAD_FOLDER, image_name)

    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    _, class_name, pred_probability = decode_predictions(preds, top=1)[0][0]
    pred_probability = float(round(pred_probability, 4))

    return class_name, pred_probability


def classify_process():
    while True:
        _, job_data = db.brpop(settings.REDIS_QUEUE)
        job = json.loads(job_data.decode("utf-8"))

        job_id = job["id"]
        image_name = job["image_name"]

        prediction, score = predict(image_name)

        output = {"prediction": prediction, "score": score}
        db.set(job_id, json.dumps(output))

        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()
