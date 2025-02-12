import speech_recognition as sr
import threading
import time

class RealtimeSpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_running = False
        self.on_result = None
        self.mic = None

    def start(self, callback):
        """开始实时语音识别"""
        self.on_result = callback
        self.is_running = True
        
        # 启动识别线程
        self.recognition_thread = threading.Thread(target=self._recognition_loop)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()

    def _recognition_loop(self):
        """持续进行语音识别的循环"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            while self.is_running:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    try:
                        text = self.recognizer.recognize_google(audio, language='zh-CN')
                        if text and self.on_result:
                            self.on_result(text)
                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print(f"语音识别错误: {e}")
                except Exception as e:
                    if self.is_running:  # 忽略停止时的超时错误
                        print(f"录音错误: {e}")

    def stop(self):
        """停止语音识别"""
        self.is_running = False