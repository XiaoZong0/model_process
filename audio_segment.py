# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 16:41:30 2025

将长音频按语义分割为约10秒的片段，模型会检测，确保不会从一句话中间分隔割裂
参数：
    input_path: 输入音频文件路径
    output_prefix: 输出文件前缀
    target_duration: 目标片段时长（秒）

@author: zongx
"""
import whisper
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import numpy as np

def split_audio_by_sentences(input_path, output_prefix, target_duration=10):
    
    # 加载Whisper模型（首次运行会自动下载）
    model = whisper.load_model("base")

    # 加载音频文件
    audio = AudioSegment.from_file(input_path)
    total_duration = len(audio) / 1000  # 总时长（秒）

    # 语音识别带时间戳
    result = model.transcribe(input_path, word_timestamps=True)
    segments = result["segments"]

    # 生成候选切割点
    split_points = []
    current_end = 0
    
    while current_end < total_duration:
        # 寻找最佳切割点
        best_split = current_end + target_duration
        candidates = [s["end"] for s in segments 
                     if s["end"] > current_end 
                     and s["end"] <= current_end + target_duration*1.2]

        if candidates:
            # 选择最接近目标时长的句子边界
            best_split = min(candidates, key=lambda x: abs(x - (current_end + target_duration)))
        else:
            # 没有找到边界时使用静音检测
            non_silent = detect_nonsilent(
                audio[current_end*1000:],
                min_silence_len=500,
                silence_thresh=-40
            )
            if non_silent:
                best_split = current_end + (non_silent[0][1]/1000)

        split_points.append(best_split)
        current_end = best_split

    # 生成音频片段
    prev_point = 0
    for i, point in enumerate(split_points):
        # 转换为毫秒
        start = int(prev_point * 1000)
        end = int(point * 1000)
        
        chunk = audio[start:end]
        chunk.export(f"{output_prefix}_{i+1:03d}.wav", format="wav")
        prev_point = point

# 使用示例
split_audio_by_sentences(
    input_path="2_025_005.wav",
    output_prefix="output_chunk",
    target_duration=10
)
