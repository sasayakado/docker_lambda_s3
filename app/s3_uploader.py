import boto3
import os

class S3Uploader:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_log(self, tmp_log_file, s3_log_key):
        """
        ログファイルをS3にアップロード。
        
        Parameters:
        - tmp_log_file (str): アップロードする一時的なログファイルのパス。
        - s3_log_key (str): S3に保存するログファイルのキー。

        Returns:
        None
        """
        if os.path.exists(tmp_log_file):
            with open(tmp_log_file, 'r') as f:
                content = f.read()
                print(content)

            self.s3.upload_file(Filename=tmp_log_file, Bucket=self.bucket_name, Key=s3_log_key)
            os.remove(tmp_log_file)
