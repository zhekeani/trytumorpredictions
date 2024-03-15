from fastapi import APIRouter, HTTPException, UploadFile, Depends
from typing import Annotated
from ..dependencies.auth import get_auth_token_header
from ..services.predictions import PredictionsService

router = APIRouter(
    prefix="/predictions",
    tags=["predictions"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_auth_token_header)],
)


@router.post("/single")
async def create_single_prediction(
    predictionsService: Annotated[PredictionsService, Depends(PredictionsService)],
    image_file: UploadFile | None = None,
):
    if not image_file:
        return {"message": "No upload file sent"}

    prediction_result = await predictionsService.create_prediction(image_file)

    return prediction_result


@router.post("/multiple")
async def create_multiple_predictions(image_files: list[UploadFile]):
    if image_files is None or not image_files:
        return {"message": "No upload files sent"}
    else:
        return {"filenames": [image_file.filename for image_file in image_files]}
