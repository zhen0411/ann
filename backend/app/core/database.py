from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from app.core.config import settings
import enum
import os

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 用户角色枚举
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    PROJECT_MANAGER = "project_manager"
    ANNOTATOR = "annotator"
    REVIEWER = "reviewer"

# 标注类型枚举
class AnnotationType(str, enum.Enum):
    RECTANGLE = "rectangle"
    POLYGON = "polygon"
    POINT = "point"
    LINE = "line"
    TEXT = "text"
    AUDIO_SEGMENT = "audio_segment"

# 媒体类型枚举
class MediaType(str, enum.Enum):
    VIDEO = "video"
    AUDIO = "audio"

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.ANNOTATOR)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    projects = relationship("Project", back_populates="owner")
    annotations = relationship("Annotation", back_populates="annotator")

# 项目模型
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    owner = relationship("User", back_populates="projects")
    media_files = relationship("MediaFile", back_populates="project")
    labels = relationship("Label", back_populates="project")
    project_users = relationship("ProjectUser", back_populates="project")

# 项目用户关联模型
class ProjectUser(Base):
    __tablename__ = "project_users"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(20), default=UserRole.ANNOTATOR)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 标签模型
class Label(Base):
    __tablename__ = "labels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    color = Column(String(7), default="#FF0000")  # HEX颜色
    project_id = Column(Integer, ForeignKey("projects.id"))
    parent_id = Column(Integer, ForeignKey("labels.id"), nullable=True)
    attributes = Column(JSON)  # 标签属性配置
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    project = relationship("Project", back_populates="labels")
    parent = relationship("Label", remote_side=[id])
    children = relationship("Label")

# 媒体文件模型
class MediaFile(Base):
    __tablename__ = "media_files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    duration = Column(Float)  # 视频/音频时长（秒）
    media_type = Column(String(10), nullable=False)  # video/audio
    project_id = Column(Integer, ForeignKey("projects.id"))
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    metadata = Column(JSON)  # 媒体文件元数据
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    project = relationship("Project", back_populates="media_files")
    annotations = relationship("Annotation", back_populates="media_file")

# 标注模型
class Annotation(Base):
    __tablename__ = "annotations"
    
    id = Column(Integer, primary_key=True, index=True)
    media_file_id = Column(Integer, ForeignKey("media_files.id"))
    annotator_id = Column(Integer, ForeignKey("users.id"))
    label_id = Column(Integer, ForeignKey("labels.id"))
    annotation_type = Column(String(20), nullable=False)
    data = Column(JSON, nullable=False)  # 标注数据（坐标、时间等）
    start_time = Column(Float)  # 开始时间（秒）
    end_time = Column(Float)  # 结束时间（秒）
    confidence = Column(Float, default=1.0)  # 置信度
    status = Column(String(20), default="pending")  # pending, approved, rejected
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    media_file = relationship("MediaFile", back_populates="annotations")
    annotator = relationship("User", foreign_keys=[annotator_id], back_populates="annotations")
    label = relationship("Label")
    reviewer = relationship("User", foreign_keys=[reviewer_id])

# 视频片段模型
class VideoSegment(Base):
    __tablename__ = "video_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    media_file_id = Column(Integer, ForeignKey("media_files.id"))
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()