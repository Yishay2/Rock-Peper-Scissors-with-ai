import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time


# 0 is for the web camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# identify hands gesture
detector = HandDetector(maxHands=1)

timer = 0
state_result = False
start_game = False
scores = [0,0]

while sum(scores) < 5:
    imgbg = cv2.imread("./Resources/BG.png")
    success, img = cap.read()

    # resize the image captured by the web camera to 87.5% from the original size
    imgscale = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgscale = imgscale[:,80:480]

    # create Game
    hands, img = detector.findHands(imgscale)
    if start_game:
        if state_result is False:
            timer = time.time()- initialTime
            cv2.putText(imgbg, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255))
            if timer > 3:
                state_result = True
                timer = 0
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    random_number = random.randint(1, 3)
                    imgAi = cv2.imread(f"./Resources/{random_number}.png", cv2.IMREAD_UNCHANGED)
                    imgbg = cvzone.overlayPNG(imgAi, imgbg, (0, 255))

                    # Game Result
                    if playerMove == 1 and random_number == 3 or\
                            playerMove == 2 and random_number == 1 or\
                            playerMove == 3 and random_number == 2:
                                scores[1] += 1

                    if playerMove == 3 and random_number == 1 or\
                        playerMove == 1 and random_number == 2 or\
                            playerMove == 2 and random_number == 3:
                             scores[0] += 1

                    imgbg[234:654, 795:1195] = imgscale
                    if state_result:
                        imgbg = cvzone.overlayPNG(imgbg, imgAi)

    cv2.putText(imgbg, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgbg, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.imshow("BG", imgbg)
    key = cv2.waitKey(1)
    if key == ord("s"):
        start_game = True
        initialTime = time.time()
        state_result = False

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

if scores[0] > scores[1]:
    print('AI WINS!')
elif scores[0] < scores[1]:
    print("Player WINS!")
else:
    print("TIE!")

