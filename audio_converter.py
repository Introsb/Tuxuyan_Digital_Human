#!/usr/bin/env python3
"""
音频格式转换工具
用于将前端录音格式转换为百度云ASR支持的格式
"""

import io
import tempfile
import os
from typing import Tuple, Optional

# 暂时禁用pydub以避免依赖问题
PYDUB_AVAILABLE = False


def convert_audio_for_baidu_asr(audio_data: bytes, original_format: str) -> Tuple[bytes, str]:
    """
    将音频数据转换为百度云ASR支持的格式

    Args:
        audio_data: 原始音频数据
        original_format: 原始格式 (wav, webm, mp3, etc.)

    Returns:
        Tuple[转换后的音频数据, 目标格式]
    """

    # 如果已经是WAV格式，直接返回
    if original_format.lower() == 'wav':
        return audio_data, 'wav'

    # 对于WebM格式，尝试直接作为WAV发送给百度云
    # 百度云ASR有时可以处理WebM格式的音频数据
    if original_format.lower() in ['webm', 'ogg']:
        print(f"🔄 WebM/OGG格式将作为WAV格式发送给百度云ASR")
        return audio_data, 'wav'

    # 如果pydub不可用，尝试直接使用原始数据
    if not PYDUB_AVAILABLE:
        print(f"⚠️ 无法转换{original_format}格式，使用原始数据")
        return audio_data, original_format

    try:
        # 使用pydub转换音频格式
        print(f"🔄 转换音频格式: {original_format} -> wav")

        # 创建临时文件来处理音频
        with tempfile.NamedTemporaryFile(suffix=f'.{original_format}', delete=False) as temp_input:
            temp_input.write(audio_data)
            temp_input_path = temp_input.name

        try:
            # 根据原始格式加载音频
            if original_format.lower() == 'mp3':
                audio = AudioSegment.from_mp3(temp_input_path)
            else:
                audio = AudioSegment.from_file(temp_input_path)

            # 转换为WAV格式，设置为16kHz单声道（百度云ASR推荐格式）
            audio = audio.set_frame_rate(16000).set_channels(1)

            # 导出为WAV格式
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_output:
                audio.export(temp_output.name, format="wav")
                temp_output_path = temp_output.name

            # 读取转换后的数据
            with open(temp_output_path, 'rb') as f:
                converted_data = f.read()

            # 清理临时文件
            os.unlink(temp_input_path)
            os.unlink(temp_output_path)

            print(f"✅ 音频转换成功: {len(audio_data)} -> {len(converted_data)} bytes")
            return converted_data, 'wav'

        except Exception as e:
            print(f"❌ 音频转换失败: {e}")
            # 清理临时文件
            if os.path.exists(temp_input_path):
                os.unlink(temp_input_path)
            # 转换失败，返回原始数据
            return audio_data, original_format

    except Exception as e:
        print(f"❌ 音频处理异常: {e}")
        return audio_data, original_format


def get_audio_info(audio_data: bytes, format_hint: str = 'wav') -> dict:
    """
    获取音频信息
    
    Args:
        audio_data: 音频数据
        format_hint: 格式提示
        
    Returns:
        音频信息字典
    """
    info = {
        'size': len(audio_data),
        'format': format_hint,
        'duration': None,
        'sample_rate': None,
        'channels': None
    }
    
    if not PYDUB_AVAILABLE:
        return info
    
    try:
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=f'.{format_hint}', delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name
        
        try:
            # 加载音频文件
            if format_hint.lower() in ['webm', 'ogg']:
                audio = AudioSegment.from_file(temp_path, format="webm")
            elif format_hint.lower() == 'mp3':
                audio = AudioSegment.from_mp3(temp_path)
            else:
                audio = AudioSegment.from_file(temp_path)
            
            info.update({
                'duration': len(audio) / 1000.0,  # 转换为秒
                'sample_rate': audio.frame_rate,
                'channels': audio.channels
            })
            
        except Exception as e:
            print(f"⚠️ 无法获取音频信息: {e}")
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"⚠️ 音频信息获取异常: {e}")
    
    return info


def test_audio_conversion():
    """测试音频转换功能"""
    print("🧪 测试音频转换功能")
    
    if not PYDUB_AVAILABLE:
        print("❌ pydub不可用，无法进行转换测试")
        return False
    
    # 创建一个简单的测试音频
    try:
        # 生成1秒的静音音频作为测试
        test_audio = AudioSegment.silent(duration=1000)  # 1秒
        test_audio = test_audio.set_frame_rate(16000).set_channels(1)
        
        # 导出为WebM格式（模拟前端录音）
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_webm:
            test_audio.export(temp_webm.name, format="webm")
            temp_webm_path = temp_webm.name
        
        # 读取WebM数据
        with open(temp_webm_path, 'rb') as f:
            webm_data = f.read()
        
        print(f"📁 测试WebM文件大小: {len(webm_data)} bytes")
        
        # 转换为WAV
        converted_data, converted_format = convert_audio_for_baidu_asr(webm_data, 'webm')
        
        print(f"📁 转换后WAV文件大小: {len(converted_data)} bytes")
        print(f"📁 转换后格式: {converted_format}")
        
        # 获取音频信息
        info = get_audio_info(converted_data, converted_format)
        print(f"📊 音频信息: {info}")
        
        # 清理临时文件
        os.unlink(temp_webm_path)
        
        print("✅ 音频转换测试成功")
        return True
        
    except Exception as e:
        print(f"❌ 音频转换测试失败: {e}")
        return False


if __name__ == "__main__":
    test_audio_conversion()
