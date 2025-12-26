import json
import time
from uuid import uuid4

import redis

from .. import settings

db = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


async def model_predict(image_name):
    print(f"Processing image {image_name}...")

    prediction = None
    score = None

    # Assign unique job ID
    job_id = str(uuid4())

    # Create job payload
    job_data = {
        "id": job_id,
        "image_name": image_name,
    }

    # Send job to Redis queue
    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    # Wait for model response
    while True:
        output = db.get(job_id)

        if output is not None:
            output = json.loads(output.decode("utf-8"))
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        time.sleep(settings.API_SLEEP)

    return prediction, score
