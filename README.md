# Trash Collector and Sorter Robot

This project is a robotic arm system that uses computer vision to automatically detect, pick up, and sort different types of recyclable materials. The system is powered by a Raspberry Pi for object detection and an Arduino for controlling the robotic arm.

## Table of Contents
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Demonstration](#demonstration)
- [Hardware](#hardware)
- [Software and Dependencies](#software-and-dependencies)
- [Setup](#setup)
- [Usage](#usage)

## Project Structure

-   **`3D Printing files/`**: Contains `.STL` files for the 3D printable parts of the robotic arm.
-   **`Arduino Code/`**: Includes the Arduino sketches for controlling the servo motors of the robotic arm. The main logic is likely in [`Arm/Arm.ino`](Arduino%20Code/Arm/Arm.ino) or [`final_code/final_code.ino`](Arduino%20Code/final_code/final_code.ino).
-   **`Raspberry pi Code/`**: Contains the Python scripts for the Raspberry Pi. This includes the main object detection logic ([`recycle_detection.py`](Raspberry%20pi%20Code/recycle_detection.py)), camera handling, and serial communication with the Arduino.
-   **`TensorflowLite/`**: Holds the trained TensorFlow Lite models ([`model.tflite`](TensorflowLite/model.tflite), [`quantized_and_pruned_model.tflite`](TensorflowLite/quantized_and_pruned_model.tflite)) used for object detection.
-   **`Trashnet Dataset/`**: Contains the image dataset, sorted into subdirectories by material type, used to train the machine learning model.
-   **`Video/`**: Contains the project demonstration video and GIF.
-   **`pr_project_report.docx`**: The project report document.

## How It Works

1.  **Detection**: The Raspberry Pi uses a camera to capture a live video stream. The [`recycle_detection.py`](Raspberry%20pi%20Code/recycle_detection.py) script processes the video frames.
2.  **Inference**: A TensorFlow Lite model running on the Pi analyzes each frame to detect and classify objects into categories like "paper", "plastic", and "metal".
3.  **Communication**: Once an object is identified, the Raspberry Pi calculates its coordinates and sends the material type and location data to the Arduino via a serial (USB) connection.
4.  **Actuation**: The Arduino receives the data and executes a sequence of movements. It controls the various servo motors of the robotic arm to pick up the object.
5.  **Sorting**: Based on the material type received from the Pi, the Arduino moves the arm to a predetermined location to drop the object into the correct sorting bin.
6.  **Feedback**: The Arduino sends a "Done Moving" signal back to the Raspberry Pi upon completing the task, making the system ready for the next object.

## Demonstration

![Project Demo](Video/output.gif)

A full video of the project in action can be found here: [Project Video](https://youtu.be/taYmQBE4060)

## Hardware

-   Raspberry Pi (with a PiCamera)
-   Google Coral Edge TPU (optional, for accelerating inference as seen in [`recycle_detection.py`](Raspberry%20pi%20Code/recycle_detection.py))
-   Arduino
-   Robotic Arm with multiple servo motors (base, shoulder, elbow, wrist, gripper)
-   USB Cable for Pi-Arduino communication

## Software and Dependencies

### Raspberry Pi

-   Python 3
-   OpenCV: `pip install opencv-python`
-   TensorFlow Lite Runtime: `pip install tflite-runtime`
-   pyserial: `pip install pyserial`
-   imutils: `pip install imutils`
-   picamera2: `pip install picamera2`
-   Edge TPU runtime (if using Coral): `pip install edgetpu`

### Arduino

-   Arduino IDE
-   `<Servo.h>` library

## Setup

1.  **Hardware**:
    -   Assemble the 3D printed robotic arm and connect the servos to the appropriate pins on the Arduino as defined in [`Arduino Code/Arm/Arm.ino`](Arduino%20Code/Arm/Arm.ino).
    -   Connect the PiCamera to the Raspberry Pi.
    -   Connect the Raspberry Pi to the Arduino via a USB cable.

2.  **Arduino**:
    -   Open the Arduino IDE.
    -   Upload the sketch from [`Arduino Code/Arm/Arm.ino`](Arduino%20Code/Arm/Arm.ino) or [`Arduino Code/final_code/final_code.ino`](Arduino%20Code/final_code/final_code.ino) to your Arduino board.
    -   Verify the correct serial port (e.g., `/dev/ttyACM0`) is used in the Python script.

3.  **Raspberry Pi**:
    -   Install all the required Python dependencies listed above.
    -   Ensure the TensorFlow Lite model and labels file are in the correct directory or provide the correct path when running the script.

## Usage

To run the main object detection and sorting program, execute the following command in the terminal on your Raspberry Pi:

```sh
python "Raspberry pi Code/recycle_detection.py" --model "TensorflowLite/quantized_and_pruned_model.tflite" --labels path/to/your/labels.txt
```

-   The `--model` argument should point to your TensorFlow Lite model file.
-   The `--labels` argument should point to a text file containing the class labels for your model.

A live video feed will be displayed on the screen, showing the detected objects and their bounding boxes. The system will then automatically control the arm to sort the detected items.