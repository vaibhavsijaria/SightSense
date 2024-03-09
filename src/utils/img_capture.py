import cv2
from PIL import Image


def img_capture():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_frame)
    img.save('frame.png')
    cap.release()
    cv2.destroyAllWindows()
    return img

def webcam_capture(ip_camera_url: str):
    print('Capturing Frame ...')
    cap = cv2.VideoCapture(ip_camera_url)

    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(rgb_frame)
    img.save('frame.png')
    cap.release()
    cv2.destroyAllWindows()

    return img
