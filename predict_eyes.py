from imutils.video import VideoStream
from imutils import face_utils
import argparse
import imutils
import time
import dlib
import cv2

#khởi tạo dò tìm khuôn mặt và tải model dự đoán
print("[INFO] loading facial landmark predictor and eye predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('D:/Hoc_Tap/Ki2_Nam3/PBL5/code/eye_predictor.dat')

# khởi tạo luồng đọc video
print("[INFO] loading camera...")
vs = cv2.VideoCapture('D:/Hoc_Tap/Ki2_Nam3/PBL5/Video/409252317403603954.mp4')

count = 0
# lặp qua các frames từ video stream
while True:
	#lấy khung , resize về chiều rộng 400pixel chuyển sanh ảnh xám
	ret, frame = vs.read()
	frame = imutils.resize(frame, width=400)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
  # detect khuôn mặt theo ảnh xám
	count += 1
	rects = detector(gray, 0)
	print(len(rects))
	if len(rects) == 0:
		cv2.imwrite('D:/Hoc_Tap/Ki2_Nam3/PBL5/code/image_error/{}.jpg'.format(count), gray)

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

		left_eye = shape[0:6,0:2]
		
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