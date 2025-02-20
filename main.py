# main.py
import os
from utils import file_utils, subtitle_utils, translate_utils
from dotenv import load_dotenv

load_dotenv()

LOCAL_DIR = os.getenv("LOCAL_DIR")
DEFAULT_LANG = os.getenv("DEFAULT_LANG")

def main():
    video_files = file_utils.get_all_video_files(LOCAL_DIR)
    print(f"开始处理视频文件: {len(video_files)}")
    for video_file in video_files:
        # 检查deal_data文件（json）是否存在, 不存在则生成
        subtitle_utils.subtitle_deal_data(video_file)
        # 保存 translated_lang
        subtitle_utils.save_translated_lang(video_file, DEFAULT_LANG)
        # 检测视频的主要语言
        dominant_language = subtitle_utils.check_subtitle_dominant_language(video_file)
        if not dominant_language:
            print(f"无法检测视频主要语言: {video_file}")
            continue
        
        # 检查字幕文件是否存在
        if not subtitle_utils.check_subtitle_exists(video_file):
            print(f"生成字幕: {video_file}")
            subtitle_utils.generate_subtitle(video_file, dominant_language)
        else:
            print(f"字幕已存在: {video_file}")

        # 检查翻译字幕文件是否存在
        if not subtitle_utils.check_translated_subtitle_exists(video_file):
            deal_data = subtitle_utils.read_deal_data(video_file)
            video_lang = deal_data.get('video_lang')
            translated_lang = deal_data.get('translated_lang')
            video_lang_subtitle = deal_data.get('video_lang_subtitle')
            if not video_lang_subtitle:
                print(f"无法获取视频原始字幕: {video_file}")
            else:

                # 这里拼一下目录, 如果 video_lang = en, translated_lang = zh, video_lang_subtitle=xxx_en.srt, translated_lang_subtitle=xxx_zh.srt
                translated_lang_subtitle = video_lang_subtitle.replace(f"_{video_lang}.srt", f"_{translated_lang}.srt")
                # 判断是否需要翻译字幕
                if video_lang == translated_lang:
                    print(f"不需要翻译字幕: {video_file}")
                else:
                    print(f"翻译字幕: {video_file}")
                    # 原始字幕，以及要翻译的语言
                    video_lang_subtitle = deal_data.get('video_lang_subtitle')
                    translate_utils.translate_subtitle(video_lang_subtitle, translated_lang, translated_lang_subtitle)
                    # 说明，可能会翻译失败的
                    if not os.path.exists(translated_lang_subtitle):
                        print(f"翻译字幕失败: {video_file}")
                # 保存翻译后的字幕
                subtitle_utils.save_translated_lang_subtitle(video_file, translated_lang_subtitle)
        else:
            print(f"翻译字幕已存在: {video_file}")


if __name__ == "__main__":
    main()
