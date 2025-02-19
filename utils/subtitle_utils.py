# utils/subtitle_utils.py
import os
import subprocess
import time
import whisper
from pydub import AudioSegment
from collections import Counter
from dotenv import load_dotenv

load_dotenv()
import torch

LLM_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# LLM_DEVICE = os.getenv("LLM_DEVICE")
DEFAULT_DETECT_LANG = os.getenv("DEFAULT_DETECT_LANG")
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL_NAME")

def check_subtitle_exists(video_file):
    subtitle_file = video_file.rsplit('.', 1)[0] + '.srt'
    return os.path.exists(subtitle_file)

def check_translated_subtitle_exists(video_file, lang):
    subtitle_file = video_file.rsplit('.', 1)[0] + f'_{lang}.srt'
    return os.path.exists(subtitle_file)

def detect_dominant_language(audio_path, segment_duration=30):
    """
    从音频文件的三个片段检测语言，并返回出现次数最多的语言.

    Args:
        audio_path (str): 音频文件路径.
        segment_duration (int): 每个片段的持续时间（秒）.

    Returns:
        str: 检测到的主要语言.
    """

    # 加载 Whisper 模型
    model = whisper.load_model(WHISPER_MODEL_NAME, device=LLM_DEVICE)

    # 使用 PyDub 加载音频文件
    audio = AudioSegment.from_file(audio_path)
    audio_length = len(audio) / 1000  # 音频总长度（秒）

    # 确定起始和结束时间
    # 开始时间 总时长的25%  结束时间 总时长的75%
    start_time = audio_length * 0.25
    end_time = audio_length * 0.75

    # 检查音频长度是否足够
    if end_time - start_time < segment_duration * 2:  # 至少需要两个片段的长度
        # raise ValueError("音频长度不足以提取三个片段")
        print("❌ 音频长度不足以提取三个片段, 使用默认语言")
        return DEFAULT_DETECT_LANG

    # 计算三个片段的起始时间
    segment_interval = (end_time - start_time - segment_duration) / 2  # 计算间隔
    segment_times = [start_time, start_time + segment_interval, end_time - segment_duration]

    detected_languages = []
    for start in segment_times:
        # 提取指定片段
        start_ms = start * 1000  # 转换为毫秒
        end_ms = (start + segment_duration) * 1000
        segment = audio[start_ms:end_ms]

        # 将片段保存为临时文件
        segment_path = "temp_segment.wav"
        segment.export(segment_path, format="wav")
        
        # 加载片段并进行预处理
        audio_segment = whisper.load_audio(segment_path)
        audio_segment = whisper.pad_or_trim(audio_segment)

        # 生成 log-Mel 谱图
        mel = whisper.log_mel_spectrogram(audio_segment, n_mels=model.dims.n_mels).to(model.device)

        # 检测语言
        _, probs = model.detect_language(mel)
        detected_language = max(probs, key=probs.get)
        # print(f"Detected language: {detected_language}")
        detected_languages.append(detected_language)

    # 统计出现次数最多的语言
    language_counts = Counter(detected_languages)
    dominant_language = language_counts.most_common(1)[0][0]
    print(f"✌️ Dominant language: {dominant_language}, languages: {detected_languages}")
    return dominant_language

def generate_subtitle(video_file):
    # 使用 whisper 生成字幕
    # 统计生成时间
    start_time = time.time()
    try:
        output_dir = os.path.dirname(video_file)
        language = detect_dominant_language(video_file)
        # 确保 whisper 已经安装
        print(f"使用 {LLM_DEVICE} 生成 {language} 字幕: {video_file}")
        if LLM_DEVICE == 'cuda':
            subprocess.run(['whisper', video_file, '--model', WHISPER_MODEL_NAME, '--device', 'cuda', '--output_dir', output_dir, '--language', language], check=True)  # 使用 GPU
        else:
            subprocess.run(['whisper', video_file, '--model', WHISPER_MODEL_NAME, '--output_dir', output_dir, '--language', language], check=True)  # 使用 CPU

        end_time = time.time()
        print(f"字幕生成成功: {video_file} (耗时: {end_time - start_time:.2f} 秒)")
    except subprocess.CalledProcessError as e:
        print(f"字幕生成失败: {e}")

if __name__ == '__main__':
    # 示例
    video_file = "/path/to/your/video/abc.mp4"  # 替换成你的视频文件
    if not check_subtitle_exists(video_file):
        generate_subtitle(video_file)
    else:
        print("字幕文件已存在")
