from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
import os
import uuid
from datetime import datetime

from app.core.database import get_db, User, MediaFile, Project, ProjectUser, MediaType
from app.core.security import get_current_user
from app.core.config import settings
from app.schemas.media import MediaFileCreate, MediaFileResponse, MediaFileList
from app.services.minio_service import MinioService
from app.services.media_service import MediaService

router = APIRouter()

@router.post("/upload", response_model=MediaFileResponse)
async def upload_media_file(
    file: UploadFile = File(...),
    project_id: int = Query(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """上传媒体文件"""
    # 检查项目权限
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 检查用户是否有权限上传到该项目
    if current_user.role != "admin" and project.owner_id != current_user.id:
        project_user = db.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == current_user.id
        ).first()
        if not project_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权上传文件到该项目"
            )
    
    # 检查文件类型
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension in settings.ALLOWED_VIDEO_EXTENSIONS:
        media_type = MediaType.VIDEO
    elif file_extension in settings.ALLOWED_AUDIO_EXTENSIONS:
        media_type = MediaType.AUDIO
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的文件类型"
        )
    
    # 检查文件大小
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件大小超过限制"
        )
    
    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    # 上传到MinIO
    minio_service = MinioService()
    file_path = f"projects/{project_id}/{unique_filename}"
    
    try:
        minio_service.upload_file(file.file, file_path, file.content_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )
    
    # 获取媒体文件信息
    media_service = MediaService()
    try:
        duration, metadata = media_service.get_media_info(file_path)
    except Exception as e:
        # 如果获取信息失败，设置默认值
        duration = 0
        metadata = {}
    
    # 保存到数据库
    db_media_file = MediaFile(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file.size,
        duration=duration,
        media_type=media_type.value,
        project_id=project_id,
        uploaded_by=current_user.id,
        metadata=metadata
    )
    
    db.add(db_media_file)
    db.commit()
    db.refresh(db_media_file)
    
    return db_media_file

@router.get("/", response_model=List[MediaFileList])
async def get_media_files(
    project_id: Optional[int] = Query(None),
    media_type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取媒体文件列表"""
    query = db.query(MediaFile)
    
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
        
        query = query.filter(MediaFile.project_id == project_id)
    else:
        # 获取用户有权限的项目
        if current_user.role != "admin":
            project_ids = db.query(ProjectUser.project_id).filter(
                ProjectUser.user_id == current_user.id
            ).subquery()
            query = query.filter(MediaFile.project_id.in_(project_ids))
    
    # 根据媒体类型过滤
    if media_type:
        query = query.filter(MediaFile.media_type == media_type)
    
    media_files = query.offset(skip).limit(limit).all()
    return media_files

@router.get("/{media_id}", response_model=MediaFileResponse)
async def get_media_file(
    media_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取媒体文件详情"""
    media_file = db.query(MediaFile).filter(MediaFile.id == media_id).first()
    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="媒体文件不存在"
        )
    
    # 检查权限
    project = db.query(Project).filter(Project.id == media_file.project_id).first()
    if current_user.role != "admin" and project.owner_id != current_user.id:
        project_user = db.query(ProjectUser).filter(
            ProjectUser.project_id == media_file.project_id,
            ProjectUser.user_id == current_user.id
        ).first()
        if not project_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问该文件"
            )
    
    return media_file

@router.delete("/{media_id}")
async def delete_media_file(
    media_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """删除媒体文件"""
    media_file = db.query(MediaFile).filter(MediaFile.id == media_id).first()
    if not media_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="媒体文件不存在"
        )
    
    # 检查权限
    project = db.query(Project).filter(Project.id == media_file.project_id).first()
    if current_user.role != "admin" and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除该文件"
        )
    
    # 从MinIO删除文件
    minio_service = MinioService()
    try:
        minio_service.delete_file(media_file.file_path)
    except Exception as e:
        # 记录错误但不阻止删除数据库记录
        print(f"删除MinIO文件失败: {str(e)}")
    
    # 删除数据库记录
    db.delete(media_file)
    db.commit()
    
    return {"message": "文件删除成功"}