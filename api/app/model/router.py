import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.auth.jwt import get_current_user
from app.model.schema import PredictResponse
from app.model.services import model_predict
import app.utils as utils  # IMPORTANTE

router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict", response_model=PredictResponse)
async def predict(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    response = {
        "success": False,
        "prediction": None,
        "score": None,
        "image_file_name": None,
    }

    # 1. Validate file
    if not file or not utils.allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type is not supported.",
        )

    # 2. Generate hashed filename
    new_filename = await utils.get_file_hash(file)
    file_path = os.path.join("uploads", new_filename)

    # 3. Save file if it does not exist
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(await file.read())

    # 4. Call ML service
    prediction, score = await model_predict(new_filename)

    # 5. Build response
    response["success"] = True
    response["prediction"] = prediction
    response["score"] = score
    response["image_file_name"] = new_filename

    return response
