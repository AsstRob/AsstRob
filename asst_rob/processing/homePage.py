from appJar import *

def ButtonHandler(select): #calles when click the button
    if select == "Manual control":
        print("Manual control")
    if select == "Auto control":
              print("Auto control")

program = gui("Welcome to AsstRob", "300x300") #set size and title main GUI
program.setBg("white") #set backgroung colour
program.addLabel("label", "AsstRob: An assitive robot for patient care") 

#Image
program.addImage("logo", "C:\\Users\\hp.DESKTOP-OU243N9\\Desktop\\UI\\logo.png") #image
program.zoomImage("logo",-2) #shrink image

#buttons
program.addButtons(["Manual control","Auto control"],ButtonHandler)

program.go()
