from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.core.database import AnnotationType

class AnnotationBase(BaseModel):
    media_file_id: int
    label_id: Optional[int] = None
    annotation_type: AnnotationType
    data: Dict[str, Any]
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    confidence: Optional[float] = 1.0

class AnnotationCreate(AnnotationBase):
    pass

class AnnotationUpdate(BaseModel):
    label_id: Optional[int] = None
    annotation_type: Optional[AnnotationType] = None
    data: Optional[Dict[str, Any]] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    confidence: Optional[float] = None

class AnnotationList(BaseModel):
    id: int
    media_file_id: int
    annotator_id: int
    label_id: Optional[int] = None
    annotation_type: str
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    confidence: Optional[float] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AnnotationResponse(AnnotationList):
    data: Dict[str, Any]
    reviewer_id: Optional[int] = None
    review_comment: Optional[str] = None
    updated_at: Optional[datetime] = None

class VideoSegmentBase(BaseModel):
    media_file_id: int
    start_time: float
    end_time: float
    created_by: int

class VideoSegmentCreate(VideoSegmentBase):
    pass

class VideoSegmentResponse(VideoSegmentResponse):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True