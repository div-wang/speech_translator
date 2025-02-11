from aip import AipSpeech
import numpy as np
import time
import json
import websocket
import threading
import base64
import hmac
import hashlib
import datetime
import urllib.parse

class RealtimeSpeechRecognizer:
    def __init__(self, app_id, api_key, secret_key):
        self.app_id = app_id
        self.api_key = api_key
        self.secret_key = secret_key
        self.ws = None
        self.is_running = False
        self.on_result = None
        
    def _generate_url(self):
        # 生成鉴权url
        url = 'wss://vop.baidu.com/realtime_asr'
        now = datetime.datetime.now()
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        token = base64.b64encode(hmac.new(
            self.secret_key.encode(),
            f'date: {date}'.encode(),
            hashlib.sha256
        ).digest()).decode()
        
        authorization = f'speak {self.api_key}:{token}'
        url_params = {
            'authorization': authorization,
            'date': date,
            'app_id': self.app_id,
            'dev_pid': 1537  # 中英文混合识别
        }
        return f"{url}?{urllib.parse.urlencode(url_params)}"

    def _on_message(self, ws, message):
        try:
            result = json.loads(message)
            if result.get('type') == 'final_result':
                text = json.loads(result['result'])['hypotheses'][0]['transcript']
                if self.on_result and text.strip():
                    self.on_result(text)
        except Exception as e:
            print(f"处理消息错误: {e}")

    def _on_error(self, ws, error):
        print(f"WebSocket错误: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("WebSocket连接关闭")

    def _on_open(self, ws):
        print("WebSocket连接已建立")
        
    def start(self, callback):
        """开始实时语音识别"""
        self.on_result = callback
        self.is_running = True
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self._generate_url(),
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def send_audio(self, audio_data):
        """发送音频数据"""
        if self.ws and self.ws.sock and self.ws.sock.connected:
            try:
                # 将numpy数组转换为base64编码
                audio_bytes = audio_data.tobytes()
                audio_base64 = base64.b64encode(audio_bytes).decode()
                data = json.dumps({
                    "type": "audio_data",
                    "data": audio_base64
                })
                self.ws.send(data)
            except Exception as e:
                print(f"发送音频数据错误: {e}")

    def stop(self):
        """停止语音识别"""
        self.is_running = False
        if self.ws:
            self.ws.close() 