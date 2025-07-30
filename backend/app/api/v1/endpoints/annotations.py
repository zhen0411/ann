from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from datetime import datetime

from app.core.database import get_db, User, Annotation, MediaFile, Label, Project, ProjectUser
from app.core.security import get_current_user
from app.schemas.annotation import (
    AnnotationCreate, AnnotationUpdate, AnnotationResponse, 
    AnnotationList, VideoSegmentCreate, VideoSegmentResponse
)

router = APIRouter()

@router.post("/", response_model=AnnotationResponse)
async def create_annotation(
    annotation_in: AnnotationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """创建标注"""
    # 检查媒体文件是否存在
    media_file = db.query(MediaFile).filter(MediaFile.id == annotation_in.media_file_id).first()
    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="媒体文件不存在"
        )
    
    # 检查用户权限
    project = db.query(Project).filter(Project.id == media_file.project_id).first()
    if current_user.role != "admin" and project.owner_id != current_user.id:
        project_user = db.query(ProjectUser).filter(
            ProjectUser.project_id == media_file.project_id,
            ProjectUser.user_id == current_user.id
        ).first()
        if not project_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权标注该文件"
            )
    
    # 检查标签是否存在
    if annotation_in.label_id:
        label = db.query(Label).filter(Label.id == annotation_in.label_id).first()
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="标签不存在"
            )
    
    # 创建标注
    db_annotation = Annotation(
        media_file_id=annotation_in.media_file_id,
        annotator_id=current_user.id,
        label_id=annotation_in.label_id,
        annotation_type=annotation_in.annotation_type,
        data=annotation_in.data,
        start_time=annotation_in.start_time,
        end_time=annotation_in.end_time,
        confidence=annotation_in.confidence
    )
    
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    
    return db_annotation

@router.get("/", response_model=List[AnnotationList])
async def get_annotations(
    media_file_id: Optional[int] = Query(None),
    project_id: Optional[int] = Query(None),
    annotation_type: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取标注列表"""
    query = db.query(Annotation)
    
    # 根据媒体文件过滤
    if media_file_id:
        # 检查权限
        media_file = db.query(MediaFile).filter(MediaFile.id == media_file_id).first()
        if not media_file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="媒体文件不存在"
            )
        
        if current_user.role != "admin" and media_file.uploaded_by != current_user.id:
            project_user = db.query(ProjectUser).filter(
                ProjectUser.project_id == media_file.project_id,
                ProjectUser.user_id == current_user.id
            ).first()
            if not project_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权访问该文件"
                )
        
        query = query.filter(Annotation.media_file_id == media_file_id)
    
    # 根据项目过滤
    if project_id:
        # 检查项目权限
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="项目不存在"
            )
        
        if current_user.role != "admin" and project.owner_id != current_user.id:
            project_user = db.query(ProjectUser).filter(
                ProjectUser.project_id == project_id,
                ProjectUser.user_id == current_user.id
            ).first()
            if not project_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="无权访问该项目"
                )
        
        # 获取项目下的媒体文件ID
        media_file_ids = db.query(MediaFile.id).filter(MediaFile.project_id == project_id).subquery()
        query = query.filter(Annotation.media_file_id.in_(media_file_ids))
    
    # 根据标注类型过滤
    if annotation_type:
        query = query.filter(Annotation.annotation_type == annotation_type)
    
    # 根据状态过滤
    if status_filter:
        query = query.filter(Annotation.status == status_filter)
    
    # 如果不是管理员，只能看到自己的标注或已审核的标注
    if current_user.role != "admin":
        query = query.filter(
            (Annotation.annotator_id == current_user.id) | 
            (Annotation.status.in_(["approved", "rejected"]))
        )
    
    annotations = query.offset(skip).limit(limit).all()
    return annotations

@router.get("/{annotation_id}", response_model=AnnotationResponse)
async def get_annotation(
    annotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取标注详情"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标注不存在"
        )
    
    # 检查权限
    if current_user.role != "admin" and annotation.annotator_id != current_user.id:
        # 检查是否是审阅员
        media_file = db.query(MediaFile).filter(MediaFile.id == annotation.media_file_id).first()
        project_user = db.query(ProjectUser).filter(
            ProjectUser.project_id == media_file.project_id,
            ProjectUser.user_id == current_user.id
        ).first()
        if not project_user or project_user.role not in ["reviewer", "project_manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问该标注"
            )
    
    return annotation

@router.put("/{annotation_id}", response_model=AnnotationResponse)
async def update_annotation(
    annotation_id: int,
    annotation_in: AnnotationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """更新标注"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标注不存在"
        )
    
    # 检查权限
    if current_user.role != "admin" and annotation.annotator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改该标注"
        )
    
    # 更新标注
    for field, value in annotation_in.dict(exclude_unset=True).items():
        setattr(annotation, field, value)
    
    annotation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(annotation)
    
    return annotation

@router.delete("/{annotation_id}")
async def delete_annotation(
    annotation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """删除标注"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标注不存在"
        )
    
    # 检查权限
    if current_user.role != "admin" and annotation.annotator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除该标注"
        )
    
    db.delete(annotation)
    db.commit()
    
    return {"message": "标注删除成功"}

@router.post("/review/{annotation_id}")
async def review_annotation(
    annotation_id: int,
    status: str,
    comment: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """审阅标注"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标注不存在"
        )
    
    # 检查权限
    media_file = db.query(MediaFile).filter(MediaFile.id == annotation.media_file_id).first()
    project_user = db.query(ProjectUser).filter(
        ProjectUser.project_id == media_file.project_id,
        ProjectUser.user_id == current_user.id
    ).first()
    
    if current_user.role != "admin" and (not project_user or project_user.role not in ["reviewer", "project_manager"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权审阅该标注"
        )
    
    # 更新标注状态
    annotation.status = status
    annotation.reviewer_id = current_user.id
    annotation.review_comment = comment
    annotation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(annotation)
    
    return {"message": "审阅完成"}