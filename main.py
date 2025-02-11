from audio_recorder import AudioRecorder
from speech_recognition import SpeechRecognizer
from translator import BaiduTranslator
from tts import BaiduTTS
import config
import time
import numpy as np

def main():
    # 初始化各个模块
    recorder = AudioRecorder(rate=config.RATE, chunk=config.CHUNK)
    recognizer = SpeechRecognizer(config.BAIDU_APP_ID, 
                                 config.BAIDU_API_KEY, 
                                 config.BAIDU_SECRET_KEY)
    translator = BaiduTranslator(config.BAIDU_APP_ID, config.BAIDU_SECRET_KEY)
    tts = BaiduTTS(config.BAIDU_APP_ID, config.BAIDU_API_KEY, config.BAIDU_SECRET_KEY)

    print("开始录音...")
    recorder.start_recording()

    try:
        while True:
            # 获取音频数据
            audio_data = recorder.get_audio_data()
            if audio_data is not None:
                # 语音识别
                text = recognizer.recognize(audio_data)
                if text:
                    print(f"识别结果: {text}")
                    
                    # 翻译成日语
                    japanese_text = translator.translate(text)
                    if japanese_text:
                        print(f"日语翻译: {japanese_text}")
                        # 使用TTS播放翻译后的文本
                        tts.speak(japanese_text)
                        
            time.sleep(0.1)  # 短暂休眠以降低CPU使用率

    except KeyboardInterrupt:
        print("\n停止录音...")
        recorder.stop_recording()

if __name__ == "__main__":
    main() 