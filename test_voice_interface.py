#!/usr/bin/env python3
"""
语音接口测试和诊断脚本
用于检查ASR、TTS、百度语音API配置和前端语音功能
"""

import requests
import json
import time
import subprocess
import webbrowser
from pathlib import Path
import tempfile
import wave
import struct

class VoiceInterfaceTester:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_banner(self):
        """显示测试横幅"""
        print("=" * 80)
        print("🎤 涂序彦教授数字人项目 - 语音接口测试和诊断")
        print("=" * 80)
        print("🎯 测试目标:")
        print("   - 检查百度语音API配置")
        print("   - 测试ASR（语音识别）功能")
        print("   - 测试TTS（语音合成）功能")
        print("   - 验证前端语音录音功能")
        print("   - 提供故障排除建议")
        print("=" * 80)
    
    def check_services(self):
        """检查服务状态"""
        print("\n🔍 检查服务状态...")
        
        try:
            backend_response = requests.get(self.backend_url, timeout=5)
            backend_ok = backend_response.status_code == 200
            print(f"{'✅' if backend_ok else '❌'} 后端服务: {'正常' if backend_ok else '异常'}")
        except:
            backend_ok = False
            print("❌ 后端服务: 无法访问")
        
        try:
            frontend_response = requests.get(self.frontend_url, timeout=5)
            frontend_ok = frontend_response.status_code == 200
            print(f"{'✅' if frontend_ok else '❌'} 前端服务: {'正常' if frontend_ok else '异常'}")
        except:
            frontend_ok = False
            print("❌ 前端服务: 无法访问")
        
        return backend_ok, frontend_ok
    
    def start_services_if_needed(self):
        """如果需要，启动服务"""
        backend_ok, frontend_ok = self.check_services()
        
        if not backend_ok or not frontend_ok:
            print("\n🚀 启动项目服务...")
            try:
                subprocess.Popen([
                    "python3", "quick_start.py"
                ], cwd=self.project_root)
                
                print("⏳ 等待服务启动...")
                time.sleep(15)
                
                backend_ok, frontend_ok = self.check_services()
                return backend_ok and frontend_ok
            except Exception as e:
                print(f"❌ 启动服务失败: {e}")
                return False
        
        return True
    
    def test_speech_status(self):
        """测试语音服务状态"""
        print("\n🔍 检查语音服务状态...")
        
        try:
            response = requests.get(f"{self.backend_url}/speech_status", timeout=10)
            
            if response.status_code == 200:
                status = response.json()
                print("✅ 语音服务状态获取成功")
                print(f"   百度语音可用: {'✅' if status.get('baidu_speech_available') else '❌'}")
                print(f"   ASR启用: {'✅' if status.get('asr_enabled') else '❌'}")
                print(f"   TTS启用: {'✅' if status.get('tts_enabled') else '❌'}")
                print(f"   APP ID: {status.get('app_id', '未配置')}")
                print(f"   状态信息: {status.get('message', '无信息')}")
                
                return status.get('baidu_speech_available', False)
            else:
                print(f"❌ 语音服务状态检查失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 语音服务状态检查异常: {e}")
            return False
    
    def create_test_audio(self):
        """创建测试音频文件"""
        print("\n🎵 创建测试音频文件...")
        
        try:
            # 创建一个简单的WAV文件（1秒的440Hz正弦波）
            sample_rate = 16000
            duration = 1.0
            frequency = 440.0
            
            # 生成音频数据
            samples = []
            for i in range(int(sample_rate * duration)):
                t = i / sample_rate
                sample = int(32767 * 0.3 * (2 * 3.14159 * frequency * t) % (2 * 3.14159))
                samples.append(sample)
            
            # 创建临时WAV文件
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            
            with wave.open(temp_file.name, 'w') as wav_file:
                wav_file.setnchannels(1)  # 单声道
                wav_file.setsampwidth(2)  # 16位
                wav_file.setframerate(sample_rate)
                
                # 写入音频数据
                for sample in samples:
                    wav_file.writeframes(struct.pack('<h', sample))
            
            print(f"✅ 测试音频文件创建成功: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            print(f"❌ 创建测试音频失败: {e}")
            return None
    
    def test_asr_endpoint(self):
        """测试ASR端点"""
        print("\n🎤 测试ASR（语音识别）端点...")
        
        # 创建测试音频
        audio_file_path = self.create_test_audio()
        if not audio_file_path:
            return False
        
        try:
            # 准备文件上传
            with open(audio_file_path, 'rb') as f:
                files = {'audio_file': ('test.wav', f, 'audio/wav')}
                
                print("📤 发送ASR请求...")
                start_time = time.time()
                
                response = requests.post(
                    f"{self.backend_url}/asr",
                    files=files,
                    timeout=30
                )
                
                elapsed_time = time.time() - start_time
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ ASR请求成功！")
                    print(f"⏱️  响应时间: {elapsed_time:.2f}秒")
                    print(f"📝 识别结果: {result.get('text', '无文本')}")
                    print(f"🎯 置信度: {result.get('confidence', 0):.2f}")
                    print(f"✅ 成功状态: {result.get('success', False)}")
                    print(f"💬 消息: {result.get('message', '无消息')}")
                    
                    # 清理临时文件
                    Path(audio_file_path).unlink()
                    
                    return result.get('success', False)
                else:
                    print(f"❌ ASR请求失败，状态码: {response.status_code}")
                    print(f"📄 响应内容: {response.text}")
                    return False
                    
        except Exception as e:
            print(f"❌ ASR测试异常: {e}")
            return False
        finally:
            # 确保清理临时文件
            if audio_file_path and Path(audio_file_path).exists():
                Path(audio_file_path).unlink()
    
    def test_tts_endpoint(self):
        """测试TTS端点"""
        print("\n🔊 测试TTS（语音合成）端点...")
        
        try:
            # 准备TTS请求
            tts_data = {
                "text": "您好，我是涂序彦教授，欢迎来到人工智能的世界。",
                "voice": "zh-CN-male",
                "speed": 4,
                "pitch": 6,
                "volume": 5
            }
            
            print(f"📤 发送TTS请求: {tts_data['text']}")
            start_time = time.time()
            
            response = requests.post(
                f"{self.backend_url}/tts",
                json=tts_data,
                timeout=30
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                audio_data = response.content
                print(f"✅ TTS请求成功！")
                print(f"⏱️  响应时间: {elapsed_time:.2f}秒")
                print(f"🎵 音频大小: {len(audio_data)} bytes")
                print(f"📄 内容类型: {response.headers.get('content-type', '未知')}")
                
                # 保存音频文件用于验证
                test_audio_path = "test_tts_output.wav"
                with open(test_audio_path, 'wb') as f:
                    f.write(audio_data)
                print(f"💾 音频已保存到: {test_audio_path}")
                
                return True
            else:
                print(f"❌ TTS请求失败，状态码: {response.status_code}")
                print(f"📄 响应内容: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ TTS测试异常: {e}")
            return False
    
    def test_frontend_voice_features(self):
        """测试前端语音功能"""
        print("\n🌐 测试前端语音功能...")
        
        try:
            # 打开浏览器到项目页面
            webbrowser.open(self.frontend_url)
            print(f"✅ 已在浏览器中打开: {self.frontend_url}")
            
            # 创建前端测试脚本
            test_script = """
// 前端语音功能测试脚本
// 在浏览器控制台中运行

console.log("🎤 开始前端语音功能测试...");

function testMicrophoneAccess() {
    console.log("🔍 测试麦克风访问权限...");
    
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            console.log("✅ 麦克风访问成功");
            console.log("🎤 音频轨道数量:", stream.getAudioTracks().length);
            
            // 停止音频流
            stream.getTracks().forEach(track => track.stop());
            
            return true;
        })
        .catch(error => {
            console.error("❌ 麦克风访问失败:", error);
            console.log("💡 请检查浏览器权限设置");
            return false;
        });
}

function testMediaRecorderSupport() {
    console.log("🔍 测试MediaRecorder支持...");
    
    if (typeof MediaRecorder !== 'undefined') {
        console.log("✅ MediaRecorder支持");
        
        // 检查支持的MIME类型
        const mimeTypes = [
            'audio/webm',
            'audio/webm;codecs=opus',
            'audio/wav',
            'audio/ogg'
        ];
        
        console.log("📋 支持的音频格式:");
        mimeTypes.forEach(type => {
            const supported = MediaRecorder.isTypeSupported(type);
            console.log(`   ${type}: ${supported ? '✅' : '❌'}`);
        });
        
        return true;
    } else {
        console.error("❌ MediaRecorder不支持");
        return false;
    }
}

function testVoiceRecorderComponent() {
    console.log("🔍 测试语音录音组件...");
    
    const voiceButton = document.querySelector('.voice-recorder-btn');
    if (voiceButton) {
        console.log("✅ 找到语音录音按钮");
        console.log("🎨 按钮状态:", voiceButton.className);
        console.log("🔘 按钮是否禁用:", voiceButton.disabled);
        return true;
    } else {
        console.error("❌ 未找到语音录音按钮");
        console.log("💡 请检查VoiceRecorder组件是否正确加载");
        return false;
    }
}

function testAudioPlayerComponent() {
    console.log("🔍 测试音频播放组件...");
    
    const audioButtons = document.querySelectorAll('[title*="播放"], [title*="朗读"]');
    if (audioButtons.length > 0) {
        console.log(`✅ 找到 ${audioButtons.length} 个音频播放按钮`);
        return true;
    } else {
        console.error("❌ 未找到音频播放按钮");
        console.log("💡 请检查AudioPlayer组件是否正确加载");
        return false;
    }
}

function testBackendConnection() {
    console.log("🔍 测试后端语音接口连接...");
    
    // 测试语音状态端点
    fetch('http://127.0.0.1:8000/speech_status')
        .then(response => response.json())
        .then(data => {
            console.log("✅ 语音状态获取成功:");
            console.log("   百度语音可用:", data.baidu_speech_available ? '✅' : '❌');
            console.log("   ASR启用:", data.asr_enabled ? '✅' : '❌');
            console.log("   TTS启用:", data.tts_enabled ? '✅' : '❌');
            console.log("   状态信息:", data.message);
        })
        .catch(error => {
            console.error("❌ 语音状态获取失败:", error);
        });
}

// 运行所有测试
console.log("🚀 开始前端语音功能测试...");

setTimeout(() => testMicrophoneAccess(), 500);
setTimeout(() => testMediaRecorderSupport(), 1000);
setTimeout(() => testVoiceRecorderComponent(), 1500);
setTimeout(() => testAudioPlayerComponent(), 2000);
setTimeout(() => testBackendConnection(), 2500);

console.log("🎯 前端语音功能测试脚本运行完成");
console.log("💡 请查看上述测试结果，如有问题请参考故障排除建议");
"""
            
            # 保存测试脚本
            with open("browser_voice_test.js", "w", encoding="utf-8") as f:
                f.write(test_script)
            
            print("📄 前端测试脚本已创建: browser_voice_test.js")
            print("💡 请在浏览器控制台中运行此脚本")
            
            return True
            
        except Exception as e:
            print(f"❌ 前端测试准备失败: {e}")
            return False
    
    def provide_troubleshooting_guide(self, results):
        """提供故障排除指南"""
        print("\n" + "=" * 80)
        print("🔧 语音接口故障排除指南")
        print("=" * 80)
        
        if not results.get('speech_status', False):
            print("\n❌ 百度语音API配置问题:")
            print("   1. 检查api_server.py中的百度API配置:")
            print("      - BAIDU_APP_ID = '119601523'")
            print("      - BAIDU_API_KEY = 'oOynRSSJJx0HReZxWpghwfdh'")
            print("      - BAIDU_SECRET_KEY = 'syqCl5ME2ZlkUJLUHRkJZQGCepH4QNa4'")
            print("   2. 安装百度语音SDK:")
            print("      pip install baidu-aip")
            print("   3. 检查百度智能云账户状态和余额")
        
        if not results.get('asr', False):
            print("\n❌ ASR（语音识别）问题:")
            print("   1. 检查音频文件格式（支持WAV、MP3、WebM）")
            print("   2. 确保音频采样率为16000Hz")
            print("   3. 检查文件大小（限制10MB）")
            print("   4. 验证麦克风权限设置")
        
        if not results.get('tts', False):
            print("\n❌ TTS（语音合成）问题:")
            print("   1. 检查文本长度（限制1024字符）")
            print("   2. 验证语音参数设置")
            print("   3. 检查网络连接")
        
        print("\n🌐 前端语音功能问题:")
        print("   1. 浏览器权限设置:")
        print("      - 允许麦克风访问")
        print("      - 允许音频播放")
        print("   2. HTTPS要求:")
        print("      - 某些浏览器要求HTTPS才能访问麦克风")
        print("      - 本地开发可以使用localhost")
        print("   3. 浏览器兼容性:")
        print("      - 推荐使用Chrome、Firefox、Safari")
        print("      - 检查MediaRecorder API支持")
        
        print("\n🔍 调试方法:")
        print("   1. 查看浏览器控制台错误信息")
        print("   2. 检查网络请求状态")
        print("   3. 运行browser_voice_test.js脚本")
        print("   4. 查看后端日志输出")
        
        print("\n📞 常见解决方案:")
        print("   1. 重启浏览器并重新授权麦克风权限")
        print("   2. 清除浏览器缓存和Cookie")
        print("   3. 检查防火墙和代理设置")
        print("   4. 更新浏览器到最新版本")
    
    def run_full_test(self):
        """运行完整测试"""
        self.print_banner()
        
        results = {
            'services': False,
            'speech_status': False,
            'asr': False,
            'tts': False,
            'frontend': False
        }
        
        # 1. 启动服务
        if not self.start_services_if_needed():
            print("❌ 服务启动失败")
            return results
        
        results['services'] = True
        
        # 2. 检查语音服务状态
        results['speech_status'] = self.test_speech_status()
        
        # 3. 测试ASR端点
        results['asr'] = self.test_asr_endpoint()
        
        # 4. 测试TTS端点
        results['tts'] = self.test_tts_endpoint()
        
        # 5. 测试前端功能
        results['frontend'] = self.test_frontend_voice_features()
        
        # 显示测试总结
        self.print_test_summary(results)
        
        # 提供故障排除指南
        self.provide_troubleshooting_guide(results)
        
        return results
    
    def print_test_summary(self, results):
        """显示测试总结"""
        print("\n" + "=" * 80)
        print("📊 语音接口测试结果总结")
        print("=" * 80)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        test_names = {
            'services': '服务启动',
            'speech_status': '语音服务状态',
            'asr': 'ASR语音识别',
            'tts': 'TTS语音合成',
            'frontend': '前端语音功能'
        }
        
        for test_key, result in results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   {test_names[test_key]}: {status}")
        
        print(f"\n📈 总体结果: {passed_tests}/{total_tests} 项测试通过")
        
        if passed_tests == total_tests:
            print("🎉 所有语音功能测试通过！语音接口配置正确。")
        elif results['services'] and results['speech_status']:
            print("⚠️  基本服务正常，但部分语音功能可能有问题。")
        else:
            print("❌ 存在严重问题，请检查配置和依赖。")

def main():
    """主函数"""
    tester = VoiceInterfaceTester()
    results = tester.run_full_test()
    return all(results.values())

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
