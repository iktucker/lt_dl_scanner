# lt_dl_scanner

This is a small python application that I wrote to replace the old ScanShell feed-through scanner that our rental counter uses.

## Installation

Requires Python (developed on 3.9 from Windows Store)

    pip install -r requirements.txt

## Configuration

Edit the config.js file to suit your needs. It is important to set the paths for the output files and the focus for the camera. FYI, I'm using a Arducam USB and it works ok. My OnePlus device using Droidcam OBS also worked. A 1080p camera is basically required since the PDF417 barcode is so dense.

The Arucam has auto-focus (disabled, but allows for point-focus operation). If you can perfectly position your camera a device with a fixed focus is fine. Make sure your camera is recognized with the default Camera app in Windows.

## Usage

    python dl_scanner.py (or maybe extract the release zip and run the dl_scanner.exe file)

With the barcode in-frame, click the Capture Back button, the GUI will lag (no threading here) and the decoded info will go into the bottom pane. If you recieve an error try repositioning, relighting, or just re-clicking the button.

Flip over the license and capture the front of the card.

Click Save to Disk and await the success window.

In PoR click customer dashboard, then click the "New From License" button to create a new customer from the scanned license. This is the same as the old ScanShell method.

## Troubleshooting Tips

First: It's supposed to look stuttery. I found that refreshing the camera view at the same rate as the cameras FPS resulted in greater than 20% CPU utilization, whereas my hack to limit refresh to a couple times a second lowered the utilization to 10%.

If you find that some fields aren't scanning, check that the license_definition.json file is the same as the current WA state license definition. I used [this document](https://www.dol.wa.gov/driverslicense/docs/barcodeCalibration-EDLEID-2017.pdf) as a reference. Maybe there is a newer one (or a similar file for your state).

## Make a Camera Box

### Supplies

- [Arducam](https://www.amazon.com/dp/B08RHTG845/ref=twister_B09DKFZW1M?_encoding=UTF8&psc=1)
- [Acrylic box](https://www.amazon.com/gp/product/B01LZUJ1L4/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
- Hardware:
    - 4x small screws (I used 4-40 x 3/8)
    - 4x nuts (I used corresponding 4-40)
    - 4x small nylon washers or rubber o-rings
- A ~3.5" x 3.7" acrylic Sheet to glue into the box (Hartnagels had a small bit laying around that I cut down to size)
- Drill and some various drill bits

### Notes
The acrylic box allows plenty of light in, which (as noted) is the main constraint in getting a good scan. If you're placing the box in a dark location consider getting an led ring light or a desk lamp.

The linked box is 8" tall, placing the small acrylic square at 6" from the bottom allowed for a good platform for the Arducam to mount. I drilled a 1/2" hole into the center of the acrylic square (for the camera module to protrude through) and four tiny holes corresponding to the mounting locations for the Arducam. I also cut the box access panel in half(ish) to allow a space for the card to be inserted. Finally, I drilled a hole large enough for the Arducams USB cable to fit through (the small end) on the back of the box just above where I planned on mounting the camera. **Do all of this *before* assembly**

Super glue the sheet in place. Place your washers/o-rings on top of the mounting holes to isolate the camera. Place the Arducam on top of the washers, insert the screws through the mounting holes, then thread on the nuts on the underside of the acrylic square to finish mounting the Arducam.

Insert the USB cord through the back of the box and plug the PCB-end into the Arducam.

Place the access panel on, probably taping it in place, and consider putting some labels on the box to instruct customers on usage.


## Thanks
Thanks for [Lumber Traders Inc](https://angelesmillwork.com) for paying me to assemble the software and hardware for this thing.
Thanks to [Point of Rental](https://www.point-of-rental.com/) software for providing an updated OCR template file.