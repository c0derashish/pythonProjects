# Face Recognition and Categorization Tool

#### Video Demo: 

[https://drive.google.com/file/d/1deVWIXnbWmPOe1bz8lVE8AvxzABp8yjO/view?usp=sharing](https://drive.google.com/file/d/1deVWIXnbWmPOe1bz8lVE8AvxzABp8yjO/view?usp=sharing "video demo")

#### Description:

This project is an automated image processing tool that detects and categorizes faces from images using face recognition technology. It provides an interactive GUI for users to select image directories, process images, and categorize detected faces into different folders. This tool is particularly useful for photographers, security systems, and digital image organization.

##### Features:

- **Face Detection & Recognition:** The program detects faces in images and recognizes previously seen faces.
- **Automatic Categorization:** Recognized faces are grouped and stored in separate directories for easy access.
- **User Input for Unknown Faces:** When an unrecognized face is detected, the user is prompted to input a name to improve recognition accuracy in future scans.
- **Graphical User Interface (GUI):** Built using `customtkinter` for an interactive and user-friendly experience.
- **Batch Processing:** Users can select entire directories for batch face recognition and categorization, saving time and effort.
- **Robust Image Handling:** Works with multiple image formats, avoiding errors due to unsupported formats and ensuring broad usability.
- **Error Handling:** The program gracefully handles missing files, corrupt images, and permission errors, making it more reliable for real-world applications.

##### Project Files:

###### `project.py`

This file contains the core logic of the project, including:

- **`getFaces(imagePath)`**: Detects faces in an image, recognizes them if previously encountered, and prompts the user to assign names to unknown faces.
- **`getImg(imagePath, outputDir)`**: Saves detected faces into categorized folders for efficient organization and retrieval.
- **`openFolder(inputDir, outputDir)`**: Processes an entire folder of images, extracting and categorizing faces in bulk.
- **`main()`**: Launches the GUI, allowing users to select directories and initiate image processing with minimal effort.

###### `test_project.py`

This file contains unit tests using `pytest` to validate core functionalities:

- **`test_getFaces()`**: Ensures that the function detects and recognizes faces correctly.

- **`test_getImg()`**: Verifies that images are categorized into appropriate folders.

- **`test_askForName()`**: Checks if the function handles unknown faces correctly.

##### Design Choices:

1. **Face Recognition Library:** The `face_recognition` library was chosen due to its high accuracy and ease of use.
2. **Graphical Interface:** `customtkinter` enhances the user experience with a modern UI compared to standard Tkinter.
3. **Threading for Performance:** The image processing operations run in a separate thread to prevent the GUI from freezing.
4. **Automatic Naming:** If a user does not provide a name, a default `PersonX` format is used to maintain organization.
5. **Cross-Platform Compatibility:** Uses file handling techniques that work on Windows, macOS, and Linux for broader usability.
6. **Scalability:** Designed to handle large image directories efficiently, making it suitable for large datasets.

##### Future Improvements:

- Implementing deep learning-based face recognition for improved accuracy.
- Adding support for video face detection and tracking.
- Enhancing the database system for storing face metadata.
- Google Drive linking for wider application.
- Introducing multi-threaded processing for even faster performance.

This project is a powerful tool for sorting and managing images based on facial recognition and can be extended for applications like security surveillance, attendance tracking, and automated photo organization.
