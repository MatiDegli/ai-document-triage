from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisRead
from app.services.analyses import get_analysis_by_id, list_analyses

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.get("", response_model=list[AnalysisRead])
def get_analyses_list(db: Session = Depends(get_db)) -> list[Analysis]:
    return list_analyses(db)


@router.get("/{analysis_id}", response_model=AnalysisRead)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)) -> Analysis:
    analysis = get_analysis_by_id(db, analysis_id)
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
