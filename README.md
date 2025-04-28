# 🚦 Traffic-Management-System

It is a Python-based Traffic Monitoring System designed to detect vehicles and recognize Indian number plates from real-time video streams or images. Built using OpenCV and OCR tools, the system automates vehicle tracking and data logging for traffic management and surveillance use cases.

🇮🇳 Specially optimized for Indian number plates, with improved detection accuracy and localization.

## 🧩 System Flow (Modules)
🎥 Input Module

Accepts video feed or image frames from CCTV/webcam.

🚗 Vehicle Detection Module

Detects and tracks vehicles using OpenCV's object detection.

🔍 Number Plate Detection Module

Locates and crops number plates from detected vehicles.

🧠 OCR & Text Extraction Module

Recognizes plate numbers using EasyOCR (or Tesseract) with preprocessing for better accuracy on Indian plates.

💾 Data Storage Module

Saves extracted number plate data with timestamps into a .csv file or database.

🖼️ Snapshot Capture Module (Optional)

Stores cropped images of detected plates as visual evidence.

## Screenshots of the Dashboard
Vehicle Count

![Vehicle Count](https://github.com/user-attachments/assets/2e9db6ba-b7fa-4dcb-957e-434337af995f)

Vehicle Speed

![Vehicle Speed](https://github.com/user-attachments/assets/0036250b-f6eb-4217-b5f4-a12e4bb102a0)

Vehicle Classification

![Vehicle Classification](https://github.com/user-attachments/assets/31f927d2-c5b5-4dbd-8fc7-0978713f49c8)

## 🛠️ Features
📹 Real-time or image-based vehicle monitoring

🔍 Accurate number plate detection & recognition (optimized for Indian fonts)

🧾 CSV/data logging of detected vehicle numbers

🖼️ Saves cropped number plate snapshots for proof

💡 Simple, modular structure for easy upgrades

## 📦 Tech Stack
Python

OpenCV

EasyOCR / Tesseract OCR

NumPy, Pandas

CSV for data storage

## 🚀 How It Works
Feed in a live video or image.

Detect vehicles using OpenCV.

Crop the number plate area.

Extract plate number using OCR.

Save the results to a file or database for future reference.
