# translatevideo
 
# 视频字幕处理项目

这个项目旨在自动生成视频字幕并进行翻译。它使用 Whisper 提取视频中的音频并生成字幕文件，使用 Ollama API 进行字幕翻译。

## 目录结构

```
translatevideo/
├── .env # 配置文件
├── main.py # 主程序入口
├── utils/ # 工具模块
│ ├── file_utils.py # 文件操作相关
│ ├── subtitle_utils.py # 字幕处理相关
│ ├── translate_utils.py # 翻译相关
├── requirements.txt # 项目依赖
├── README.md # 项目说明
```


## 部署方案

### 1. 环境准备

确保你的开发环境中已经安装了 Python 3.x。可以通过以下命令检查 Python 版本：
```
python --version
```


### 2. 克隆项目

首先，将项目克隆到本地：
```
git clone https://github.com/yourusername/your_project.git
cd your_project
```


### 3. 创建虚拟环境（可选）

为了避免依赖冲突，建议创建一个虚拟环境：
```
创建虚拟环境
python -m venv translatevideo

激活虚拟环境（Windows）
translatevideo\Scripts\activate

激活虚拟环境（macOS/Linux）
source translatevideo/bin/activate
```


### 4. 安装依赖

使用 `requirements.txt` 安装所需的依赖包：
```
pip install -r requirements.txt
```

安装cuda，如果有需要，这个根据情况咨询安装：
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### 5. 配置环境变量

在项目根目录下创建一个 `.env` 文件，并根据需要配置以下内容：
```
LOCAL_DIR=/path/to/your/video/directory # 替换为你的视频文件所在目录
DEFAULT_LANG=zh # 默认翻译语言（例如：zh）
```


### 6. 安装 Ollama

确保你已经安装并运行了 Ollama，并选择了合适的模型。Ollama 默认监听 `https://127.0.0.1:11434`。

### 7. 运行主程序

最后，运行主程序以开始处理视频字幕：
```
python main.py
```
### 8. 运行诊断程序

你可以先运行一下检测程序，看看有没有配置成功：
```
python diagnose.py
```

## 使用说明

- 本项目会自动查找指定目录下的所有视频文件，并生成对应的字幕文件。
- 如果字幕文件已经存在，将跳过字幕生成步骤。
- 如果翻译后的字幕文件不存在，将调用 Ollama API 进行翻译。

## 注意事项

- 确保你的机器上有足够的计算资源来运行 Whisper 和 Ollama。
- 根据需要调整代码中的参数和配置以满足你的需求。

## License

MIT License.
