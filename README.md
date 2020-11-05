# SpyCam

The SpyCam system is the result of a design course assignment at the University of Cape Town in 2020. This system provides a full demonstrator and API of a low-power, Embedded Systems implementation of mechanical pan and tilt camera arm with facial detection. This project inspired us to create a high-quality yet affordable security alternative to families living within the dangerous parts of South Africa.


## Requirements

In order to achieve the correct results, we suggest you use the following equipment:
* Raspberry Pi 3B+ or higher
* Pimoroni Pan-Tilt Board
* Pimoroni Dual Servo Mechanism
* Standard Power Adapter for Raspberry Pi (A USB power cable might not work)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install opencv.

```bash
pip install opencv-contrib-python
pip install pantilthat
pip install imutils
pip install "picamera[array]"
```
* Please note that in order to reliably use the SpyCam Demonstrator and API, it is suggested you work with Python 3 and was tested on Python 3.7 on the Raspberry Pi 3 B+

## Usage
The demonstrator currently consists of two different methods of operation:
1. Autonomous Haar-Cascade Model Facial Detection
2. Manual override of operation through a local webserver

If you are a beginner or would like to simply try the demonstrator of the system, use the following command line where the downloaded files have been extracted:

```python
python3 spycam.py
```
For more experienced users, you can use the direct command line interface:
```python
python3 pan_tilt_tracking.py --cascade haarcascade_frontalface_default.xml
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Other notes from the Dev Team
We hope this helps anyone inside or outside of South Africa! This design was inspired by Adrian Rosebrock at https://www.pyimagesearch.com/ , please give it a look and support him if possible.
