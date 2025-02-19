# utils/file_utils.py
import os

def get_all_video_files(local_dir):
    video_files = []
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv')):  # 常见视频格式
                video_files.append(os.path.join(root, file))
    return video_files

if __name__ == '__main__':
    # 示例
    video_dir = "/path/to/your/video/directory"  # 替换成你的本地目录
    videos = get_all_video_files(video_dir)
    print(videos)
