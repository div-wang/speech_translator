from aip import AipSpeech
import numpy as np
import wave
import io

class SpeechRecognizer:
    def __init__(self, app_id, api_key, secret_key):
        self.client = AipSpeech(app_id, api_key, secret_key)

    def recognize(self, audio_data):
        # 将音频数据转换为字节
        byte_io = io.BytesIO()
        with wave.open(byte_io, 'wb') as wave_file:
            wave_file.setnchannels(1)
            wave_file.setsampwidth(2)
            wave_file.setframerate(16000)
            wave_file.writeframes(audio_data.tobytes())
        
        audio_data = byte_io.getvalue()
        
        # 调用百度语音识别API
        result = self.client.asr(audio_data, 'wav', 16000, {
            'dev_pid': 1537,  # 支持中英文混合识别
        })
        
        if result['err_no'] == 0:
            return result['result'][0]
        return None 