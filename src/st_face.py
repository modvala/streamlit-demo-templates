import streamlit as st
import os
from pathlib import Path
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import time
import pathlib

st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
cwd =  pathlib.PureWindowsPath(__file__)

#------------------------------------------Ex1----------------------------------------------
#no_camera = cwd.parent.parent / "data" / "no_camera.png"
#swith = st.checkbox("Camera is active", value = True) #st.button("ON/OFF") 
#col1, col2 = st.columns(2)
#
#with col1:
#    if swith:
#        picture = st.camera_input("Take a picture", key="camera1")
#    else:
#        image = Image.open(str(no_camera))
#        st.image(image)
#
##------------------------------------------Ex1a---------------------------------------------
#
#face_cascade = cv2.CascadeClassifier(str(cwd.parent.parent / "data" / 'haarcascade_frontalface_default.xml'))
#with col2:
#    if picture is not None:
#        st.info("Detection of face")
#        # To read image file buffer with OpenCV:
#        bytes_data = picture.getvalue()
#        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
#        gray = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2GRAY)
#        # Detect the faces
#        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#        # Draw the rectangle around each face
#        for (x, y, w, h) in faces:
#            cv2.rectangle(cv2_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#        # Display
#        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
#        st.image(cv2_img)
#
#------------------------------------------Ex2----------------------------------------------
slide = st.sidebar
image_placeholder = st.empty()
#
face_cascade = cv2.CascadeClassifier(str(cwd.parent.parent / "data" / 'haarcascade_frontalface_default.xml'))
#
def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return img
#
def rotate_image(img, center = False, clockwise = False, counterclockwise = False):
    img = Image.fromarray(img)
    if clockwise:
        img = img.transpose(Image.ROTATE_90)
    if center:
        img = img.transpose(0)
    if counterclockwise:
        img = img.rotate(-90)
    img = np.array(img)
    return img

def brightness_contrast(img, contrast = 0, brightness = 1.0):

    img = Image.fromarray(img)
    im_out = ImageEnhance.Brightness(img).enhance(float(brightness))
    im_out = ImageEnhance.Contrast(im_out).enhance(float(contrast))
    im_out = np.array(im_out)
    return im_out

with slide:
    contrast = st.slider("Contrast", min_value=0.0, max_value=2.0, value=1.0, step=0.01)
    brightness = st.number_input("Brightness", min_value=0.0, max_value=2.0, value=0.5, step=0.01)
    clockwise = st.button("ROTATE +90")
    counterclockwise =st.button("ROTATE -90")
    center =st.button("CENTER")

def transform(frame):
    frame = brightness_contrast(frame, contrast=contrast, brightness=brightness)
    frame = rotate_image(frame, center, clockwise, counterclockwise)
    return frame

#
video = cv2.VideoCapture(0)
ok = True
while ok:
    ok, frame  = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # To read image file buffer as a PIL Image:
    frame = transform(frame)
    frame = detect_face(frame)
    with image_placeholder:
        st.image(frame)