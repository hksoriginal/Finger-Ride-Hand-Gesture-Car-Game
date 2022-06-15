from pynput.keyboard import Key, Controller
import pygame
from pygame.locals import *
from tkinter import *
import cv2
import numpy as np
import handTrackingModule as htm
import random
from PIL import Image, ImageTk
import multiprocessing
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
keyboard = Controller()

# opencv
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = htm.handDetector(detectionCon=0.85)


########################
root = Tk()
root.resizable(False, False)
root.geometry("940x720")
root.title("Finger Ride")
root.iconbitmap('images/icon.ico')


main_frame = Label(root, bg='#333333')
main_frame.place(x=0, y=0, height=720, width=940)

#  display Label
bg_display = Image.open('images/bg.png')
bg_display = bg_display.resize((640, 480), Image.ANTIALIAS)
bg_display = ImageTk.PhotoImage(bg_display)
display_frame = Label(root, image=bg_display)
display_frame.place(x=150, y=150, height=480, width=640)


score_lb = Label(root, bg='#333333', fg='white',
                 text="Hit Play to Start", font='Helvetica 45')
score_lb.place(x=0, y=0, height=100, width=940)
###########################################################
###############


def game():

    score_lb['bg'] = '#333333'

    count = 0
    counts = 0
    flag = True
    key = 0

    # import image

    size = width, height = (800, 800)
    road_w = int(width/1.6)
    roadMark_w = int(width/80)
    right_lane = int(width/2 + road_w/4)
    left_lane = int(width/2 - road_w/4)
    car_pic = (120, 200)
    speed = 1

    pygame.init()
    running = True
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Finger Ride')
    screen.fill((0, 156, 79))

    pygame_icon = pygame.image.load('images/icon.ico')
    pygame.display.set_icon(pygame_icon)

    pygame.display.update()

    # load images
    car = pygame.image.load('hk_car.png')
    car = pygame.transform.scale(car, car_pic)
    car_loc = car.get_rect()
    car_loc.center = right_lane, height*0.8

    car2 = pygame.image.load('ene_car.png')
    car2 = pygame.transform.scale(car2, car_pic)
    car2_loc = car2.get_rect()

    car2_loc.center = left_lane, height*0.2
    score = 0
    counter = 0
    counts = 0

    # game loop
    while running:

        counter += 1
        if counter == 500:
            speed += 0.15
            counter = 0
            # score_lb['text'] = "Leveled Up!"
            print("Level Up", speed)
        # animating enemy
        car2_loc[1] += speed*6
        if car2_loc[1] > height:

            if random.randint(0, 1) == 0:
                car2_loc.center = right_lane, -200

            else:
                car2_loc.center = left_lane, -200

        ################################################################
        success, img = cap.read()
        # img = cv2.flip(img, 1)

        # find hand landmarks
        img = detector.findHands(img)
        myList = detector.findPosition(img, draw=False)

        if(len(myList) != 0):
            # print(myList[8][1:3])
            x, y = myList[8][1:3]
            # print(x, y)
            # print(myList[8][1])

            if counter > 10:
                if(myList[8][1] <= 320):
                    print("Right")
                    # car_loc = car_loc.move([-int(road_w/2), 0])
                    car_loc = car_loc.move([int(road_w/2), 0])
                elif(myList[8][1] > 320):
                    print("Left")
                    # car_loc = car_loc.move([int(road_w/2), 0])
                    car_loc = car_loc.move([-int(road_w/2), 0])
                else:
                    car_loc = car_loc.move([-int(road_w/2), 0])
                    # pygame.display.update()

        # cv2.imshow('image', img)
        # cv2.waitKey(0)

        # cropped Face image
        # img = cv2.flip(img, 1)
        cropped_face = img
        cropped_face = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
        cropped_array = ImageTk.PhotoImage(Image.fromarray(cropped_face))
        display_frame['image'] = cropped_array
        root.update()

        ################################################################

        # game logic

        if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 200:
            print('game over!')
            score_lb['text'] = "Game Over!"
            score_lb['bg'] = 'red'
            break
        # event listener
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # if event.type == KEYDOWN:
            #     if event.key in [K_a, K_LEFT]:
            #         car_loc = car_loc.move([-int(road_w/2), 0])
            # if event.type == KEYDOWN:
            #     if event.key in [K_d, K_RIGHT]:
            #         car_loc = car_loc.move([int(road_w/2), 0])

        pygame.draw.rect(screen, (50, 50, 50),
                         (width/2-road_w/2, 0, road_w, height)
                         )

        pygame.draw.rect(screen, (255, 240, 60),
                         (width/2-roadMark_w/2, 0, roadMark_w, height)
                         )

        pygame.draw.rect(screen, (255, 255, 255),
                         (width/2-road_w/2 + roadMark_w*2, 0, roadMark_w, height)
                         )
        pygame.draw.rect(screen, (255, 255, 255),
                         (width/2+road_w/2 - roadMark_w*3, 0, roadMark_w, height)
                         )

        screen.blit(car, car_loc)
        screen.blit(car2, car2_loc)
        if car2_loc[1] == height-50:
            score += 1
            score_lb['text'] = 'Score: ' + str(score)
            root.update()

        pygame.display.update()

    pygame.quit()


    # play Button
play_btn = Image.open('images/play.png')
play_btn = play_btn.resize((150, 50), Image.ANTIALIAS)
play_btn = ImageTk.PhotoImage(play_btn)
gplay_btn = Button(main_frame, command=game, image=play_btn, cursor="hand2",
                   relief='flat')
gplay_btn.place(x=400, y=660, width=140, height=40)
root.mainloop()
