from appJar import *
import RPi.GPIO as GPIO 
from time import sleep

in1 = 24
in2 = 23
in3 = 17
in4 = 27
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)

def ButtonHandler(select): #calles when click the button
    if select == "Move forward":
         print("Move forward")
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)
         temp1=1
 
    if select == "Move backward":
         print("Move backward")
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
         temp1=0

    if select == "Turn left":
         print("Turn left")
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)

    if select == "Turn right":
         print("Turn right")
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)

    if select == "Stop":
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

    if select == "Exit:
        GPIO.cleanup()
         print("GPIO Clean up")
         break

program = gui("Manual controller", "300x300") #set size and title main GUI
program.setBg("white") #set backgroung colour
program.addLabel("label", "Manual controller") 

#Image
program.addImage("logo", "C:\\Users\\hp.DESKTOP-OU243N9\\Desktop\\UI\\logo.png") #image
program.zoomImage("logo",-2) #shrink image

#buttons
program.addButtons(["Move forward"],ButtonHandler)
program.addButtons(["Turn left","Stop","Turn right"],ButtonHandler)
program.addButtons(["Move backward"],ButtonHandler)
program.addButtons(["Exit"],ButtonHandler)

program.go()
