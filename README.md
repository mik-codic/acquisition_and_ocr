# README

This repository shows how to use the TIS camera with the TIS.py library. The main script incorporates the usage of the Halcon library to run the DeepOcr for recognizing text in the image.

# Requirements
To run the main script the following libraries must be installed:
* halcon library is needed for the DeepOCR algorithm
```bash
$ pip install mvtec-halcon==24111
```
* gstreamer for python
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0
```
* Pymodbus library for sending and receiving messages
```bash
pip install  -U pymodbus
```
or Otherwise you can pull the trunk source and install from there:
```bash
git clone git://github.com/bashwork/pymodbus.git
cd pymodbus
python setup.py install
```
To properly run the script it's necessary the usage of an industrial camera and all the required drivers and library for usage, usually specified by the producer of the camera.


To run the script, simply run:
```bash
$ python main.py
```
the program will initialize the camera and prompt the user to insert an input for acquiring the images.
