# build_lite.ps1
# Script to build the standalone Windows application for Police Precincts (LITE / Offline Architecture)

Write-Host "Ensuring PyInstaller is installed inside venv..."
.\venv\Scripts\pip.exe install pyinstaller

Write-Host "Building Police Forensics AI Executable (LITE MODE)..."

# We use --onedir to create an unpacked folder. 
# This avoids the 30-second PyInstaller extraction delay every time the app is launched.
.\venv\Scripts\pyinstaller.exe --name "CyberTerminal_LITE" `
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
            --hidden-import kraken `
            --hidden-import requests `
            src/app.py

Write-Host "========================================================="
Write-Host "Build Complete!"
Write-Host "The application is located in: dist/CyberTerminal_LITE"
Write-Host "To deploy on another machine, copy the entire 'CyberTerminal_LITE' folder."
Write-Host "PRO UPGRADE: Drop a Llama 8B .gguf file into the weights/ folder to automatically unlock PRO mode!"
Write-Host "========================================================="
