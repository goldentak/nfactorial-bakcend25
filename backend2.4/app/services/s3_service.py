import boto3
import uuid
from app.config import settings

class S3Service:
    def __init__(self):
        if not all([settings.aws_access_key_id, settings.aws_secret_access_key, settings.aws_region]):
            raise Exception("AWS credentials not properly configured")
            
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
    
    async def upload_audio_file(self, file_content: bytes, filename: str = None) -> str:
        try:
            if not filename:
                filename = f"audio/{uuid.uuid4()}.mp3"
            
            self.s3_client.put_object(
                Bucket=settings.aws_bucket_name,
                Key=filename,
                Body=file_content,
                ContentType='audio/mpeg'
            )
            
            url = f"https://{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{filename}"
            return url
            
        except Exception as e:
            raise Exception(f"S3 upload error: {str(e)}")