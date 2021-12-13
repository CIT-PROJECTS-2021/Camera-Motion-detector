import tkinter as tk
import cv2
from tkinter import messagebox



window=tk.Tk()

window.title("Motion Detector")

canvas = tk.Canvas(window, width=200, height=300)
canvas.grid(columnspan=10, rowspan=10)

def run():
  video = cv2.VideoCapture(0) 

  ret, frame1 = video.read()
  ret, frame2 = video.read()
  
  while video.isOpened():
    
    diff = cv2.absdiff(frame1, frame2)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    
    dilated = cv2.dilate(thresh, None, iterations=3)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 700:
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 100, 200), 2)
    
        cv2.putText(frame1, "Status:  {}".format('Motion'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,1, (255,0,0), 2)
    
        cv2.imshow("CAM", frame1)

        frame1 = frame2
    
    ret, frame2 = video.read()

    if cv2.waitKey(15) == ord('q'):
        break
  
  if video.isOpened() is False:
      messagebox.showerror('Error', 'No video input detected')

  cv2.destroyAllWindows()
  video.release()  
  
instru1 = tk.Label(window, text='Welcome to the motion detection app', font=('Raleway',15))
instru2 = tk.Label(window, text='Press start app to detect motion', font=('Raleway',10))
instru1.grid(column=0, row=3)
instru2.grid(column=0, row=4)
run_text = tk.StringVar()
run_btn = tk.Button(window, textvariable=run_text, command=run, font='Raleway',bg='#20bebe', height=1, width=8 )
run_text.set("Start App")
run_btn.grid(column=0, row=5)

window.mainloop()
