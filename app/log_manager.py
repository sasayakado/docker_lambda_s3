import os
import datetime
import pytz

class LogManager:
    def __init__(self, base_dir, log_file_name):
        """LogManagerの初期化

        Parameters:
        - base_dir (str): ログファイルを保存する基本ディレクトリ。
        - log_file_name (str): ログファイルの名前のベース部分。
        """
        self.base_dir = base_dir
        self.log_file_name = log_file_name
    
    def get_current_time(self):
        """日本のタイムゾーンでの現在時刻を取得

        Returns:
        datetime: 現在の日本のタイムゾーンの日時。
        """
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        return datetime.datetime.now(tokyo_tz)

    def format_time(self, current_time):
        """日時をフォーマットする

        Parameters:
        - current_time (datetime): フォーマットする日時。

        Returns:
        tuple: (日付の文字列, 日時の文字列)。
        """
        return current_time.strftime('%-m月%-d日'), current_time.strftime('%Y%m%d_%H:%M:%S')

    def write_log(self, content):
        """ログ内容をファイルに書き込む

        Parameters:
        - content (str): 書き込むログの内容。

        Returns:
        str: 作成されたログファイルのパス。
        """
        current_time = self.get_current_time()
        today_str, today_time_str = self.format_time(current_time)

        log_dir = os.path.join(self.base_dir, today_str)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_path = os.path.join(log_dir, f"{today_time_str}{self.log_file_name}")

        with open(log_file_path, 'w') as f:
            f.write(content + '\n')
        
        return log_file_path
