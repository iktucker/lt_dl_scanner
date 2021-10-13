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

## Troubleshooting Tips

First: It's supposed to look stuttery. I found that refreshing the camera view at the same rate as the cameras FPS resulted in greater than 20% CPU utilization, whereas my hack to limit refresh to a couple times a second lowered the utilization to 10%.

If you find that some fields aren't scanning, check that the license_definition.json file is the same as the current WA state license definition. I used (https://www.dol.wa.gov/driverslicense/docs/barcodeCalibration-EDLEID-2017.pdf)[this document] as a reference. Maybe there is a newer one (or a similar file for your state).

## Make a Camera Box

### Supplies

- Arducam
- Acrylic box
- Mini led ring light

