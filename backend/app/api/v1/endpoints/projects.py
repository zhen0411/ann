from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app.core.database import get_db, User, Project, ProjectUser, UserRole
from app.core.security import get_current_user, check_user_permission
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectList
from app.schemas.user import UserResponse

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """创建新项目"""
    if not check_user_permission(current_user, UserRole.PROJECT_MANAGER):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要项目管理员权限"
        )
    
    # 创建项目
    db_project = Project(
        name=project_in.name,
        description=project_in.description,
        owner_id=current_user.id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project

@router.get("/", response_model=List[ProjectList])
async def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取项目列表"""
    # 根据用户角色获取项目
    if current_user.role == UserRole.ADMIN:
        projects = db.query(Project).offset(skip).limit(limit).all()
    else:
        # 获取用户参与的项目
        project_ids = db.query(ProjectUser.project_id).filter(
            ProjectUser.user_id == current_user.id
        ).subquery()
        projects = db.query(Project).filter(
            Project.id.in_(project_ids)
        ).offset(skip).limit(limit).all()
    
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """获取项目详情"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 检查用户权限
    if current_user.role != UserRole.ADMIN and project.owner_id != current_user.id:
        # 检查用户是否参与该项目
        project_user = db.query(ProjectUser).filter(
            ProjectUser.project_id == project_id,
            ProjectUser.user_id == current_user.id
        ).first()
        if not project_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问该项目"
            )
    
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """更新项目信息"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 检查权限
    if current_user.role != UserRole.ADMIN and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改该项目"
        )
    
    # 更新项目
    for field, value in project_in.dict(exclude_unset=True).items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """删除项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 检查权限
    if current_user.role != UserRole.ADMIN and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除该项目"
        )
    
    # 删除项目（这里应该先删除相关数据）
    db.delete(project)
    db.commit()
    
    return {"message": "项目删除成功"}

@router.post("/{project_id}/users/{user_id}")
async def add_user_to_project(
    project_id: int,
    user_id: int,
    role: UserRole = UserRole.ANNOTATOR,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Any:
    """添加用户到项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 检查权限
    if current_user.role != UserRole.ADMIN and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权管理该项目用户"
        )
    
    # 检查用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查是否已经添加
    existing = db.query(ProjectUser).filter(
        ProjectUser.project_id == project_id,
        ProjectUser.user_id == user_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已在该项目中"
        )
    
    # 添加用户到项目
    project_user = ProjectUser(
        project_id=project_id,
        user_id=user_id,
        role=role
    )
    db.add(project_user)
    db.commit()
    
    return {"message": "用户添加成功"}