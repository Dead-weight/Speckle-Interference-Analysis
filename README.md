# Speckle-Interference-Analysis

 These programs provide a procedure for image analysis that allows for the precise melting curve determination for a laser-heating experiment. The analysis technique here is encapsulated into two separate python programs, SpeckleCapture.py and SpecklyProcess.py. The programs are stand-alone with the use of a Teledyne Instruments camera. In this method, a series of images is collected and analyzed pixel by pixel for the standard deviation, $\sigma_{ij}$, across the set of images. 

    $\sigma_{ij} = \sqrt{\frac{1}{N}\sum_{k=1}^N(x_{ijk}-<x_{ij}>)^2$

where $N$ is the number of the processed images, $k$ is the iterative element of $N$, $i$ and $j$ are the y and x pixel coordinates, respectively.

The average image is also matched with a reference image taken prior to measurement in a second calculation to determine how alike the images are to each other using the correlation coefficient, $\rho$,
\begin{equation}
    \rho = \frac{\sum_{ij}(y_{ij}-\Bar{y})(z_{ij}-\Bar{z})}{\sqrt{[\sum_{ij}(y_{ij}-\Bar{y})^2][\sum_{ij}{(z_{ij}-\Bar{z})^2}]}}
\end{equation}
where $\Bar{y}$ and $\Bar{z}$ are the average pixel values for the image and corresponding reference image. 

SpeckleCapture.py captures a user-defined series of images from a teledyne camera and saves them according to the power output with a time-stamp in the filename. An example output frame is located on figure 4.1(a) with a chosen region of interest around the speckle interference pattern from the $532\;nm$ light source.
