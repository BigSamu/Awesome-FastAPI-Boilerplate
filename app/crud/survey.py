from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Survey
from app.schemas import SurveyResponse, SurveyCreate, SurveyUpdate


class CRUDSurvey(CRUDBase[Survey, SurveyCreate, SurveyUpdate]):
    # Declare model specific CRUD operation methods.

    def get_one_by_filename(self, db: Session, filename: str) -> Survey:
        return db.query(Survey).filter(Survey.filename == filename).first()


survey = CRUDSurvey(Survey)
