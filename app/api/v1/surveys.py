from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app import crud, models, schemas
from app.api.deps import get_db, get_current_user


router = APIRouter()

@router.get("", response_model=List[schemas.PostResponse])
def read_all_surveys(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve all surveys.
    """
    surveys = crud.survey.get_all(db)
    return surveys

@router.get("/{survey_id}", response_model=schemas.PostResponse)
def read_one_survey(survey_id:int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Retrieve one survey by id.
    """
    survey = crud.survey.get_one(db, model_id=survey_id)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The survey with id '{survey_id}' does not exist in the system.",
        )
    return survey

@router.post("", response_model=schemas.PostResponse)
def create_survey(*, db: Session = Depends(get_db), survey_in: schemas.PostCreate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Create new survey.
    """
    survey = crud.survey.create(db, obj_in=survey_in)
    return survey

@router.put("/{survey_id}", response_model=schemas.PostResponse)
def update_survey(*, survey_id: int, db: Session = Depends(get_db), survey_in: schemas.PostUpdate, current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Update existing survey.
    """
    survey = crud.survey.get_one(db, model_id=survey_id)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The survey with id '{survey_id}' does not exist in the system.",
        )
    survey = crud.survey.update(db, db_obj=survey, obj_in=survey_in)
    return survey

@router.delete("", response_model=schemas.Message)
def delete_all_surveys(*, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete all surveys.
    """
    surveys = crud.survey.get_all(db)
    if not surveys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"It doesn't exist any survey in the system.",
        )
    rows_deleted=crud.survey.remove_all(db)
    return {"message": f"{rows_deleted} surveys were deleted."}


@router.delete("/{survey_id}", response_model=schemas.Message)
def delete_one_survey(*, survey_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)) -> Any:
    """
    Delete one survey by id.
    """
    survey = crud.survey.get_one(db, model_id=survey_id)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The survey with id '{survey_id}' does not exist in the system.",
        )
    crud.survey.remove_one(db, model_id=survey.id)
    return {"message": f"Post with id '{survey_id}' deleted."}
