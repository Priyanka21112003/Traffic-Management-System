# 🚦 Traffic-Management-System

It is a Python-based Traffic Monitoring System designed to detect vehicles and recognize Indian number plates from real-time video streams or images. Built using OpenCV and OCR tools, the system automates vehicle tracking and data logging for traffic management and surveillance use cases.

🇮🇳 Specially optimized for Indian number plates, with improved detection accuracy and localization.

🧩 System Flow (Modules)
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

🛠️ Features
📹 Real-time or image-based vehicle monitoring

🔍 Accurate number plate detection & recognition (optimized for Indian fonts)

🧾 CSV/data logging of detected vehicle numbers

🖼️ Saves cropped number plate snapshots for proof

💡 Simple, modular structure for easy upgrades

📦 Tech Stack
Python

OpenCV

EasyOCR / Tesseract OCR

NumPy, Pandas

CSV for data storage

🚀 How It Works
Feed in a live video or image.

Detect vehicles using OpenCV.

Crop the number plate area.

Extract plate number using OCR.

Save the results to a file or database for future reference.
