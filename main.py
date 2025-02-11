import sounddevice as sd
from speech_recognition import RealtimeSpeechRecognizer
from translator import BaiduTranslator
from tts import BaiduTTS
import config
import numpy as np

def main():
    # 初始化模块
    recognizer = RealtimeSpeechRecognizer(
        config.BAIDU_APP_ID,
        config.BAIDU_API_KEY,
        config.BAIDU_SECRET_KEY
    )
    translator = BaiduTranslator(config.BAIDU_APP_ID, config.BAIDU_SECRET_KEY)
    tts = BaiduTTS(config.BAIDU_APP_ID, config.BAIDU_API_KEY, config.BAIDU_SECRET_KEY)

    def audio_callback(indata, frames, time, status):
        """音频回调函数"""
        if status:
            print(f"状态: {status}")
        # 发送音频数据到识别器
        recognizer.send_audio(indata.copy())

    def on_recognition_result(text):
        """识别结果回调"""
        print(f"识别结果: {text}")
        japanese_text = translator.translate(text)
        if japanese_text:
            print(f"日语翻译: {japanese_text}")
            tts.speak(japanese_text)

    # 启动语音识别
    recognizer.start(callback=on_recognition_result)

    try:
        # 开启音频流
        with sd.InputStream(
            channels=1,
            dtype=np.int16,
            samplerate=16000,
            blocksize=1024,
            callback=audio_callback
        ):
            print("开始录音，按Ctrl+C停止...")
            while True:
                sd.sleep(1000)
                
    except KeyboardInterrupt:
        print("\n停止录音...")
        recognizer.stop()

if __name__ == "__main__":
    main() 