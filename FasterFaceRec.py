#!/usr/bin/env python3
import face_recognition
import cv2
import numpy as np

import pygame
pygame.mixer.init()
import pyautogui
import os
import time
from datetime import datetime, timedelta, date
#from playsound import playsound
#import threading
import re

#Initialize Webcam
video_capture = cv2.VideoCapture(0)
faces_folder = "faces"

known_face_encodings = []
known_face_names = []

#Parses through each image file (jpg, jpeg, and png) in the folder
for filename in os.listdir(faces_folder):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(faces_folder, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)
        if face_encoding:
            known_face_encodings.append(face_encoding[0])
            #The filename will be used as the person's name
            name = os.path.splitext(filename)[0]
            known_face_names.append(name)

#Two arrays to holder information about face encosings and face locations. These are large data sets which provide numeric mappings of face
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

#We are going to create a file name "face_recognition_log" which stores logs of passerbys. This can be set to all or only recognied individuals
# EXP. Log:
#Hayden detected at 2024-10-06 14:24:19
log_file = "face_recognition_log.csv"

def log_detection(name):
    """Log the name and timestamp of the detected face."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"{name} detected at {timestamp}\n")

#Since we have the filepath denoted to the name, we need a function to clean it up. This will remain all characters and numbers
def remove_numbers_from_strings(array):
    #Iterate through each string in the array
    return [re.sub(r'\d+', '', string) for string in array]

#This section is denoted to high priority individuals.
#Contained within "#" will be all the needed code per high priority person
######################################################################
high_priority = {
    "Amazon": {
        "first_identify": True,
        "reset": None,
        "timer": 10,
        "audio": pygame.mixer.Sound('/home/hayden/Downloads/AudioTriggers/bbtrimmed.mp3')
    },
    "JesseSowell": {
        "first_identify": True,
        "reset": None,
        "timer": 10,
        "audio": pygame.mixer.Sound('/home/hayden/Downloads/AudioTriggers/ecjsp.mp3')
    },
    "BobAllen": {
        "first_identify": True,
        "reset": None,
        "timer": 10,
        "audio": pygame.mixer.Sound('/home/hayden/Downloads/AudioTriggers/swdvtrimmed.mp3')
    },
    "JacobRegnier": {
        "first_identify": True,
        "reset": None,
        "timer": 10,
        "audio": pygame.mixer.Sound('/home/hayden/Downloads/AudioTriggers/tibtrimmed.mp3')
    }
}

known_face_names = remove_numbers_from_strings(known_face_names)

while True:
    #Grab a single frame of video
    ret, frame = video_capture.read()
    current_time = datetime.now().strftime("%H:%M")
    if process_this_frame:
        #Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            #See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            ####Uncomment the line below to record all individuals, even unknown####
            #log_detection(name)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                #Record only people in database
                log_detection(name)
                #   *SPECIAL CASES*
                if name in high_priority:
                    rec = high_priority[name]
                    if rec["first_identify"]:
                        rec["first_identify"] = False
                        rec["reset"] = time.time()
                        rec["audio"].play()
                    if not rec["first_identify"] and rec["reset"] is not None:
                        if time.time() - rec["reset"] >= rec["timer"]:
                            rec["first_identify"] = True
            face_names.append(name)

    process_this_frame = not process_this_frame
    #Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        #If name is Unknown, box around face will display RED, otherwise box displays GREEN
        if name == "Unknown":
            box_color = (0, 0, 255)
        elif name in high_priority:
            box_color = (255, 0, 0)
        else:
            box_color = (0, 255, 0)
        #Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

        #Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), box_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    #Display the resulting image
    cv2.imshow('Video', frame)

    #If thekeystroke 'q' is entered, the code will break manually. However the if statement below will automatically close the program at 23:59 or 11:59pm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if current_time == "23:59":
        print("CLOSING APPLICATION")
        pyautogui.press('q')
        break
#Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

#This will run upon closing of the webcam. The code below acts to consolidate the appended log file
time.sleep(2)
today = date.today()

#Input and output file paths
input_file = "face_recognition_log.csv"
output_file = "log_" + str(today) + ".csv"

#Time threshold to consider similar entries (within 'x' seconds)
TIME_THRESHOLD = timedelta(seconds=10)

def consolidate_logs(input_file, output_file):
    with open(input_file, "r") as file:
        lines = file.readlines()
    #Dictionary to keep track of the last log time for each person
    last_detected = {}
    with open(output_file, "a") as output:
        for line in lines:
            parts = line.split(" detected at ")
            if len(parts) != 2:
                continue
            person = parts[0]
            timestamp_str = parts[1].strip()
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

            #Check if the person has been detected recently
            if person in last_detected:
                last_time = last_detected[person]
                if timestamp - last_time < TIME_THRESHOLD:
                    continue
            #Write the consolidated log entry
            output.write(f"{person} detected at {timestamp_str}\n")
            #Update the last detected time for the person
            last_detected[person] = timestamp

    print(f"Consolidation complete! Check {output_file} for the result.")
consolidate_logs(input_file, output_file)
#Clear log file for the day
open('face_recognition_log.csv', 'w').close()
