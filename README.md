# Image Resizer

The script take one positional argument - path to image that need to be resized and resize the image with options, set in console with optional argumnets. The image name based on initial name + ```__widthxheight``` 

# Console arguments

```
-he -height height of final image
-w -width width of final image (if proportion of final image os not the same is will be written in console)
-s -scale scale of final image, can be less than 1
-o -output path to final image, if not set, the script save the image in the same folder
```

# Usage example

Python 3 and Pillow should be already installed. Example of script launch on Linux, Python 3.5:

```
$ python image_resize.py <path to image> -h 300 -s 4
-h and -w parameters are conflicted with -s
$ python image_resize.py <path to image>
There is not enough parameters
$ python image_resize.py <path to image> -h 300 -w 500
# if initial image proportions is not the same
The scale of final image is not the same
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
