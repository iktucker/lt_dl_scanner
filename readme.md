# lt_dl_scanner

This is a small python application that I wrote to replace the old ScanShell feed-through scanner that our rental counter uses.

## Installation

Requires Python (developed on 3.9 from Windows Store)

    pip install -r requirements.txt

## Configuration

Edit the config.js file to suit your needs. It important to set the paths for the files and the focus for the camera. FYI, I'm using a Arducam USB at it works ok. My OnePlus device using Droidvcam OBS also worked. A 1080p is basically required since the PDF417 barcode is so dense.

The Arucam has auto-focus (disabled). If you can perfectly position your camera a device without focus is fine. Make sure your camera is recognized with the Camera app in Windows.

## Usage

python dl_scanner.py (or maybe extract the release zip and run the dl_scanner.exe file)

With the barcode in-frame, click the Capture Back button, the GUI will lag (no threading here) and the decoded info will go into the bottom pane. If you recieve an error try repositioning, relighting, or just re-clicking the button.

Flip over the license and capture the front of the card.

Click Save to Disk and await the success window.

In PoR click customer dashboard, then click the "New From License" button to create a new customer from the scanned license. This is the same as the old ScanShell method.