# Speckle-Interference-Analysis

 The analysis technique here is encapsulated into two separate python programs, SpeckleCapture.py and SpecklyProcess.py. The programs are stand-alone with the use of a Teledyne Instruments camera. In this method, a series of images is collected and analyzed pixel by pixel for the standard deviation across the set of images. The average image is also matched with a reference image taken prior to measurement in a second calculation to determine how alike the images are to each other using the correlation coefficient. These programs provide a procedure for image analysis that allows for the precise melting curve determination for a laser-heating experiment.

SpeckleCapture.py captures a user-defined series of images from a teledyne camera and saves them according to the power output with a time-stamp in the filename. The SpeckleProcess.py program prompts the user for the filename and creates a 3D array where the values at x and y coordinates are pixel intensities along a z coordinate for number of images. The program then calculates the average standard deviation per pixel across the images and an image can be produced from this resultant 2D array. An example of the 2D and 3D outputs for the standard images is located in the files for both before and during melt. 

Plotting the values of the average standard deviation and the correlation coefficient as a function of laser power can determine precise melt curves of the material. A discontinuous step for the average standard deviation in the positive direction as well as a step in the negative direction for the correlation coefficient values would indicate an increase in the variance of the speckle interference pattern, which coincides with the onset of liquid motion, or melt.

![LH Breadboard](https://github.com/Dead-weight/Speckle-Interference-Analysis/assets/151807915/ac08c606-b97b-435b-90c8-52fc2ee49090)
![LH Breadboard2](https://github.com/Dead-weight/Speckle-Interference-Analysis/assets/151807915/53725858-4ebc-4e67-ab84-e4cf2d75d453)


![Melt](https://github.com/Dead-weight/Speckle-Interference-Analysis/assets/151807915/577b34d8-b4e3-49a2-adf8-a8251d045400)
![NoMelt2D](https://github.com/Dead-weight/Speckle-Interference-Analysis/assets/151807915/9439e781-00c7-4f4e-8585-cec112bb3aaa)
![NoMelt3D](https://github.com/Dead-weight/Speckle-Interference-Analysis/assets/151807915/235bc602-8440-41a2-9bef-c8109f901387)
![Melt2D](https://github.com/Dead-weight/Speckle-Interference-Analysis/assets/151807915/38525b0c-1fa8-49ee-80ad-2a81c73f1dcb)
![Melt3D](https://github.com/Dead-weight/Speckle-Interference-Analysis/assets/151807915/e246ab11-5573-4215-8b78-c6c0c5f571d5)

