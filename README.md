# model_process
对于语音模态、视频模态、图片模态的基本处理方法
## audio_segment.py
将长音频按语义分割为约10秒的片段，模型会检测，确保不会从一句话中间分隔割裂
参数：
    input_path: 输入音频文件路径
    output_prefix: 输出文件前缀
    target_duration: 目标片段时长（秒）
