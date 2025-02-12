import win32com.client

class TextToSpeech:
    def __init__(self):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
        # 获取所有可用的语音
        self.voices = self.speaker.GetVoices()
        
        # 设置默认语音（可以根据需要选择不同的语音）
        for voice in self.voices:
            if 'English' in voice.GetDescription():
                self.speaker.Voice = voice
                break

    def speak(self, text):
        """将文本转换为语音"""
        try:
            self.speaker.Speak(text)
        except Exception as e:
            print(f"语音合成错误: {e}") 