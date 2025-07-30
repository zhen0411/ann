from celery import shared_task
from app.core.celery_app import celery_app
from app.services.media_service import MediaService
from app.services.minio_service import MinioService
from app.core.database import SessionLocal, MediaFile
import os

@shared_task
def process_media_file(media_file_id: int):
    """处理媒体文件（获取信息、提取帧等）"""
    db = SessionLocal()
    try:
        media_file = db.query(MediaFile).filter(MediaFile.id == media_file_id).first()
        if not media_file:
            return {"error": "媒体文件不存在"}
        
        media_service = MediaService()
        
        # 获取媒体信息
        try:
            duration, metadata = media_service.get_media_info(media_file.file_path)
            
            # 更新数据库中的媒体信息
            media_file.duration = duration
            media_file.metadata = metadata
            db.commit()
            
            return {
                "success": True,
                "media_file_id": media_file_id,
                "duration": duration,
                "metadata": metadata
            }
        except Exception as e:
            return {"error": f"处理媒体文件失败: {str(e)}"}
            
    finally:
        db.close()

@shared_task
def extract_video_frames(media_file_id: int, fps: int = 1):
    """提取视频帧"""
    db = SessionLocal()
    try:
        media_file = db.query(MediaFile).filter(MediaFile.id == media_file_id).first()
        if not media_file:
            return {"error": "媒体文件不存在"}
        
        if media_file.media_type != "video":
            return {"error": "不是视频文件"}
        
        media_service = MediaService()
        
        # 创建临时目录
        temp_dir = f"/tmp/frames_{media_file_id}"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # 提取帧
            frame_files = media_service.extract_frames(media_file.file_path, temp_dir, fps)
            
            # 上传帧到MinIO
            minio_service = MinioService()
            uploaded_frames = []
            
            for frame_file in frame_files:
                frame_name = os.path.basename(frame_file)
                minio_path = f"frames/{media_file_id}/{frame_name}"
                
                with open(frame_file, 'rb') as f:
                    minio_service.upload_file(f, minio_path, "image/jpeg")
                
                uploaded_frames.append(minio_path)
            
            return {
                "success": True,
                "media_file_id": media_file_id,
                "frame_count": len(uploaded_frames),
                "frames": uploaded_frames
            }
            
        finally:
            # 清理临时目录
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                
    finally:
        db.close()

@shared_task
def create_video_segment(media_file_id: int, start_time: float, end_time: float):
    """创建视频片段"""
    db = SessionLocal()
    try:
        media_file = db.query(MediaFile).filter(MediaFile.id == media_file_id).first()
        if not media_file:
            return {"error": "媒体文件不存在"}
        
        if media_file.media_type != "video":
            return {"error": "不是视频文件"}
        
        media_service = MediaService()
        minio_service = MinioService()
        
        # 创建临时输出文件
        temp_output = f"/tmp/segment_{media_file_id}_{start_time}_{end_time}.mp4"
        
        try:
            # 创建视频片段
            success = media_service.create_video_segment(
                media_file.file_path, temp_output, start_time, end_time
            )
            
            if success:
                # 上传到MinIO
                segment_name = f"segments/{media_file_id}/{start_time}_{end_time}.mp4"
                
                with open(temp_output, 'rb') as f:
                    minio_service.upload_file(f, segment_name, "video/mp4")
                
                return {
                    "success": True,
                    "media_file_id": media_file_id,
                    "segment_path": segment_name,
                    "start_time": start_time,
                    "end_time": end_time
                }
            else:
                return {"error": "创建视频片段失败"}
                
        finally:
            # 清理临时文件
            if os.path.exists(temp_output):
                os.unlink(temp_output)
                
    finally:
        db.close()

@shared_task
def extract_audio_waveform(media_file_id: int):
    """提取音频波形数据"""
    db = SessionLocal()
    try:
        media_file = db.query(MediaFile).filter(MediaFile.id == media_file_id).first()
        if not media_file:
            return {"error": "媒体文件不存在"}
        
        if media_file.media_type != "audio":
            return {"error": "不是音频文件"}
        
        media_service = MediaService()
        
        try:
            waveform_data = media_service.extract_audio_waveform(media_file.file_path)
            
            if waveform_data:
                return {
                    "success": True,
                    "media_file_id": media_file_id,
                    "waveform_data": waveform_data
                }
            else:
                return {"error": "提取音频波形失败"}
                
        except Exception as e:
            return {"error": f"提取音频波形失败: {str(e)}"}
            
    finally:
        db.close()