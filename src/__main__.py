from .utils.audio import record, to_text
from .utils.img_capture import img_capture, webcam_capture
from .utils.gemini import gemini_response
from .utils.tts import tts

import os


def main():
    while True:
        record('output.wav')
        text = to_text('output.wav')
        if text:
            print(text)
            # img = img_capture()
            img = webcam_capture('http://172.18.234.240:8080/video')
            response = gemini_response(img=img,text=text)
            tts(response)
            # os.remove('frame.png')
            # os.remove('output.wav')
        

if __name__ == "__main__":
    main()