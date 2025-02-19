# diagnose.py
import os
import requests
from dotenv import load_dotenv

def check_env_file():
    """检查 .env 文件是否存在并加载配置"""
    if not os.path.exists('.env'):
        print("错误: .env 文件不存在，请确保该文件在项目根目录下。")
        return False

    load_dotenv()
    local_dir = os.getenv("LOCAL_DIR")
    default_lang = os.getenv("DEFAULT_LANG")

    if not local_dir or not default_lang:
        print("错误: .env 文件中缺少必要的配置项 (LOCAL_DIR 或 DEFAULT_LANG)。")
        return False

    print(f".env 配置项检查通过:\n  LOCAL_DIR: {local_dir}\n  DEFAULT_LANG: {default_lang}")
    return True

def check_ollama_connection():
    """检查 Ollama API 是否可连接"""
    try:
        response = requests.get('http://127.0.0.1:11434/api/version')
        response.raise_for_status()  # 检查是否有 HTTP 错误
        print("Ollama API 连接成功！")
        return True
    except requests.exceptions.RequestException as e:
        print(f"错误: 无法连接到 Ollama API - {e}")
        return False

def check_whisper_installation():
    """检查 Whisper 是否已安装并可用"""
    try:
        import whisper  # 尝试导入 Whisper 库
        print("Whisper 安装正常。")
        return True
    except ImportError:
        print("错误: Whisper 库未安装，请运行 'pip install whisper'。")
        return False

def main():
    print("项目诊断开始...\n")
    
    env_check = check_env_file()
    ollama_check = check_ollama_connection()
    whisper_check = check_whisper_installation()

    if env_check and ollama_check and whisper_check:
        print("\n所有检查通过，项目可以正常运行！")
    else:
        print("\n请根据上述错误信息进行修复。")

if __name__ == "__main__":
    main()
