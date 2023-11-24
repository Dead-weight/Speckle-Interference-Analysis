'''
SpeckleProcess.py reads in a series of images from a folder to process them pixel-by-pixel.
Images are read and stored as matrices where each matrix location gets compared with the other image matrices.
The comparison is in the form of standard deviation and a new matrix is generated where each element is the 
standard deviation of that location among the images. The average standard deviation across the entirety 
of the final matrix is read out as a single value. 
'''

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image



def read_speckle_images(folder):
    
    
    images_array = []
    
    for filename in os.listdir(folder):
        
        image_path = os.path.join(folder, filename)
        img = Image.open(image_path)

        # Stores image into an array
        image_array = np.array(img)
        
        # Use following 2 lines only if a region of interest of the image is needed
        #array_ROI = image_array[465:915,850:1375]
        array_ROI = image_array[615:765,1075:1255]
        images_array.append(array_ROI)
        
        # Adds new array onto images array. Use following line, comment out ROI, and append images array.
        #images_array.append(image_array)
        
    return images_array
    
def main():
       
    folder_name1 = input("What is the name of the folder you would like to open?\n")
    ref_folder = 'Reference'
    # Get current directory path for use later
    main_dir = os.getcwd()
    
    # Change directory to the images folder
    os.chdir('Images')
       
    images1 = read_speckle_images(folder_name1)
    ref_image = read_speckle_images(ref_folder)
    
    print('\n *** Opening %s *** \n' % folder_name1)
    
    print('There are %d images in this folder\n' % len(images1))
        
    # Make an array of same size as sample images
    avg_array = np.zeros(np.shape(images1[0]))
    #print(avg_array)
    
    # Defines variables for image iteration based on image size. Changes with camera ROI or aspect ratio
    a,b = np.shape(images1[0])  
    print('\n Image ROI has the pixel dimension (%d, %d) \n'% (a , b))
    
    for i in range(len(images1)): 
       
        # Sums up the images into a single 2D array of pixel data
        avg_array = avg_array+images1[i]
        
        # Draws an image on the current figure
        plt.imshow(images1[i], cmap='copper')

        # Interval in plt.pause(interval) in seconds and determines how fast images are plotted
        plt.pause(0.001)
        
        # Clear current reference of the figure to improve display speed
        plt.clf()
    

    # Divides the sum of pixel data to form an array of average pixel value
    avg_array = 1/len(images1)*avg_array
    
    # Gets mean value of matrices for correlation calculation
    mean_img = np.mean(avg_array)
    mean_ref = np.mean(ref_image[0])
    
    # Variables initialized for calculating correlation coefficient
    SUM_ref_numerator=0
    SUM_ref_sqr = 0
    SUM_img_sqr =0
    
    
    #Creates an array to hold standard deviations of each pixel    
    std_array = np.zeros(np.shape(images1[0]))         
    
    # Iterates through the 'y-axis' pixel values in the image
    for i in range(a):
        
        # Iterates through the 'x-axis' pixel values in the image
        for j in range(b):
            
            # Here the vaiables for the correlation coefficient calculation are constructed using
            # the reference image and average image from the selection.
            ref_ij = float(ref_image[0][i,j] - mean_ref)
            img_ij = float(avg_array[i,j] - mean_img)
            SUM_ref_numerator = SUM_ref_numerator + (ref_ij * img_ij)
            SUM_ref_sqr = SUM_ref_sqr + (ref_ij * ref_ij)
            SUM_img_sqr = SUM_img_sqr + (img_ij * img_ij)
                
            # Variable initialized for the sum in the radiacal for standard deviation
            SUM = 0
            
            # Iterates through the number of images in the folder
            for k in range(len(images1)):
                
                # Stores a variable for difference of pixel value from the average
                C = float(images1[k][i,j]-avg_array[i,j])
                
                # Creates the value to sum up inside the radical in the standard deviation equation
                SUM = SUM + C*C
                
            std_array[i,j] = SUM
            #print(std_array[i,j])
            
            # Finalizes the operation to place in (i,j) pixel position the std array
            std_array[i,j] = np.sqrt(1/len(images1)*std_array[i,j])        
        
    
    # This variable is where the correlation coefficient is calculated. +1 in denominator allows
    # for non-zero denominator.
    rho = SUM_ref_numerator/(np.sqrt((SUM_ref_sqr)*SUM_img_sqr)+1)
    
    # Finds the average value of the standard deviation in all pixel locations
    mean_std = np.mean(std_array) 
    
    font1 = {'family':'serif','color':'blue','size':15}
    
    # Plots the image of standard deviations
    #ax = fig.add_subplot(311)
    plt.imshow(std_array, cmap = "nipy_spectral")
    plt.title('Standard Deviation of Speckle Images\n', fontdict = font1)
    
    
    print(type(std_array))
    print(np.shape(std_array))
    
    
    fig = plt.figure()
    aa, bb = np.mgrid[0:std_array.shape[0], 0:std_array.shape[1]]
    ax = fig.add_subplot(111, projection = "3d")
    ax.plot_surface( aa, bb, std_array, rstride=1, cstride=1, cmap = "nipy_spectral", linewidth = 0)
    plt.title('Standard Deviation of Speckle Images\n', fontdict = font1)

    #print(std_array)

    print('\n*** The average standard deviation is [%f] ***\n' % mean_std)
    print('*** The correlation coefficient with the reference image is [%f] ***\n' % rho)
    
    # Return to main speckle folder directory
    os.chdir(main_dir)
    
    return

if __name__ == '__main__':
    main()