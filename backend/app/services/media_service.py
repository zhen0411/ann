import ffmpeg
import os
import tempfile
from typing import Tuple, Dict, Any, Optional
from app.core.config import settings
from app.services.minio_service import MinioService

class MediaService:
    def __init__(self):
        self.minio_service = MinioService()
    
    def get_media_info(self, file_path: str) -> Tuple[float, Dict[str, Any]]:
        """获取媒体文件信息"""
        try:
            # 从MinIO下载文件到临时目录
            file_data = self.minio_service.download_file(file_path)
            if not file_data:
                raise Exception("无法下载文件")
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_path)[1]) as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name
            
            try:
                # 使用ffmpeg获取媒体信息
                probe = ffmpeg.probe(temp_file_path)
                
                # 获取时长
                duration = float(probe['format']['duration'])
                
                # 获取视频/音频流信息
                streams = probe.get('streams', [])
                video_stream = next((s for s in streams if s['codec_type'] == 'video'), None)
                audio_stream = next((s for s in streams if s['codec_type'] == 'audio'), None)
                
                metadata = {
                    'format': probe['format']['format_name'],
                    'duration': duration,
                    'size': probe['format']['size'],
                    'bit_rate': probe['format'].get('bit_rate'),
                    'video_stream': video_stream,
                    'audio_stream': audio_stream
                }
                
                return duration, metadata
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            print(f"获取媒体信息失败: {e}")
            raise e
    
    def extract_frames(self, file_path: str, output_dir: str, fps: int = 1) -> list:
        """提取视频帧"""
        try:
            # 从MinIO下载文件
            file_data = self.minio_service.download_file(file_path)
            if not file_data:
                raise Exception("无法下载文件")
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_path)[1]) as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name
            
            try:
                # 确保输出目录存在
                os.makedirs(output_dir, exist_ok=True)
                
                # 使用ffmpeg提取帧
                output_pattern = os.path.join(output_dir, "frame_%04d.jpg")
                
                stream = ffmpeg.input(temp_file_path)
                stream = ffmpeg.filter(stream, 'fps', fps=fps)
                stream = ffmpeg.output(stream, output_pattern, vframes=None)
                ffmpeg.run(stream, overwrite_output=True)
                
                # 返回生成的帧文件列表
                frame_files = []
                for filename in os.listdir(output_dir):
                    if filename.startswith("frame_") and filename.endswith(".jpg"):
                        frame_files.append(os.path.join(output_dir, filename))
                
                return sorted(frame_files)
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            print(f"提取视频帧失败: {e}")
            raise e
    
    def create_video_segment(self, input_path: str, output_path: str, start_time: float, end_time: float) -> bool:
        """创建视频片段"""
        try:
            # 从MinIO下载文件
            file_data = self.minio_service.download_file(input_path)
            if not file_data:
                raise Exception("无法下载文件")
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_path)[1]) as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name
            
            try:
                # 使用ffmpeg剪切视频
                duration = end_time - start_time
                
                stream = ffmpeg.input(temp_file_path, ss=start_time, t=duration)
                stream = ffmpeg.output(stream, output_path, acodec='copy', vcodec='copy')
                ffmpeg.run(stream, overwrite_output=True)
                
                return True
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            print(f"创建视频片段失败: {e}")
            return False
    
    def extract_audio_waveform(self, file_path: str) -> Optional[Dict[str, Any]]:
        """提取音频波形数据"""
        try:
            # 从MinIO下载文件
            file_data = self.minio_service.download_file(file_path)
            if not file_data:
                raise Exception("无法下载文件")
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_path)[1]) as temp_file:
                temp_file.write(file_data)
                temp_file_path = temp_file.name
            
            try:
                # 使用ffmpeg提取音频信息
                probe = ffmpeg.probe(temp_file_path)
                
                # 获取音频流信息
                audio_stream = next((s for s in probe.get('streams', []) if s['codec_type'] == 'audio'), None)
                if not audio_stream:
                    raise Exception("未找到音频流")
                
                # 提取音频数据用于波形分析
                # 这里可以添加更复杂的音频分析逻辑
                
                waveform_data = {
                    'sample_rate': int(audio_stream.get('sample_rate', 44100)),
                    'channels': int(audio_stream.get('channels', 2)),
                    'duration': float(probe['format']['duration']),
                    'bit_rate': audio_stream.get('bit_rate'),
                    'codec': audio_stream.get('codec_name')
                }
                
                return waveform_data
                
            finally:
                # 清理临时文件
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            print(f"提取音频波形失败: {e}")
            return None