# build_executable.ps1
# Script to build the standalone Windows application for Police Precincts

Write-Host "Ensuring PyInstaller is installed..."
pip install pyinstaller

Write-Host "Building Police Forensics AI Executable..."

# We use --onedir to create an unpacked folder. 
# This avoids the 30-second PyInstaller extraction delay every time the app is launched.
pyinstaller --name "CyberTerminal" `
            --onedir `
            --noconfirm `
            --clean `
            --add-data "assets;assets" `
            --add-data "weights;weights" `
            --add-data "third_party;third_party" `
            --add-data "src;src" `
            --hidden-import gradio `
            --hidden-import pandas `
            --hidden-import openpyxl `
            --hidden-import torch `
            --hidden-import torchvision `
            --hidden-import cv2 `
            --hidden-import basicsr `
            --hidden-import facexlib `
            --hidden-import gfpgan `
            --hidden-import google.genai `
            src/app.py

Write-Host "========================================================="
Write-Host "Build Complete!"
Write-Host "The application is located in: dist/CyberTerminal"
Write-Host "To deploy on another machine, copy the entire 'CyberTerminal' folder."
Write-Host "Do not forget to create a .env file next to CyberTerminal.exe with your GEMINI_API_KEY."
Write-Host "========================================================="
