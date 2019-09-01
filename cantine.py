import pygame
import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk
from pyzbar import pyzbar
import datetime
import os

Eleves = []
Results = []

auj_file_name = datetime.datetime.now().strftime("%Y%m%d")+"_cantine.csv"
if auj_file_name in os.listdir("."):
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    os.rename(auj_file_name, auj_file_name+now)

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Cantine")
window.config(background="#FFFFFF")

valide = 0

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)


#Capture video frames
box = tk.Listbox(imageFrame)
box.pack()
cap = cv2.VideoCapture(0)

def show_frame():
    global Eleves, Results, valide, etat, box
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    def toggleVideo(e):
        global cap, box, etat
        etat = 1-etat
    if etat:
        cv2.imshow('Image actuelle', frame)
    else:
        cv2.destroyAllWindows()
    box.bind("v", toggleVideo)

    img = frame
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    decodedObjects = pyzbar.decode(cv2.flip(img, 1))
    for obj in decodedObjects:
        if obj.data not in Eleves:
            #pygame.mixer.music.play()
            eleve = obj.data.decode("utf-8")
            Eleves.append(obj.data)
            ligne = datetime.datetime.now().strftime("%d/%m;%H:%M:%S")+";"+eleve
            file = open(auj_file_name, "a")
            file.write(ligne+"\n")
            file.close()
            box.insert(tk.END, eleve)
            Results.append(ligne)
            box.config(background="green")
    if valide == 10:
        box.config(background="#FFFFFF")
        valide = 0
    else:
        valide += 1
    box.after(100, show_frame)


etat = 0
show_frame()  #Display 2
window.mainloop()  #Starts GUI
