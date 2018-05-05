# Pi Camera application for HAL10K
# Written by Jeff Dunehew
# April 2018

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 90

# Take pic function
def snapshot(picfilename):
    camera.start_preview()
    sleep(5)
    camera.capture(picfilename)
    print("Took picture")
    camera.stop_preview()
    return;

# to loop and take a series of pictures:
# for i in range(5)
#     sleep(5)
#     camera.capture('/home/pi/Pictures/HAL10K/image.jpg')
# camera.stop_preview()

# To rotate camera:
# camera.rotation = 180

# To alter transparency of the camera preview by setting 
# an alpha level (note - alpha can be between 0 and 255):
# camera.start_preview(alpha=200)

# recording video:
# camera.start_preview()
# camera.start_recording('/home/pi/vide.h264')
# sleep(10)
# camera.stop_recording()
# camera.stop_preview()

# to play the video, open terminal window and type 
# 'omxplayer video.h264'








