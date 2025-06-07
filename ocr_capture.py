#!/usr/bin/env python3
import pytesseract
import pyttsx3
from PIL import Image
import os

# Captura pantalla usando imagemagick
os.system("import -window root /tmp/screen_capture.png")

# OCR
text = pytesseract.image_to_string(Image.open("/tmp/screen_capture.png"))
print("Texto detectado:", text)

# Voz
engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()
