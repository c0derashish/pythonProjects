from deepface import DeepFace
import cv2
import numpy as np
import csv
import os
from datetime import datetime

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Load known faces from a dictionary
known_faces = {}

# List of students
students = list(known_faces.keys())

# Get current date for CSV
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
f = open(rf"F:\Ultimate\arpita\project\attendance\{current_date}.csv", "w+", newline="")
lnwriter = csv.writer(f)
lnwriter.writerow(["Name", "Time"])

def capture_new_student():
    name = input("Enter new student's name: ")
    image_path = rf"F:\Ultimate\arpita\project\faces\{name}.jpg"
    
    print("Capturing image...")
    ret, frame = video_capture.read()
    if ret:
        cv2.imwrite(image_path, frame)
        known_faces[name] = image_path
        print(f"New student {name} added successfully!")
    else:
        print("Error capturing image!")
    return

def scan_faces():
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        cv2.imwrite("temp.jpg", frame)
        
        for name, img_path in known_faces.items():
            try:
                result = DeepFace.verify("temp.jpg", img_path, model_name="VGG-Face", enforce_detection=False)
                if result["verified"]:
                    print(f"{name} is recognized!")
                    lnwriter.writerow([name, datetime.now().strftime("%H:%M:%S")])
                    cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Attendance", frame)
                    cv2.waitKey(100)  # Show the recognized face for 2 seconds
                    return
                    
            except Exception as e:
                print("Error in DeepFace verification:", e)
        else :
            print("User is not in Student Data!")
            return

def remove_student() :
    name = input("Enter student's name: ")
    image_path = rf"F:\Ultimate\arpita\project\faces\{name}.jpg"
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"{name} is removed.")
        try :
            del known_faces[name]
        except: pass
    else :
        print("User is not in Student Data!")
        return

    

def main_menu():
    while True:
        print("\nMenu:")
        print("1. Scan face")
        print("2. Add new student")
        print("3. Remove a student")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            scan_faces()
        elif choice == "2":
            capture_new_student()
        elif choice == "3" :
            remove_student()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")

main_menu()

video_capture.release()
cv2.destroyAllWindows()
f.close()

