from aip import AipSpeech
import wave
import pygame.mixer
import io
import time

class BaiduTTS:
    def __init__(self, app_id, api_key, secret_key):
        self.client = AipSpeech(app_id, api_key, secret_key)
        pygame.mixer.init(frequency=16000)

    def speak(self, text):
        try:
            # 调用百度TTS API
            result = self.client.synthesis(text, 'jp', 1, {
                'spd': 5,  # 语速
                'pit': 5,  # 音调
                'vol': 5,  # 音量
                'per': 0   # 发音人，可以根据需求更改
            })

            # 检查返回结果是否为音频数据
            if not isinstance(result, dict):
                # 将音频数据写入内存文件
                audio_io = io.BytesIO(result)
                
                # 使用pygame播放音频
                pygame.mixer.music.load(audio_io)
                pygame.mixer.music.play()
                
                # 等待音频播放完成
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    
            else:
                print("TTS转换失败:", result)
                
        except Exception as e:
            print(f"TTS错误: {e}") 