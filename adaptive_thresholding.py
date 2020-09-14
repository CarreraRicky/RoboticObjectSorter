import cv2
import threading
import numpy as np
import serial

connected = False
ser = serial.Serial("com4",115200)

# events = [i for  i in dir(cv2) if "EVENT" in i ] # loop through the entire cv2 package
# print(events, "\n")
def handle_data(data):
    print(data)

def read_from_port(ser):
    global connected
    while not connected:
        #serin = ser.read()
        connected = True

        while True:
           reading = ser.readline().decode()
           handle_data(reading)

thread = threading.Thread(target=read_from_port, args=(ser,))
thread.start()

def mouse_click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: # when the left mouse is click on image, will give x and y coords on image
        # print(x, ",", y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        str_XY = str(x) + "," + str(y) + '\n'
        # x_coord = str(x) + ' '
        # y_coord = str(y) + ' '
        # ser.write(str.encode(x_coord))
        # ser.write(str.encode(y_coord))
        ser.write(str.encode(str_XY))
        print_text = cv2.putText(frame,str_XY, (x,y), font, 0.5, (255,255,0), 2)
        show_image = cv2.imshow("image window", frame)

capture = cv2.VideoCapture(0)
while True:
    frame = cv2.imread("C:/Dev/ComputerVision/smarties.png")
    # blurred_frame = cv2.GaussianBlur(frame, (5,5), 0) # reduces background noise.
    # _, frame = capture.read()
    blurred_frame = cv2.GaussianBlur(frame, (5,5), 0) # reduces background noise.

    # coverting BGR to HSV
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # Blue range
    blue_lower = np.array([100,50,50])
    blue_upper = np.array([150,255,255])

    # Red range
    # lower mask (0-10)
    # lower_red = np.array([0,50,50])
    # upper_red = np.array([10,255,255])
    # mask0 = cv2.inRange(frame, lower_red, upper_red)

    lower_red = np.array([160,50,50])
    upper_red = np.array([179,255,255])

    # upper mask (170-180)
    # lower_red = np.array([170,50,50])
    # upper_red = np.array([180,255,255])
    # mask1 = cv2.inRange(frame, lower_red, upper_red)

    # Green range
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])

    # Thresholding the image to specific colors
    mask = cv2.inRange(hsv,blue_lower, blue_upper)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel,iterations = 2)
    mask = cv2.dilate(mask, kernel, iterations = 2)

    contours,hierachy= cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 2200:
            cv2.drawContours(frame, contours, -1, (0,255,0), 3)

        # calculate moments for each contour
        m = cv2.moments(contour)
        if m['m00']!= 0:
            # calculate x,y coordinate of center
            cX = int(m["m10"]/m["m00"])
            cY = int(m["m01"]/m["m00"])
            # cv2.circle(frame, (cX,cY),5,(255,255,255),-1)
            # cv2.putText(frame, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        else:
            cX,cY = 0,0

        cv2.circle(frame, (cX,cY),5,(0,255,255),-1)
        cv2.putText(frame, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 2)

    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    cv2.setMouseCallback("frame", mouse_click_event) # used to call our mouse_click_event function

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
# points = [] # will store the different points we put on the image
# print(points)
cv2.destroyAllWindows()