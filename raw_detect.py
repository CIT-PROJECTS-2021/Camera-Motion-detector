
#?Importing opencv library for computer based vision
import cv2  

#? Capturing the video 
video = cv2.VideoCapture('vtest.avi') 

#? Splitting the video capture frames into frame1 and frame2 
#*to separately deal with each frame 
ret, frame1 = video.read()
ret, frame2 = video.read()
print(video.isOpened())
while video.isOpened():
    #? Getting absolute difference between the first frame and the second frame
    diff = cv2.absdiff(frame1, frame2)

    #? Converting the difference to grayscale mode
    #*It is easier to get the difference in grayscale mode than RGB
    #*Because grayscale contains only two channels
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    #? Applying blur to the grayscale 
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    #? Applying threshold to blur
    #*                        (src,thre-value,max-thre-value,type)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    #? Dilating the threshold image to fill
    #*Helps in making the image more 
    #*                   (src,corner-size,no of iterations)
    dilated = cv2.dilate(thresh, None, iterations=3)

    #? Finding the contours
    # *                            (src,     mode,          method)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #? Alternative code for the output without drawing the rectangles
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    
    #? For loop for drawing a rectangle
     
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        #* If the object's area is less than 00, do nothing
        #* If the area is greater than 700, draw the rectangle  
        #* Helps in ommitting motion detection on the ribbon
        if cv2.contourArea(contour) < 700:
            continue

        #? Drawing the rectangle on the moving object
        #           (src,    point1,   point2,     color,   thickness)  
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 100, 200), 2)
       
        #? Putting text on the video
        #*                                              (position,      font-face,        ,font-scale, color, thickness)
    cv2.putText(frame1, "Status:  {}".format('Motion'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,0), 2)
    
    #?Output windows
    cv2.imshow("CAM", frame1)
    #cv2.imshow('Gray', gray)
    #cv2.imshow('Gray', blur)
    #cv2.imshow('Gray', thresh)
    #cv2.imshow('Gray', dilated)
    

    #? Assigning frame2 into frame1
    frame1 = frame2

    #? Reading frame2 
    ret, frame2 = video.read()

    if cv2.waitKey(15) == ord('q'):
        break
    
cv2.destroyAllWindows()
video.release()

