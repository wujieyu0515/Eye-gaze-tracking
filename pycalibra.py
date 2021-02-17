import pygame
from pygame.locals import *
import sys
import cv2


def run_calibration(screen,webcam, gaze,cali_settings):

    left_cali_temp = []
    right_cali_temp = []
    left_inner_temp = []
    right_inner_temp = []

    count = 0

    for point in cali_settings.point_pos:
        for x,y in point:
            pygame.draw.circle(screen, cali_settings.black, (x, y), cali_settings.point_r, 2)
            pygame.display.flip()
            check_events(screen, x, y, cali_settings,webcam,gaze,count,left_cali_temp,right_cali_temp,
                         left_inner_temp,right_inner_temp)
            left_cali_temp = []
            right_cali_temp = []
            left_inner_temp =[]
            right_inner_temp =[]

            count += 1


def check_events(screen, x, y, cali_settings,webcam,gaze,count,left_cali_temp,right_cali_temp,
                         left_inner_temp,right_inner_temp):
    # process all events
    while True:
        # We get a new frame from the webcam
        _, frame = webcam.read()
        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame,(left_x,left_y),(right_x,right_y) = gaze.annotated_frame()
        left_cali_temp.append((left_x,left_y))
        right_cali_temp.append((right_x,right_y))
        if gaze.eye_left.inner :
            left_inner_temp.append(gaze.eye_left.inner )
        if gaze.eye_right.inner :
            right_inner_temp.append(gaze.eye_right.inner)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos_x, mpos_y = pygame.mouse.get_pos()
                cali_settings.mouse_pos.append([mpos_x,mpos_y])
                cali_settings.left_cali.append(get_cali_pos(left_cali_temp))

                cali_settings.right_cali.append(get_cali_pos(right_cali_temp))
                cali_settings.left_inner.append(get_cali_pos(left_inner_temp))

                cali_settings.right_inner.append(get_cali_pos(right_inner_temp))

                if check_click(x,y,mpos_x, mpos_y,cali_settings,screen,count):
                    return

def get_cali_pos(temp):
    x = 0
    y = 0
    for i,j in temp:
        x += i
        y += j
    try:
        x = int(x/len(temp))
        y= int(y/len(temp))
        return (x,y)
    except ZeroDivisionError:
        return None

def check_click(x,y,mpos_x,mpos_y,cali_settings,screen,count):
    if (x - 2 * cali_settings.point_r <= mpos_x <= x + 2 * cali_settings.point_r) \
            and (y - 2 * cali_settings.point_r <= mpos_y <= y + 2 * cali_settings.point_r) \
            and cali_settings.left_cali[count] and cali_settings.right_cali[count] :

        pygame.draw.circle(screen, cali_settings.black, (x, y), cali_settings.point_r, 0)
        update_screen(screen, cali_settings)

        return True

def update_screen(screen,cali_settings):
    pygame.display.flip()
    pygame.time.wait(1000)
    screen.fill(cali_settings.white)
    pygame.display.flip()
    pygame.time.wait(1000)


class Settings():
    def __init__(self):
        self.white = (255, 255, 255)
        self.black = (0,0,0)
        self.point_r =22
        self.point_margin_x = 440  # number of pixels to the left and right
        self.point_margin_y = 200  # number of pixels to the top and bottom
        self.screenpad_x = 175  # number of pixels between the point and the left and right of the window
        self.screenpad_y = 175  # number of pixels between the point and the top and bottom of the window
        self.point_pos = self.get_point_pos()
        self.left_cali = []
        self.right_cali =[]
        self.left_inner = []
        self.right_inner =[]
        self.mouse_pos =[]


    def get_point_pos(self):
        point = []
        for y in range(3):
            row = []
            for x in range(3):
                row.append([x * (self.point_r + self.point_margin_x) + self.screenpad_x,
                            y * (self.point_r + self.point_margin_y) + self.screenpad_y])
            point.append(row)

        return point








