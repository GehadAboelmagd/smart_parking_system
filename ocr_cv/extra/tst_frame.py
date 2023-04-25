import cv2
import ocr_cv
import time
import pytesseract

avg_list = []

# Open the default camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print('Error opening camera')
    exit()

cv2.setNumThreads(2)
print(cv2.getThreadNum())
cv2.ocl.setUseOpenCL(False)

# Read and display frames from the camera
while True:
# Read a frame from the camera
	strt = time.time()
	ret, frame = cap.read()

	if not ret:
		print('Error reading frame')
		break

	frame = cv2.UMat(frame)	

	frame = cv2.medianBlur(frame , ksize= 3 )
	frame = cv2.medianBlur(frame , ksize= 3 )
	frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
	frame = cv2.bitwise_not(frame)
	frame = cv2.threshold(frame , 0 , 255 , cv2.THRESH_BINARY_INV+ cv2.THRESH_OTSU)[1]
	frame = cv2.Laplacian(frame, cv2.CV_8U, ksize=3)

	frame = frame.get()
	imgstr  = pytesseract.image_to_string( frame , lang='eng' ,config= "--psm 6" )
 
	cv2.imshow('Camera', frame)

	end = time.time()	
	frametime = end - strt
	fps = 1 / (frametime + 0.000001)
	print (f"frametime,fps : {frametime} , {fps}")
	avg_list.append(fps)
 
	# Exit the loop if 'q' is pressed
	if cv2.waitKey(1) == ord('q'):
		break

sum , avg = 0 , 0
for i in avg_list :
   sum += i

avg = sum / len(avg_list)
print (f"avg fps: {avg}")
# Release the VideoCapture object and close the window
cap.release()
cv2.destroyAllWindows()