This dataset consists of a collection of images and annotation of exit signs recorded at different distances.
the file camera_info.txt contains info about camera resolution and focal length 
Each subfolder contains images grouped by the distance at which they were recorded (1 = 1 meter, 2= 2 meters, and so on).
Within each folder, there are four subfolders that correspond to different locations in the building. Note that the naming of the locations is consistent across distances.
- 2
   + a
   + b
   + c
   - d
      + imgs (contains original images)
      + masks (binary masks, annotations)
      - VIO_2_d (log file containing info about camera pose when the images were shot)

TODO: describe VIO file
