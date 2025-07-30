from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class MediaFileBase(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    duration: Optional[float] = None
    media_type: str
    project_id: int
    uploaded_by: int
    metadata: Optional[Dict[str, Any]] = None

class MediaFileCreate(MediaFileBase):
    pass

class MediaFileUpdate(BaseModel):
    filename: Optional[str] = None
    original_filename: Optional[str] = None
    duration: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class MediaFileList(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    duration: Optional[float] = None
    media_type: str
    project_id: int
    uploaded_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MediaFileResponse(MediaFileList):
    file_path: str
    metadata: Optional[Dict[str, Any]] = None
    updated_at: Optional[datetime] = None

class VideoSegmentBase(BaseModel):
    media_file_id: int
    start_time: float
    end_time: float
    created_by: int

class VideoSegmentCreate(VideoSegmentBase):
    pass

class VideoSegmentResponse(VideoSegmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True