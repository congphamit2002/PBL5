from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
from threading import Thread
import dlib
import cv2
from tkinter import *
from tkinter import ttk
import requests
import json
import os
import playsound

# Cau hinh duong dan den file warning.wav
wav_path = "D:/Hoc_Tap/Ki2_Nam3/PBL5/code/warning.wav"

# Ham phat ra am thanh
def play_sound(path):
	os.system('aplay ' + path)

#Ham tinh distance 2 diem
def e_distance(pA, pB):
    return np.linalg.norm(pA - pB)

def eye_ratio(eye):
    #tinh distance theo chieu doc mi tren va mi duoi
    distance_V1 = e_distance(eye[1], eye[5])
    distance_V2 = e_distance(eye[2], eye[4])

    #Tinh distance theo chieu ngang 2 duoi mat
    distance_H = e_distance(eye[0], eye[3])

    #Tinh eye ratio
    eye_ratio_val = (distance_V1 + distance_V2) / (2.0 * distance_H)
    return eye_ratio_val

#Threshold 
eye_ratio_threshold = 0.2

#So frame lien tuc nham mat
max_sleep_frames = 15


#Flag canh bao 
flag = False

# khởi tạo đối số
# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--shape-predictor", required=True,
# 	help="path to facial landmark predictor")
# args = vars(ap.parse_args())

def startDetect(token):
	#khởi tạo dò tìm khuôn mặt và tải model dự đoán
	print("[INFO] loading facial landmark predictor and eye predictor...")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor('D:/Hoc_Tap/Ki2_Nam3/PBL5/code/eye_predictor.dat')

	# khởi tạo luồng đọc video
	print("[INFO] loading camera...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

	isSendApi = True
	i_frame = 0
        
	#Dem so frame ngu gat
	sleep_frames = 0
	# lặp qua các frames từ video stream
	while True:
		#lấy khung , resize về chiều rộng 400pixel chuyển sanh ảnh xám
		frame = vs.read()
		i_frame += 1
		if i_frame % 20 == 0:
			frame = imutils.resize(frame, width=300)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# detect khuôn mặt theo ảnh xám
			rects = detector(gray, 0)

		# lặp qua khuôn mặt đã detect 
			for rect in rects:
				#chuyển đổi bounding box của dlib sang bounding box của open cv 
				#vẽ bounding box 
				(x, y, w, h) = face_utils.rect_to_bb(rect)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

				#sử dụng custom predict để dự đoán vị trí của mắt
				# convert chúng sang numpy array
				shape = predictor(gray, rect)
				shape = face_utils.shape_to_np(shape)
				
				#lay toa do mat trai va mat phai
				left_eye = shape[0:6, 0:2]
				right_eye = shape[6:12, 0:2]

				#lay eye_ratio hai mat
				left_eye_ratio = eye_ratio(left_eye)
				right_eye_ratio = eye_ratio(right_eye)
				# right_eye_ratio = 0

				average = (left_eye_ratio + right_eye_ratio) / 2.0

				if average < eye_ratio_threshold:
					sleep_frames += 1

					if sleep_frames >= max_sleep_frames:
						# Ve dong chu canh bao
						cv2.putText(frame, "WARNING!!!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
						if isSendApi == True:
							print('Send API with token',str(token).strip(),'.')
							requests.post('https://pbl5-api.onrender.com/api/sendwarning',headers={'Content-Type':'application/json','Authorization': 'Bearer {}'.format(token)})
							isSendApi  = False

							# Tien hanh phat am thanh trong 1 luong rieng
							t = Thread(target=play_sound, args=(wav_path,))
							t.daemon = True
							t.start()
							
				else:
					isSendApi = True
					sleep_frames = 0
					cv2.putText(frame, "EYE AVG RATIO: {:.3f}".format(average), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)


				#lặp qua các cặp tọa độ (x, y) và vẽ chúng
				for (sX, sY) in shape:
					cv2.circle(frame, (sX, sY), 1, (0, 0, 255), -1)

		# hiển thị frame
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
			# bấm q để kết thúc
			if key == ord("q"):
				break
	# đóng luồng
	cv2.destroyAllWindows()
	vs.stop()


class Authentication:
    user = 'admin'
    passw = 'admin'
    def __init__(self,root):

        self.root = root
        self.root.title('USER AUTHENTICATION')

        '''Make Window 10X10'''

        rows = 0
        while rows<10:
            self.root.rowconfigure(rows, weight=1)
            self.root.columnconfigure(rows, weight=1)
            rows+=1

        '''Username and Password'''

        frame = LabelFrame(self.root, text='Login', width=300, height=200)
        frame.grid(row = 1,column = 1,columnspan=20,rowspan=20)

        Label(frame, text = ' Usename ').grid(row = 2, column = 1, sticky = W)
        self.username = Entry(frame)
        self.username.grid(row = 2,column = 2)

        Label(frame, text = ' Password ').grid(row = 5, column = 1, sticky = W)
        self.password = Entry(frame, show='*')
        self.password.grid(row = 5, column = 2)

        # Button

        ttk.Button(frame, text = 'LOGIN',command = self.login_user).grid(row=7,column=2)
        '''Message Display'''
        self.message = Label(text = '',fg = 'Red')
        self.message.grid(row=9,column=6)


    def login_user(self):
        '''Check username and password entered are correct'''
        if self.username.get() != "" and self.password.get() != "":
            print('username ' + self.username.get())
            print('password ' + self.password.get())
            username = self.username.get()
            password = self.password.get()
            response = requests.post('https://pbl5-api.onrender.com/api/login', data = {'email': username, 'password': password})
            status = response.status_code
            data = json.loads(response.text)
            token = data['token']
            print("Token: ", token)
            if(token != '' and status == 200):
                  root.destroy()
                  startDetect(token=token)
				

        else:
            self.message['text'] = 'Username or Password incorrect. Try again!'


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x250')
    application = Authentication(root)
    root.mainloop()