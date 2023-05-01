import numpy as np
import cv2

oldx = oldy = -1                                                                            #지역 변수 선언
color = (0, 0, 255)
thickness = 4
eraser_size = 20
mode = 'draw'

def on_mouse(event, x, y, flags, param):                                                    #마우스 함수
    global oldx, oldy, color, thickness, mode                                               #밖에 있는 변수 불러오기

    if event == cv2.EVENT_LBUTTONDOWN:                                                      #왼쪽 마우스가 눌러지면 실행
        if mode == 'draw':                                                                  #모드 값이 draw면 실행
            oldx, oldy = x, y                                                               #oldx에 x를 oldy에 y를 받음
        elif mode == 'erase':                                                               #모드 값이 'erase' 면 실행
            cv2.circle(img, (x, y), eraser_size, (255, 255, 255), -1)                       #지우게가 될 투명원을 생성
            cv2.imshow('image', img)

    elif event == cv2.EVENT_LBUTTONUP:                                                      #마우스 클릭을 땠을때 실행
        print('EVENT_LBUTTONUP: %d, %d' % (x, y))                                           #마우스 땠을때 좌표를 출력

    elif event == cv2.EVENT_MOUSEMOVE:                                                      #마우스가 움직일때 발생
        if flags & cv2.EVENT_FLAG_LBUTTON:
            if mode == 'draw':                                                              #모드가 draw일때 실행
                cv2.line(img, (oldx, oldy), (x, y), color, thickness, cv2.LINE_AA)          #받은 값을 통해 선 생성
            elif mode == 'erase':                                                           #모드가 erase 일때 실행
                cv2.circle(img, (x, y), eraser_size, (255, 255, 255), -1)
            cv2.imshow('image', img)
            oldx, oldy = x, y

def on_trackbar(val):                                                                       #트렉바 함수
    global color, eraser_size, thickness
    color = (cv2.getTrackbarPos('Blue', 'image'),                                           #변수에 각 색의 트렉바 저장
             cv2.getTrackbarPos('Green', 'image'),
             cv2.getTrackbarPos('Red', 'image'))
    eraser_size = cv2.getTrackbarPos('Eraser Size', 'image')                                #변수에 지우게 크기 트렉바 저장
    thickness = cv2.getTrackbarPos('Thickness', 'image')                                    #변수에 굵이 트렉바 저장

def on_mode_change(val):                                                                    #모드 변경 함수
    global mode                                                                             #밖에 있는 변수 불러오기
    if val == 0:                                                                            #val 값이 0이 되면 실행
        mode = 'draw'                                                                       #mode에 draw 입력
        cv2.setTrackbarPos('Eraser Size', 'image', 20)                                      #지우게 크게 트렉바 설정
    elif val == 1:                                                                          #val 값이 1이 되면 실행
        mode = 'erase'                                                                      #mode에 erase 입력
        cv2.setTrackbarPos('Eraser Size', 'image', 40)                                      #지우게 크게 트렉바 설정

img = np.ones((480, 640, 3), dtype=np.uint8) * 255                                          #켄버스 생성

cv2.namedWindow('image')
cv2.setMouseCallback('image', on_mouse)                                                     #사전에 작성한 마우스 함수 불러옴

cv2.createTrackbar('Red', 'image', 0, 255, on_trackbar)                                     #Red 트렉바 생성
cv2.createTrackbar('Green', 'image', 0, 255, on_trackbar)                                   #Green 트렉바 생성
cv2.createTrackbar('Blue', 'image', 255, 255, on_trackbar)                                  #Blue 트렉바 생성
cv2.createTrackbar('Thickness', 'image', thickness, 10, on_trackbar)                        #굵기 트렉바 생성
cv2.createTrackbar('Eraser Size', 'image', eraser_size, 100, on_trackbar)                   #지우게 크기 트렉바 생성

cv2.createTrackbar('Mode', 'image', 0, 1, on_mode_change)                                   #Mode 트렉바 생성

while True:                                                                                 #값이 True 이면 실행
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):                                                                       #q가 눌러 진다면 중지
        break

cv2.destroyAllWindows()