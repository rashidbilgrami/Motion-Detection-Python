# import open CV Class
import cv2

# import Date and time
from datetime import date

# function readMouse Event
coordinates = [-100, -100]

# no need for it because x and y is further available in the section
# define event for identify coordiantes to draw rectangle on the video


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinates.clear()
        coordinates.append(x)
        coordinates.append(y)
        return coordinates

# read Video from file if youwant
# cap = cv2.VideoCapture("Megamind_bugy.avi")


# read video from cam, generally it's on zero if you did not find it you can find it on (-1)
cap = cv2.VideoCapture(0)

# set the video size of your video
cap.set(3, 1024)
cap.set(4, 600)

# http://www.fourcc.org/codecs.php
# Set video encoder
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# Set Frame width and height as like video size these functions or codes are available online at open cv portals
framewidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameheight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# save the file as output
out = cv2.VideoWriter("myFile.avi", fourcc,
                      10.0, (framewidth, frameheight))

# Check either the file or cam exisit or not
while (cap.isOpened()):
    # read Frame
    ret, frame = cap.read()

    # read another frame in next variable
    ret, frame1 = cap.read()

    # http://www.codebind.com/python/opencv-python-tutorial-beginners-read-write-show-videos-camera-opencv/ get the list of codes

    # if frame exisit
    if ret == True:

        # Set Font
        font = cv2.FONT_HERSHEY_SIMPLEX
        # Get Date
        text = date.today()

        # Set Date as text on video top position
        frame = cv2.putText(frame, str(text), (10, 50), font, 1,
                            (0, 255, 255), 2, cv2.LINE_AA)

        # Draw coordinates for the rectangle
        frame = cv2.putText(frame, str(coordinates[0]) + ' ,' + str(coordinates[1]), (coordinates[0], coordinates[1]), font, 1,
                            (0, 255, 255), 2, cv2.LINE_AA)

        # Draw ractangle once you click on the video the square will display
        frame = cv2.rectangle(frame, (coordinates[0], coordinates[1]), (
            coordinates[0]+150, coordinates[1]+150), (0, 255, 255), 1)

        # cv_object_management Properties just for checking
        '''
        print(frame.shape)  # Return The tuple of number row, columns  and channel
        print(frame.size)  # return total number of pixel size
        print(frame.dtype)  # retun data type
        b, r, g = cv2.split(frame)
        print(b)
        print(r)
        print(g)
        '''

        # Start motion detuction
        # find differnce in frame and frame 2
        diff = cv2.absdiff(frame, frame1)

        # convert different in gray scale it's easy to recoganize the difference
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Apply Blur the gray scale frame image
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply threshold on blur image
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        # Make the frame dilated
        dilated = cv2.dilate(thresh, None, iterations=3)

        # Find Contours and place in the variables
        contours, _ = cv2.findContours(
            dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Read Individual Contour
        for contour in contours:
            # Get Contour property to get x, y , w, h position
            (x, y, w, h) = cv2.boundingRect(contour)

            # draw countrours if you want to like to view enable it and play the script
            # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

            # Control motion detection size of green box here
            if cv2.contourArea(contour) < 9000:
                continue
            else:
                frame = cv2.rectangle(
                    frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                frame = cv2.putText(frame, "Motion Detected", (x, y), font, 1,
                                    (0, 255, 255), 2, cv2.LINE_AA)

        # display Image
        cv2.imshow("frame", frame)

        # left click button class mouse event
        cv2.setMouseCallback("frame", click_event)

        # save file if required and frame is there
        out.write(frame)

        # https://https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html get video capture property
        # print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # break the loop on press key q
        if cv2.waitKey(113) == ord('q'):
            break

# relase and distory objects.
cap.release()
out.release()
cv2.destroyAllWindows()
