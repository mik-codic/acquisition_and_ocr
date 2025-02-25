# README

This repository shows how to use the TIS camera with the TIS.py library. The main script incorporates the usage of the Halcon library to run the DeepOcr for recognizing text in the image.

# Requirements
To run the main script the following libraries must be installed:
* halcon
  ```bash
$ pip install mvtec-halcon==24111
```
*

To run the script, simply run:
```bash
$ python main.py
```
the program will initialize the camera and prompt the user to insert an input for acquiring the images.
