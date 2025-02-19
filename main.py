# main.py
import os
from utils import file_utils, subtitle_utils, translate_utils
from dotenv import load_dotenv

load_dotenv()

LOCAL_DIR = os.getenv("LOCAL_DIR")
DEFAULT_LANG = os.getenv("DEFAULT_LANG")

def main():
    video_files = file_utils.get_all_video_files(LOCAL_DIR)

    for video_file in video_files:
        # 检查字幕文件是否存在
        if not subtitle_utils.check_subtitle_exists(video_file):
            print(f"生成字幕: {video_file}")
            subtitle_utils.generate_subtitle(video_file)
        else:
            print(f"字幕已存在: {video_file}")

        # 检查翻译字幕文件是否存在
        if not subtitle_utils.check_translated_subtitle_exists(video_file, DEFAULT_LANG):
            subtitle_file = video_file.rsplit('.', 1)[0] + '.srt'
            if os.path.exists(subtitle_file):
                print(f"翻译字幕: {video_file}")
                translate_utils.translate_subtitle(subtitle_file, DEFAULT_LANG)
            else:
                print(f"原始字幕文件不存在，无法翻译: {video_file}")
        else:
            print(f"翻译字幕已存在: {video_file}")
        break

if __name__ == "__main__":
    main()
