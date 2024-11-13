#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os
from collections import defaultdict
from datetime import date
today = date.today()

def list_log_files(folder_path):
    try:
        #Get the list of all files and folders in the specified directory
        contents = os.listdir(folder_path)
       
        #Filter the contents to include only files starting with "log_"
        log_files = [file for file in contents if file.startswith("log_")]
       
        if log_files:
            print("Current logs.\n")
            for file in log_files:
                print(file)
        else:
            print(f"No files starting with 'log_' were found in '{folder_path}'.")
    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied to access '{folder_path}'.")

folder_path = '/home/hayden/Downloads'
list_log_files(folder_path)

print("Example .csv log name: log_2024-10-12.csv (year, month, day)")
output = input("Enter log date here: ")
output_file = '/home/hayden/Downloads/' + output
name_counts = defaultdict(int)

with open(output_file, 'r', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        if row:
            #Split the line by 'detected at' to extract the name
            name = row[0].split(' detected at')[0]
            #Increment the count for the detected name
            name_counts[name] += 1
#Append the counts to the same CSV file
with open(output_file, 'a', newline='') as file:
    writer = csv.writer(file)
    #Write a blank row to separate the data and the counts
    writer.writerow([])
    writer.writerow(["Name detection counts:"])
    
    #Write each name and its count to the CSV
    for name, count in name_counts.items():
        writer.writerow([f"{name} detected {count} times"])
        
