'''
SpeckleCapture.py captures and saves a series of 10 images from a FLIR or pointgrey camera.
This program requires the spinnaker SDK download from their website. 
Both the PC download as well as the python library are required for functionality. 
This program is utilizing the methodology of the examples from the python file download. 
** NOTE ** If there are more than 1 cameras on the system there will be additional files created 
and images collected for each camera
'''

import os
import PySpin
import sys
import matplotlib.pyplot as plt
from datetime import datetime


def acquire_speckle(cam, nodemap, nodemap_tldevice, num_images, power):
    """
    This function acquires and saves 'num_images' from the camera
    
    Parameters
    ----------
    cam : TYPE CameraPtr
        Camera device images acquired from
    nodemap : TYPE INodeMap
        Camera device nodemap
    nodemap_tldevice : TYPE INodeMap
        Transport layer camera device nodemap
    power : TYPE Double
        Passed paramter for filename
    Returns true if successful, false otherwise
    """
    
    print('**  Begin Speckle Image Acquision  **\n')
    
    try:
        # Set acquisition mode to continuous
        result = True
             
        # Node entries casted to a pointer type here.
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsReadable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
            return False
       
        # Retrieve entry node from enumeration node
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsReadable(node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
            return False 
        
        # Retrieve integer value from entry node
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()

        # Set integer value from entry node as new value of enumeration node
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        
        print('Speckle acquisition mode set to continuous')
        
        #Begin speckle image acquisition
        cam.BeginAcquisition()
        
        print('**   ACQUIRING IMAGES   **\n')
        
        # Retrieve device serial number for filename
        device_serial_number = ''
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print('Device serial number retrieved as %s...' % device_serial_number)
            
            print('Power reading retrieved as %d...' % power)
            
        # Create ImageProcessor instance for post processing images
        processor = PySpin.ImageProcessor()
        
        # Set default image processor color processing method
        processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)
        
        # Get current directory path for use later
        main_dir = os.getcwd()
        
        os.chdir('Images')
        
        # Make a new folder
        today = datetime.now()
        folder_name = '%d' % power + "mW " + today.strftime('%h %d %Y %H-%M-%S')
        os.mkdir(folder_name)
        
        print('\n Images Saved under folder name %s ...' % folder_name)
        
        
        
        # Change directory to new folder
        os.chdir(folder_name)
        
        # Loop for image retrieval
        for i in range(num_images):
            try:
                # Retrieve next image
                image_result = cam.GetNextImage(1000)
                
                # Ensure image collection
                if image_result.IsIncomplete():
                    print('Image failed with status %d' % image_result.GetImageStatus())
                
                else:
                                    
                    # Convert image to mono 8 pixel format
                    image_converted = processor.Convert(image_result, PySpin.PixelFormat_Mono8)
                    
                    # Create a unique filename
                    n = i+1
                    file_name = '%dmW Speckle #%d .jpg' % (power, n)
                    
                    
                    #  Save image
                    image_converted.Save(file_name)
                    #print('Image saved at %s' % file_name)

                    # Getting the image data as a numpy array
                    image_data = image_converted.GetNDArray()

                    # Draws an image on the current figure
                    plt.imshow(image_data, cmap='gray')

                    # Interval in plt.pause(interval) determines how fast the images are displayed in a GUI
                    # Interval is in seconds.
                    plt.pause(0.001)

                    # Clear current reference of a figure. This will improve display speed significantly
                    plt.clf()

                    #  Release image
                    image_result.Release()

                    
            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False
        
        # Return to main directory
        os.chdir(main_dir)
        
        # End Acquisition from the camera
        cam.EndAcquisition()
    
    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False
    
    return result


                        
def run_single_camera(cam, num_images, power):
    """
    This function acts as the body of the camera operation.

    Parameters
    ----------
    cam : TYPE CameraPtr
        Camera device images acquired from

    Returns true if successful, false otherwise
    """
    try:
        result = True

        # Retrieve TL device nodemap
        nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # Initialize camera
        cam.Init()

        # Retrieve GenICam nodemap
        nodemap = cam.GetNodeMap()

        # Acquire images
        result &= acquire_speckle(cam, nodemap, nodemap_tldevice, num_images, power)

        # Deinitialize camera
        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result



def main():

    # Ensure permission to write to this folder.
    try:
        test_file = open('test.txt', 'w+')
    except IOError:
        print('Unable to write to current directory. Please check permissions.')
        input('Press Enter to exit...')
        return False

    test_file.close()
    os.remove(test_file.name)
    
    result = True



    n_images = input("How many images would you like to capture?\n\n")
    num_images = int(n_images)
    pwr = input("\n\n What is the power reading?\n\n")
    power = float(pwr)
    
    
    # Retrieve singleton reference to system object
    system = PySpin.System.GetInstance()

    # Get current library version
    #version = system.GetLibraryVersion()
    #print('Library version: %d.%d.%d.%d' % (version.major, version.minor, version.type, version.build))

    # Retrieve list of cameras from the system
    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print('Number of cameras detected: %d' % num_cameras)

    # Finish if there are no cameras
    if num_cameras == 0:

        # Clear camera list before releasing system
        cam_list.Clear()

        # Release system instance
        system.ReleaseInstance()

        print('No cameras')
        input('Press Enter to exit...')
        return False

    # Run example on each camera
    for i, cam in enumerate(cam_list):

        print('Running camera %d...' % i)

        result &= run_single_camera(cam, num_images, power)
        print('Camera %d run complete... \n' % i)

    # Release reference to camera
    del cam

    # Clear camera list before releasing system
    cam_list.Clear()

    # Release system instance
    system.ReleaseInstance()

    #input('Press Enter to exit...')
    return result

if __name__ == '__main__':
    if main():
        sys.exit(0)
    else:
        sys.exit(1)
                    
                    
        
        
        