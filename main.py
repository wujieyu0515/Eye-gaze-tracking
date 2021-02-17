import cv2
from gaze_tracking import GazeTracking
import pygame
import pycalibra
from pycalibra import Settings
import fitting
import os
import sys

gaze = GazeTracking()
cali_flag = True
cali_settings = Settings()

webcam = cv2.VideoCapture(0)
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
# create the WINDOW
screen = pygame.display.set_mode((1280, 800))
screen.fill(cali_settings.white)
pygame.display.set_caption('Calibration')

if cali_flag:
    pycalibra.run_calibration(screen,webcam,gaze,cali_settings)
    cali_flag = False


left_screen_x_model = fitting.cali_fitting(cali_settings.left_cali, cali_settings.left_inner,
                                           cali_settings.mouse_pos,0)
right_screen_x_model = fitting.cali_fitting(cali_settings.right_cali, cali_settings.right_inner,
                                            cali_settings.mouse_pos, 0)
left_screen_y_model = fitting.cali_fitting(cali_settings.left_cali, cali_settings.left_inner,
                                           cali_settings.mouse_pos, 1)
right_screen_y_model = fitting.cali_fitting(cali_settings.right_cali, cali_settings.right_inner,
                                            cali_settings.mouse_pos, 1)
while True:

    _, frame = webcam.read()
    gaze.refresh(frame)
    frame, (left_x, left_y), (right_x, right_y) = gaze.annotated_frame()
    if left_x and left_y and right_x and right_y and gaze.eye_left.inner and gaze.eye_right.inner :
        left_mat = fitting.get_matrix(left_x,left_y,gaze.eye_left.inner[0],gaze.eye_left.inner[1])
        right_mat = fitting.get_matrix(right_x,right_y,gaze.eye_right.inner[0],gaze.eye_right.inner[1])
        left_screen_x = left_screen_x_model.predict([left_mat])
        left_screen_y = left_screen_y_model.predict([left_mat])
        right_screen_x = right_screen_x_model.predict([right_mat])
        right_screen_y = right_screen_y_model.predict([right_mat])
        draw_x = fitting.get_mid(left_screen_x, right_screen_x)
        draw_y = fitting.get_mid(left_screen_y, right_screen_y)
        pygame.draw.circle(screen, cali_settings.black, (draw_x, draw_y), 5, 0)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
    pygame.display.flip()









""" 
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()

    text = ""
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    """
    # cv2.imshow("Demo", frame)
    #if cv2.waitKey(1) == 27:
     #   break