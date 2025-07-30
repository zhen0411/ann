from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import io
from typing import Optional

class MinioService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """确保存储桶存在"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"创建存储桶失败: {e}")
    
    def upload_file(self, file_obj, object_name: str, content_type: str = "application/octet-stream"):
        """上传文件到MinIO"""
        try:
            # 读取文件内容
            file_data = file_obj.read()
            file_obj.seek(0)  # 重置文件指针
            
            # 上传文件
            self.client.put_object(
                self.bucket_name,
                object_name,
                io.BytesIO(file_data),
                length=len(file_data),
                content_type=content_type
            )
            return True
        except S3Error as e:
            print(f"上传文件失败: {e}")
            raise e
    
    def download_file(self, object_name: str) -> Optional[bytes]:
        """从MinIO下载文件"""
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return response.read()
        except S3Error as e:
            print(f"下载文件失败: {e}")
            return None
    
    def get_file_url(self, object_name: str, expires: int = 3600) -> Optional[str]:
        """获取文件的预签名URL"""
        try:
            return self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=expires
            )
        except S3Error as e:
            print(f"生成预签名URL失败: {e}")
            return None
    
    def delete_file(self, object_name: str) -> bool:
        """删除文件"""
        try:
            self.client.remove_object(self.bucket_name, object_name)
            return True
        except S3Error as e:
            print(f"删除文件失败: {e}")
            return False
    
    def list_files(self, prefix: str = "", recursive: bool = True) -> list:
        """列出文件"""
        try:
            objects = self.client.list_objects(
                self.bucket_name,
                prefix=prefix,
                recursive=recursive
            )
            return [obj.object_name for obj in objects]
        except S3Error as e:
            print(f"列出文件失败: {e}")
            return []
    
    def file_exists(self, object_name: str) -> bool:
        """检查文件是否存在"""
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False