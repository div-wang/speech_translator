from speech_recognition import RealtimeSpeechRecognizer
from translator import Translator
from tts import TextToSpeech
import time

def main():
    recognizer = RealtimeSpeechRecognizer()
    translator = Translator()
    tts = TextToSpeech()

    def on_speech_result(text):
        print(f"识别到的中文: {text}")
        # 翻译成英文
        english_text = translator.translate(text, from_lang='zh', to_lang='en')
        if english_text:
            print(f"翻译后的英文: {english_text}")
            # 播放英文语音
            tts.speak(english_text)

    try:
        print("开始录音，请说话...")
        recognizer.start(on_speech_result)
        
        # 保持程序运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止录音...")
        recognizer.stop()

if __name__ == "__main__":
    main() 