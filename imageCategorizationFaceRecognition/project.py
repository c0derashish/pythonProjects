import face_recognition
import cv2
import os
import customtkinter as ctk
from tkinter import filedialog
import numpy as np
from PIL import Image, UnidentifiedImageError
import threading
import shutil

knownFaces = []
detectedNames = []
defaultNameCount = 1

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def askForName(faceImage):
    global defaultNameCount
    try:
        faceImageRgb = cv2.cvtColor(faceImage, cv2.COLOR_BGR2RGB)
        imgPil = Image.fromarray(faceImageRgb).resize((150, 150))
    except cv2.error:
        return None
    except UnidentifiedImageError:
        return None
    
    dialog = ctk.CTkToplevel()
    dialog.title("Enter Name")
    dialog.transient(dialog.master)
    dialog.grab_set()
    
    
    imgCtk = ctk.CTkImage(light_image=imgPil, size=(150, 150))
    label = ctk.CTkLabel(dialog, image=imgCtk, text="")
    label.image = imgCtk 
    label.pack(pady=10)
    
    userInput = ctk.StringVar()
    entry = ctk.CTkEntry(dialog, textvariable=userInput, width=200)
    entry.pack(pady=5)
    
    name = None
    submitted = threading.Event()

    def submit():
        nonlocal name
        name = userInput.get().strip()
        submitted.set()
        dialog.destroy()
        
    def auto_close():
        nonlocal name
        if not submitted.is_set():
            submitted.set()
            dialog.destroy()

    ctk.CTkButton(dialog, text="Submit", command=submit).pack(pady=10)
    
    dialog.bind('<Return>', lambda event: submit())
    
    dialog.after(20000, auto_close)
    
    dialog.wait_window(dialog)
    
    if not name:
        name = f"Person{defaultNameCount}"
        defaultNameCount += 1
    return name

def getFaces(imagePath):
    image = cv2.imread(imagePath)
    global detectedNames
    detectedNames = []
    if image is None:
        return detectedNames, None
    try:
        pilImage = Image.open(imagePath)
        if pilImage.mode not in ("RGB", "L"):
            return detectedNames, image
        if pilImage.mode == "RGB":
            rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceLocations = face_recognition.face_locations(rgbImage)
    except:
        return detectedNames, image
    
    
    for (top, right, bottom, left) in faceLocations:
        faceImage = image[top-20:bottom+20, left-20:right+20]
        if faceImage.size == 0:
            continue
        faceImageRgb = cv2.cvtColor(faceImage, cv2.COLOR_BGR2RGB)
        try:
            faceEncoding = face_recognition.face_encodings(faceImageRgb)
            if not faceEncoding:
                continue
            faceEncoding = faceEncoding[0]
        except (IndexError, TypeError) as e:
            print(f"Error encoding face: {e}")
            continue
            
        matched = False
        for knownEncoding, knownName in knownFaces:
            if face_recognition.compare_faces([knownEncoding], faceEncoding, tolerance=0.6)[0]:
                detectedNames.append(knownName)
                matched = True
                
        if not matched:
            name = askForName(faceImage)
            knownFaces.append((faceEncoding, name))
            detectedNames.append(name)
            
    return detectedNames, image

def getImg(imagePath, outputDir):
    names, image = getFaces(imagePath)
    if image is None:
        return
        
    for name in names:
        name = ''.join([c for c in name if c not in ('.', '/', '\\')])
        folder = os.path.join(outputDir, name)
        os.makedirs(folder, exist_ok=True)
        dest_path = os.path.join(folder, os.path.basename(imagePath))
        
        try:
            os.symlink(imagePath, dest_path)
        except (OSError, AttributeError):
            try:
                shutil.copy2(imagePath, dest_path)
            except Exception as e:
                print(f"Error copying file {imagePath}: {e}")

def openFolder(inputDir, outputDir):
    imageFiles = []
    for root, _, files in os.walk(inputDir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp")):
                imageFiles.append(os.path.join(root, file))
    
    if not imageFiles:
        return
        
    progress_window = ctk.CTkToplevel()
    progress_window.title("Processing Images")
    progress_window.geometry("400x150")
    
    label = ctk.CTkLabel(progress_window, text="Processing images...", font=("Arial", 14))
    label.pack(pady=10)
    
    progress = ctk.CTkProgressBar(progress_window, width=300)
    progress.set(0)
    progress.pack(pady=10)
    
    status_label = ctk.CTkLabel(progress_window, text="0/{}".format(len(imageFiles)), font=("Arial", 12))
    status_label.pack(pady=5)
    
    def process_images():
        for i, image in enumerate(imageFiles):
            getImg(image, outputDir)
            progress.set((i + 1) / len(imageFiles))
            status_label.configure(text=f"{i+1}/{len(imageFiles)}")
            progress_window.update()
            
        label.configure(text="Processing Completed!")
        progress_window.after(1000, progress_window.destroy)
        
    
    threading.Thread(target=process_images, daemon=True).start()
    progress_window.mainloop()
    
    
def main():
    def selectInputDir():
        folderPath = filedialog.askdirectory(title="Select Folder to Process")
        if folderPath:
            inputFolder.set(folderPath)
    
    def selectOutputDir():
        folderPath = filedialog.askdirectory(title="Select Output Folder")
        if folderPath:
            outputFolder.set(folderPath)
    
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Face Recognition and Categorization Tool")
    root.geometry("600x400")
    
    def startProcessing():
        inputDir = inputFolder.get()
        outputDir = outputFolder.get()
        if not inputDir or not outputDir:
            statusLabel.configure(text="Please select both input and output folders!", text_color="red")
            return
            
        statusLabel.configure(text="Processing started...", text_color="blue")
        
        processing_thread = threading.Thread(
            target=lambda: openFolder(inputDir, outputDir),
            daemon=True
        )
        processing_thread.start()
        
                  
    titleLabel = ctk.CTkLabel(root, text="Face Recognition\nAnd Categorization Tool", font=("Arial", 24, "bold"))
    titleLabel.pack(pady=20)
    
    inputFolder = ctk.StringVar()
    outputFolder = ctk.StringVar()

    ctk.CTkLabel(root, text="Select Input Folder:").pack()
    ctk.CTkEntry(root, textvariable=inputFolder, width=300).pack()
    ctk.CTkButton(root, text="Browse", command=selectInputDir).pack(pady=5)

    ctk.CTkLabel(root, text="Select Output Folder:").pack()
    ctk.CTkEntry(root, textvariable=outputFolder, width=300).pack()
    ctk.CTkButton(root, text="Browse", command=selectOutputDir).pack(pady=5)

    ctk.CTkButton(root, text="Start Processing", command=startProcessing, fg_color="blue").pack(pady=20)
    
    root.bind('<Return>', lambda event: startProcessing())
    
    statusLabel = ctk.CTkLabel(root, text="", font=("Arial", 12))
    statusLabel.pack(pady=5)
        
    
    root.mainloop()

if __name__ == "__main__":
    main()