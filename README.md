 # Table of Contents
1. [Introduction](README.md#introduction)
1. [Directory structure](README.md#directory-structure)
1. [Program structure](README.md#program-structure)
1. [Run the code](README.md#run-the-code)

# Introduction
This program calculates the distance from a camera to an exit sign in real-life, given the image containing the exit taken by the camera and coordinates of its four corners, together with the sign dimensions and the camera intrinsic parameters.

This program serves two purposes. First, this distance estimation model placed on top of a deep learning model, which assuming can accurately segment the four corners of the sign automatically, would be able to calculate the distance from the exit sign to the camera. Second, this distance estimation model works as a “labeler”: given a large dataset of exit sign images, with this model, we can obtain the exit sign distance from each image and feed it into a deep learning model that detects exit signs and predicts its distance from regression learning.

# Requirements
* Python 2.7
* numpy
* cv2
* json
* glob
* yaml

# Directory structure
```
├── README.md
├── data
│   ├── csv
│   │   ├── groundtruth-830.csv
│   │   ├── quadrilateral-1787.csv
│   │   ├── street-1008x756.csv
│   │   └── street-4032x3024.csv
│   ├── exit_sign_1787
│   ├── groundtruth_exit_sign
│   ├── groundtruth_exit_sign_cleaned_830
│   │   ├── camera_orientations
│   │   ├── imgs
│   │   └── masks
│   ├── json
│   │   ├── groundtruth-830.json
│   │   ├── groundtruth-results-830.json
│   │   ├── quadrilateral-raw-1807.json
│   │   ├── quadrilateral-results-1787.json
│   │   ├── street-raw-1008x756.json
│   │   ├── street-raw-4032x3024.json
│   │   ├── street-results-1008x756.json
│   │   └── street-results-4032x3024.json
│   ├── street_1008x756
│   └── street_4032x3024
├── pnp_distance_measurement
│   ├── calib
│   │   ├── calib.io_checker_200x150_7x8_18.pdf
│   │   ├── calib.py
│   │   ├── calib_imgs_1008x756
│   │   ├── calib_imgs_4032x3024
│   │   ├── calib_results_1008x756
│   │   ├── calib_results_4032x3024
│   │   ├── calibration_matrix_1008×756.yaml
│   │   └── calibration_matrix_4032x3024.yaml
│   ├── conf.py
│   ├── main.py
│   ├── pnp.py
│   └── resize
│       ├── resize.py
│       ├── resized
│       └── to_resize
├── preprocessing
│   ├── download_data.py
│   ├── json_to_csv.py
│   ├── masks_to_json.py
│   └── read_groundthruth.py
└── results
    └── arrow_imgs
        ├── exit_sign
        ├── groundtruth_exit_sign
        ├── street_1008x756
        └── street_4032x3024
```

# Program structure
## Main files
* `main.py`: run file, also contains some helper functions:
    * `create_quadrilateral_arr()`: read json input and extract the 4 labeled corner coordinates and the real distance (for the groundtruth dataset containing 830 exit sign images). Convert the extracted information of all the points to an array of quadrilateral objects, with attributes defined in `pnp.py`
    * `find_distance_error()`: (Applicable for the groundtruth dataset containing 830 exit sign images only) Calulate the average error of the calculated distance comparing with the real distance
    * `find_ave_proj_error()`: Calulate the average pixel differences in x and y directions between the labels and the projected images
    * `display_image()`: Display the image, the exit sign label boundaries and the normal Oxyz at the center of the exit sign
    * `write_to_json()`: Write the quadrilateral array to a json output file

* `pnp.py`: library containing:
    * `rearrange_pts()`: Rearrange 4 corner points to the correct order for matching
    * `rotate_vertical_quadrilateral()`: Rotate the quadrilateral 90 degrees in case it's vertical
    * `find_R_t()`: Find R vector and T vector from input 2D image points using PNP algorithm
    * `find_horizontal_distance()`: Calculate the horizontal distance, which is the dot product of T_vec and the unit normal vector of the sign (with respect to the camera reference system)
    * `project_2D()`: Project the 3D exit sign coodinates back to 2D given the computed Extrinsic vectors
    * `find_projection_err()`: Calculate the average error (in pixels) between the labeled vertices and the projected vertices of a quadrilateral

* `conf.py`: contains configurations for input and output paths, camera matrix, distortion coefficients. There are 4 different input options in `conf.py`:
    * `main_360x640`: Main exit sign dataset with 1787 images (details in Data)
    * `groundtruth_1920x1440_iPhone8`: The smaller exit sign dataset with 830 images (details in Data)
    * `street_4032x3024_iPhone8s`: 15 image dataset, used to verify the accuracy of the distance measurement implementation (details in Data)
    * `street_1008x756_iPhone8s`: the same dataset as the `street_4032x3024`, but images' size reduced to w/4 and h/4

  You can choose the input option + its parameters by uncommenting the line of code containing its name in the beginning of the file (line 3-6), and leaving the other 3 commented

## Data
* `exit_sign_1787`: main image dataset, provided by the Smith-Kettlewell Eye Research Institute. It contains 1787 images taken indoors, each contains at least one exit sign. The exit signs were intentionally taken at different distances with different poses and lighting conditions so that there are enough noises and variations. Each image has a height of 640 pixels and width 360 pixels, with a focal length provided as 536 pixels
* `groundtruth_exit_sign`: image dataset of 830 images along with the manually measured distance from the sign in the image to the camera. Each image in this dataset has a height of 1920 pixels and width of 1440 pixels, and a focal length provided as 1602 pixels
* `groundtruth_exit_sign_cleaned_830`: the same groundtruth image dataset, but cleaned (flattened, removing its hierachical structure) for easier file reading
* `street_4032x3024`: image dataset created by me, containing 15 images of a white board whose width is 32 inches (81.28 cm) and height is 19 inches (48.26 cm). This dataset was used to verify the accuracy of my distance measurement implementation
* `street_1008x756`: the same dataset as the `street_4032x3024`, but images' size reduced to w/4 and h/4 to speed up processing
* `json`: json data for the above datasets. Used by the program to get the 4 corner coordinates
* `csv`: csv data for the above datasets. These csv files were created for the sole purpose of making `.record` input files for the Tensorflow Object Detection Model in my subsequent project: Exit-Sign-Detector

## Other folders:
* `calib`: contains `calib.py` which takes checkerboard images taken at different angles as input and output the camera intrinsic matrix and distortion coefficients
* `resize`: contains script `resize.py` to resize all images in a directory
* `preprocessing` (not important as only required to run once to get the data to the right format): contains the following processing scripts:
    * `download_data.py`: for downloading the main 1787 image dataset as I did not have direct access to the images and had to use this script to download them from the google drive URLs given in the `quadrilateral-raw-1807.json`
    * `
* `results/arrow_imgs`: contains images with the exit sign label boundaries and the normal Oxyz at the center of the exit sign

# Run the code
Run `python main.py` in your Terminal

