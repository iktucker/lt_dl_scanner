# drivers license by Danil Polshin from the Noun Project

import cv2
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
from pdf417decoder import PDF417Decoder
import json
import tkinter as Tk
from tkinter import PhotoImage, ttk, messagebox
from time import sleep
from datetime import datetime as time

with open("license_definition.json") as f:
    map = json.load(f)["licenseMap"]

with open("config.json") as f:
    config = json.load(f)

global infoFrameCanvas
global cameraRefreshTime
global frame_rgb
global frontImgCap
global decodedData
exitFlag = False

cameraRefreshTime = time.utcnow()

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def captureImg(position, canvas):
    global frame_rgb
    global frontImgCap
    img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb).resize([240, 135]))
    canvas.img1 = img
    canvas.create_image(0,0,anchor='nw', image=img)

    # Set global frontImgCapture for front capture press
    if (position == 'front'):
        frontImgCap = frame_rgb

def decodeBarcode(frame):
    global map
    global infoFrameCanvas
    global decodedData
    decoder = PDF417Decoder(Image.fromarray(frame))
        
    if (decoder.decode() > 0):
        # Store the results
        decodedData = decoder.barcode_data_index_to_string(0).splitlines()

        # Delete and recreate the scroll area
        infoFrameCanvas.pack_forget()
        infoFrameCanvas = ScrollableFrame(infoFrame)
        infoFrameCanvas.pack(side = 'bottom')

        lines = decodedData

        for line in lines:
            if (line[0:3] in map):                
                ttk.Label(infoFrameCanvas.scrollable_frame, anchor = "w", text= (map[line[0:3]] + ": " + line[3:])).pack(fill = "both")
            continue
    else:
        # Delete and recreate the scroll area
        infoFrameCanvas.pack_forget()
        infoFrameCanvas = ScrollableFrame(infoFrame)
        infoFrameCanvas.pack(side = 'bottom')

        ttk.Label(infoFrameCanvas.scrollable_frame, anchor = "w", text= "Failed decoding barcode. Please recapture back.").pack(fill = "both")

        print('Nothing to decode or decode failed')

def captureAndDecode(position, canvas):
    global frame_rgb

    # Increase brightness and contrast to ease barcode reading
    enhancerContrast = ImageEnhance.Contrast(Image.fromarray(frame_rgb))
    contrasty = enhancerContrast.enhance(2)
    enhancerBrightness = ImageEnhance.Brightness(contrasty)
    frame_rgb = np.array(enhancerBrightness.enhance(2))

    captureImg(position, canvas)
    decodeBarcode(frame_rgb)

def saveToDisk():
    global decodedData
    global frontImgCap
    global map
    global config

    dataDict = {}
    for line in decodedData:
        if (line[0:3] in map):
            # Special case for formatting the ZIP code
            if (map[line[0:3]] == 'addressZIP'):
                dataDict[map[line[0:3]]] = (line[3:8] + '-' + line[8:])
                continue

            # Special case for formatting the sex as char
            if (map[line[0:3]] == 'sex'):
                if line[3:] == '0':
                    dataDict[map[line[0:3]]] = 'F'
                else:
                    dataDict[map[line[0:3]]] = 'M'
                continue

            # Special case for older licenses with combined first and middle
            if (map[line[0:3]] == 'firstMiddle'):
                dataDict['firstName'] = line[3:]
                dataDict['middleName'] = ''
                dataDict['weight'] = '0'
                continue

            dataDict[map[line[0:3]]] = line[3:]
        continue    

    path = config['path']
    imgPath = config['imgPath']
    dataPath = config['dataPath']

    print('Writing data to file')

    # Open the template file
    with open("DEFAULT_TEMPLATE.txt") as f:
        csvTemplate = f.read()

    if ((frontImgCap.any()) and (len(decodedData) > 0)):
        Image.fromarray(frontImgCap).resize(config['frontImgResolution']).save(imgPath, 'JPEG')
        with open(dataPath, "w") as text_file:
            text_file.write(csvTemplate.format(**dataDict))

    messagebox.showinfo("Files Saved", ("Files created at " + path))

def on_quit():
    global exitFlag
    exitFlag = True
    mainWindow.destroy()

mainWindow = Tk.Tk(className='dlScannerWindow')
mainWindow.title('LT Drivers License Scanner')
mainWindow.iconphoto(False, PhotoImage(file = 'icon.png'))

mainWindow.geometry("500x800")

# Setup exit handler
mainWindow.protocol("WM_DELETE_WINDOW", on_quit)

cameraFrame = Tk.Frame(mainWindow, width = 490, height = 330)
cameraFrame.pack(side = 'top')
cameraFrame.pack_propagate(0)

cameraDisplayArea = Tk.Frame(cameraFrame, width = 480, height = 270, bg = 'black')
cameraDisplayArea.pack(side = 'top', padx = 10, pady = 10)
cameraDisplayArea.pack_propagate(0)

cameraDisplayCanvas = Tk.Canvas(cameraDisplayArea, bg = 'black')
cameraDisplayCanvas.pack(expand='yes', fill='both')
cameraDisplayCanvas.pack_propagate(0)

cameraFrameCaptureButtonFront = Tk.Button(cameraFrame, text='Capture Front')
cameraFrameCaptureButtonFront.pack(side= 'left', padx = [125,0], pady = [0, 20])

cameraFrameCaptureButtonBack = Tk.Button(cameraFrame, text='Capture Back')
cameraFrameCaptureButtonBack.pack(side= 'right', padx = [0,125], pady = [0, 20])

capturedImagesFrame = Tk.Frame(mainWindow, width = 490, height = 150)
capturedImagesFrame.pack(side = 'top', padx=[5, 5])

frontImgFrame = Tk.Frame(capturedImagesFrame, width = 240, height = 135, bg = 'black')
frontImgFrame.pack(side = 'left', pady=[5, 5])
frontImgFrame.pack_propagate(0)

frontImgCanvas = Tk.Canvas(frontImgFrame, bg = 'black')
frontImgCanvas.pack(expand='yes', fill='both')
frontImgCanvas.pack_propagate(0)

frontImgFrameLabel = Tk.Label(frontImgCanvas, text="Front", fg = 'white', bg = 'black')
frontImgFrameLabel.pack(pady=5)

backImgFrame = Tk.Frame(capturedImagesFrame,  width = 240, height = 135, bg = 'black')
backImgFrame.pack(side = 'right', pady=[5, 5])
backImgFrame.pack_propagate(0)

backImgCanvas = Tk.Canvas(backImgFrame, bg = 'black')
backImgCanvas.pack(expand='yes', fill='both')
backImgCanvas.pack_propagate(0)

backImgFrameLabel = Tk.Label(backImgCanvas, text="Back", fg = 'white', bg = 'black')
backImgFrameLabel.pack(pady=5)

capturedImagesFrame.pack_propagate(0)

saveButtonFrame = Tk.Frame(mainWindow)
saveButtonFrame.pack(side = "bottom", expand = 'yes', fill = 'x')

saveButton = Tk.Button(saveButtonFrame, text = "Save to Disk", command = saveToDisk)
saveButton.pack(side = "right", padx = [0, 20], pady = 10)

infoFrame = Tk.Frame(mainWindow)
infoFrame.pack(side = "bottom", pady=[0, 20])

infoFrameLabel = Tk.Label(infoFrame, text="Barcode Info:")
infoFrameLabel.pack(side = 'top')

separator = ttk.Separator(infoFrame, orient='horizontal')
separator.pack(fill='x')

infoFrameCanvas = ScrollableFrame(infoFrame)
infoFrameCanvas.pack(side = 'bottom')

# Open the default webcam
camera = cv2.VideoCapture(0,cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, config['camera']['resolution']['width'])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config['camera']['resolution']['height'])
camera.set(cv2.CAP_PROP_AUTOFOCUS, config['camera']['autofocus'])
camera.set(cv2.CAP_PROP_FOCUS, config['camera']['focus'])
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, config['camera']['autoexposure'])
camera.set(cv2.CAP_PROP_EXPOSURE, config['camera']['exposure'])

while (mainWindow.wait_window):
    if (exitFlag): break

    ret, frame = camera.read()
    if not ret:
        print("failed to grab frame")
        break

    if ((time.utcnow() - cameraRefreshTime).microseconds >= 200000):
        camera.set(cv2.CAP_PROP_FOCUS, config['camera']['focus'])
        cameraRefreshTime = time.utcnow()
        frame_rgb = frame[:,:,::-1]
        img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb).resize([480, 270]))
        cameraDisplayCanvas.create_image(0,0,anchor='nw', image=img)

        cameraFrameCaptureButtonFront['command'] = lambda position = 'front', canvas = frontImgCanvas : captureImg(position, canvas)
        cameraFrameCaptureButtonBack['command'] = lambda position = 'back', canvas = backImgCanvas : captureAndDecode(position, canvas)

    mainWindow.update()

mainWindow.mainloop()
