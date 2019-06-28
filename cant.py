import cv2
import numpy as np
from pyzbar import pyzbar
import pygame
import datetime




def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_PLAIN
    Results, Eleves = [], []
    pygame.mixer.init()
    pygame.mixer.music.load("beep.mp3")

    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        #cv2.imshow('my webcam', img)
        decodedObjects = pyzbar.decode(cv2.flip(img, 1))
        for obj in decodedObjects:
            if obj.data not in Eleves:
                pygame.mixer.music.play()
                eleve = obj.data.decode("utf-8")
                Eleves.append(obj.data)
                ligne = datetime.datetime.now().strftime("%d/%m;%H:%M:%S")+";"+eleve
                print(ligne)
                Results.append(ligne)
            cv2.putText(img, str(obj.data), (50, 50), font, 2,
                        (255, 0, 0), 3)
        if cv2.waitKey(1) == 27:
            print(Results)
            break  # esc to quit
    


def main():
    show_webcam(mirror=True)
main()
