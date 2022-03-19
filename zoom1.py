from vidstream import *
from kivymd.app import MDApp
import socket
import threading
import requests
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRound
from kivy.lang import Builder

local_ip_adress = "127.0.0.1"
print(local_ip_adress)
server = StreamingServer(local_ip_adress,7777)
receiver = AudioReceiver(local_ip_adress,5555)

kv = '''
BoxLayout:
    orientation:"vertical"
    MDToolbar:
        title:"Zoom App"
        left_action_items:[['menu']]
        right_action_items:[['dots-vertical']]
        pos_hint:{"top":1}
    MDTextFieldRound:
        hint_text: "Target ip address "
        id:ip
    MDFlatButton:
        text:"Start listenning"
        on_release:app.start_listening()
    MDFlatButton:
        text:"Start audio stream"
        on_release:app.start_Audio_streaming()
    MDFlatButton:
        text:"Start camera stream"
        on_release:app.start_camera_streaming()
    MDFlatButton:
        text:"Start screens sharing"
        on_release:app.start_screen_sharing()
'''
class ZoomApp(MDApp):
    def build(self):
        return Builder.load_string(kv)
    
    def start_listening(self):
        self.t1 = threading.Thread(target=server.start_server)
        self.t2 = threading.Thread(target=receiver.start_server)
        
        self.t1.start()
        self.t2.start()
        
    def start_camera_streaming(self):
        self.camera_client = CameraClient("127.0.0.1",9999)
        self.t3 = threading.Thread(target=self.camera_client.start_stream)
        self.t3.start()
    
    def start_screen_sharing(self):
        self.screen_client = ScreenShareClient("127.0.0.1",9999)
        self.t4 = threading.Thread(target=self.screen_client.start_stream)
        self.t4.start()
        
    def start_Audio_streaming(self):
        self.audio_client = AudioSender("127.0.0.1",6424)
        self.t5 = threading.Thread(target=self.audio_client.start_stream)
        self.t5.start()
        
        
if __name__ == "__main__":
    ZoomApp().run()
        