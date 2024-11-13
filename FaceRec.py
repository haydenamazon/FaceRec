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

#Initialize webcam
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
        "audio": pygame.mixer.Sound('/home/hayden/Downloads/AudioTriggers/eftrimmed.mp3')
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
    },
    "HannahKermicle": {
        "first_identify": True,
        "reset": None,
        "timer": 10,
        "audio": pygame.mixer.Sound('/home/hayden/Downloads/AudioTriggers/hmctrimmed.mp3')
    }
}
known_face_names = remove_numbers_from_strings(known_face_names)

#REMOVE LINES TO HAVE DEFAULT FEED SIZE (1/2)
cv2.namedWindow("FaceRec", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("FaceRec", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
screen_width, screen_height = pyautogui.size()
#############################################
#THESE LINES MUST BE HERE AS WEBCAM WILL FAULT OPEN AS IT MUST WAIT TILL AFTER TRAINING SESH

#TOLERANCE FOR FACE RECOGNITION. LOWER NUMBER = STRICTER TOLERANCE. HIGHER NUMBER = LESS TOLERANCE
tolerance = 0.55 

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    current_time = datetime.now().strftime("%H:%M")
    #Line below necessary to flip webcam feed. Removing the line makes it act as a camera instead of a mirror.
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)

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
        # Draw a box around the face
        if name == "Unknown":
            box_color = (0, 0, 255)
        elif name in high_priority:
            box_color = (255, 0, 0)
        else:
            box_color = (0, 255, 0)
        #Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), box_color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    #REMOVE LINES TO HAVE DEFAULT FEED SIZE (2/2)
    frame_height, frame_width = frame.shape[:2]
    scale = min(screen_width / frame_width, screen_height / frame_height)
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)
    resized_frame = cv2.resize(frame, (new_width, new_height))

    screen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
    y_offset = (screen_height - new_height) // 2
    x_offset = (screen_width - new_width) // 2
    screen[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_frame
    #############################################
    # Display the frame in full screen
    cv2.imshow("FaceRec", screen)

    #Hit 'q' on the keyboard to quit!
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
