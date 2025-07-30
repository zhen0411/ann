from celery import shared_task
from app.core.celery_app import celery_app
from app.core.database import SessionLocal, Annotation, MediaFile, Project, Label
from sqlalchemy import func
import json
from datetime import datetime

@shared_task
def export_annotations(project_id: int, format: str = "json"):
    """导出项目标注数据"""
    db = SessionLocal()
    try:
        # 获取项目信息
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"error": "项目不存在"}
        
        # 获取项目下的所有标注
        annotations = db.query(Annotation).join(MediaFile).filter(
            MediaFile.project_id == project_id
        ).all()
        
        # 获取标签信息
        labels = db.query(Label).filter(Label.project_id == project_id).all()
        label_map = {label.id: label for label in labels}
        
        # 格式化标注数据
        export_data = {
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description
            },
            "export_time": datetime.utcnow().isoformat(),
            "format": format,
            "annotations": []
        }
        
        for annotation in annotations:
            label_info = None
            if annotation.label_id and annotation.label_id in label_map:
                label = label_map[annotation.label_id]
                label_info = {
                    "id": label.id,
                    "name": label.name,
                    "color": label.color
                }
            
            annotation_data = {
                "id": annotation.id,
                "media_file_id": annotation.media_file_id,
                "annotation_type": annotation.annotation_type,
                "data": annotation.data,
                "start_time": annotation.start_time,
                "end_time": annotation.end_time,
                "confidence": annotation.confidence,
                "status": annotation.status,
                "label": label_info,
                "created_at": annotation.created_at.isoformat(),
                "updated_at": annotation.updated_at.isoformat() if annotation.updated_at else None
            }
            export_data["annotations"].append(annotation_data)
        
        return {
            "success": True,
            "project_id": project_id,
            "annotation_count": len(export_data["annotations"]),
            "data": export_data
        }
        
    finally:
        db.close()

@shared_task
def generate_annotation_statistics(project_id: int):
    """生成标注统计信息"""
    db = SessionLocal()
    try:
        # 获取项目信息
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return {"error": "项目不存在"}
        
        # 统计标注数量
        total_annotations = db.query(func.count(Annotation.id)).join(MediaFile).filter(
            MediaFile.project_id == project_id
        ).scalar()
        
        # 按状态统计
        status_stats = db.query(
            Annotation.status,
            func.count(Annotation.id)
        ).join(MediaFile).filter(
            MediaFile.project_id == project_id
        ).group_by(Annotation.status).all()
        
        # 按标注类型统计
        type_stats = db.query(
            Annotation.annotation_type,
            func.count(Annotation.id)
        ).join(MediaFile).filter(
            MediaFile.project_id == project_id
        ).group_by(Annotation.annotation_type).all()
        
        # 按标签统计
        label_stats = db.query(
            Annotation.label_id,
            func.count(Annotation.id)
        ).join(MediaFile).filter(
            MediaFile.project_id == project_id,
            Annotation.label_id.isnot(None)
        ).group_by(Annotation.label_id).all()
        
        # 获取标签信息
        labels = db.query(Label).filter(Label.project_id == project_id).all()
        label_map = {label.id: label for label in labels}
        
        # 格式化统计结果
        statistics = {
            "project_id": project_id,
            "total_annotations": total_annotations,
            "status_distribution": {
                status: count for status, count in status_stats
            },
            "type_distribution": {
                annotation_type: count for annotation_type, count in type_stats
            },
            "label_distribution": {
                label_map[label_id].name if label_id in label_map else f"Label_{label_id}": count
                for label_id, count in label_stats
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        return {
            "success": True,
            "statistics": statistics
        }
        
    finally:
        db.close()

@shared_task
def batch_review_annotations(project_id: int, status: str, comment: str = None):
    """批量审阅标注"""
    db = SessionLocal()
    try:
        # 获取项目下所有待审阅的标注
        annotations = db.query(Annotation).join(MediaFile).filter(
            MediaFile.project_id == project_id,
            Annotation.status == "pending"
        ).all()
        
        updated_count = 0
        for annotation in annotations:
            annotation.status = status
            annotation.review_comment = comment
            annotation.updated_at = datetime.utcnow()
            updated_count += 1
        
        db.commit()
        
        return {
            "success": True,
            "project_id": project_id,
            "updated_count": updated_count,
            "new_status": status
        }
        
    except Exception as e:
        db.rollback()
        return {"error": f"批量审阅失败: {str(e)}"}
    finally:
        db.close()

@shared_task
def cleanup_old_annotations(days: int = 30):
    """清理旧的标注数据"""
    db = SessionLocal()
    try:
        from datetime import timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # 删除指定日期之前的标注
        deleted_count = db.query(Annotation).filter(
            Annotation.created_at < cutoff_date,
            Annotation.status.in_(["rejected", "deleted"])
        ).delete()
        
        db.commit()
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }
        
    except Exception as e:
        db.rollback()
        return {"error": f"清理失败: {str(e)}"}
    finally:
        db.close()