# utils/translate_utils.py
import os
import time
from litellm import completion
from dotenv import load_dotenv
from . import config

load_dotenv()

API_BASE = os.getenv("LLM_API_BASE")
MODEL = os.getenv("LLM_MODEL_NAME")
DEFAULT_LANG = os.getenv("DEFAULT_LANG")

print(f"调用 litellm API: {API_BASE}, Model: {MODEL}")

def llm_completion(messages):
    # 调用 litellm API 进行翻译
    try:
        response = completion(
            model=MODEL, 
            messages=messages, 
            api_base=API_BASE,
            temperature=0.2,
        )
        print(response)
        content = response['choices'][0]['message']['content']
        return content
    except Exception as e:
        print(f"翻译失败: {e}")
        return None

def srt_to_array(subtitle_file: str) -> list:
    subtitle_array = []
    with open(subtitle_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # print(lines)
        i = 0
        while i < len(lines):
            # 读取序号
            sequence_number = lines[i].strip()
            i += 1
            # 读取时间码
            timecode = lines[i].strip()
            i += 1
            # 读取字幕文本
            subtitle_text = lines[i].strip()
            i += 1
            subtitle_array.append({'sequence_number': sequence_number, 'timecode': timecode, 'text': subtitle_text.strip()})
            # 跳过空行
            i += 1
    return subtitle_array

def array_to_srt(subtitle_array: list, subtitle_file: str):
    with open(subtitle_file, 'w', encoding='utf-8') as file:
        for subtitle in subtitle_array:
            file.write(subtitle['sequence_number'] + '\n')
            file.write(subtitle['timecode'] + '\n')
            file.write(subtitle['text'] + '\n')
            file.write('\n')  # 用空行分隔字幕

def format_subtitle_text(text):
    # 去除多余的空格和换行符
    text = text.strip()
    # 去除多余的空格
    text = ' '.join(text.split())
    # 去除换行符
    text = text.replace('\n', ' ')
    return text

def translate_subtitle(subtitle_file, lang = DEFAULT_LANG):
    start_time = time.time()
    # 获取语言全称
    full_lang = config.LANG_DICT.get(lang)
    print(f"Translate the following text to {full_lang}")
    # 读取字幕文件
    # 从 SRT 文件读取字幕到数组
    subtitles = srt_to_array(subtitle_file)
    failed_count = 0
    success_count = 0
    # 翻译每条字幕
    for subtitle in subtitles:
        # 获取字幕文本 判断是否为空
        if not subtitle['text']:
            continue
        messages = [{ "content": f"请将以下用户发送的文本翻译成{full_lang}。请勿返回任何解释、说明或额外信息，只返回翻译后的文本。","role": "system"},{ "content": subtitle['text'],"role": "user"}]
        trans_text = llm_completion(messages)
        print(f"{subtitle['text']} -> {trans_text}")
        # TODO 这里需要评测翻译结果，如果翻译结果不符合预期，可以调用其他翻译 API
        # 翻译成功，替换原始文本
        trans_text = format_subtitle_text(trans_text)
        if trans_text and trans_text != subtitle['text']:
            subtitle['text'] = trans_text
            print(f"翻译成功: {subtitle['text']}")
            success_count += 1
        else:
            # 翻译失败，保留原始文本
            print(f"翻译失败: {subtitle['text']}")
            failed_count += 1
    print(f"翻译完成，失败次数: {failed_count}")
    failed_rate = failed_count / (failed_count + success_count) * 100
    end_time = time.time()
    print(f"翻译耗时: {end_time - start_time:.2f} 秒，失败率: {failed_rate:.2f}%")
    if failed_rate > 10:
        print(f"翻译失败率超过10%，请检查翻译结果，没有保存翻译后的字幕文件")
        return
    # 将翻译后的字幕写入新的 SRT 文件
    translated_subtitle_file = subtitle_file.replace('.srt', f'_{lang}.srt')
    array_to_srt(subtitles, translated_subtitle_file)
    

if __name__ == '__main__':
    # 示例
    subtitle_file = "/path/to/your/video/abc.srt"  # 替换成你的字幕文件
    lang = 'zh'  # 翻译成中文
    translate_subtitle(subtitle_file, lang)