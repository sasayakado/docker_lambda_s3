import os
import traceback
from s3_uploader import S3Uploader
from log_manager import LogManager

BUCKET_NAME = os.environ["BUCKET_NAME"]
LOG_FILE = os.environ["LOG_FILE"]


def lambda_handler(event, context):
    try:
        # ログの管理・書き込みを担当するLogManagerのインスタンスを作成
        log_manager = LogManager("/tmp", LOG_FILE)
        today_time_str = log_manager.format_time(log_manager.get_current_time())[1]

        # ログ内容を生成し、ファイルに書き込む
        log_content = f"{today_time_str}　テスト ファイル だよ"
        tmp_log_file = log_manager.write_log(log_content)

        # S3Uploaderのインスタンスを作成し、ログファイルをS3にアップロード
        uploader = S3Uploader(BUCKET_NAME)
        s3_key = tmp_log_file.split("/tmp/")[1]
        uploader.upload_log(tmp_log_file, s3_key)

    except Exception as e:
        print("エラーが発生しました: ", e)
        print(traceback.format_exc())


if __name__ == "__main__":
    test_event = {}
    test_context = {}
    lambda_handler(test_event, test_context)
