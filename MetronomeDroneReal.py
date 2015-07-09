
#TODO CHANGE BACKGROUND OF WINDOW TO SOMETHING AWESOME
#TODO CHANGE THE FONT AND SIZE OF THE TEMPO AND PITCH SO THEY STAND OUT 



#TODO make sure all labels initially are set to retrieve the starting value (no magic numbers)



#import libraries
from music import *
from gui import *
from random import *
from timer import *

###########################################################################################################################################
##This is a program based on the intermittent metronome and drone recording done by Jason Sulliman.  This idea is that a musician will   ##
##develop a better sense of time and pitch by using metronomes and drones (respectively) that are intermittent rather than continous     ##
##which is the typical way one would use the devices.  This program allows the user to select one or more pitches to be played as a      ##
##drone and the drone can be either continuous (e.g., like a traditional drone) or can be used in this "improved" manner.  To add to the ##
##usefullness of the random mode, if more than one pitch is selected, each pitch will be independently random, giving the user more      ##
##and varied random feedback.  In addition, the user can select, via a slider, the amount of space between playings.  Selecting more     ##
##space between playings reduces the feedback the user get and, thus, makes it more difficult.  For the metronome, The user can select   ##
##the amount of random space bewteen beats from no space at all to equal amounts of space and beats (the occurance of the space will be  ##
##random, but the amount of space will be roughly equal to the amount of noise).                                                         ##
###########################################################################################################################################



#define variables

delay = 5000 #Initial value for timer
randomSilence = randint(0, 5)#random interger to be added to s2 (slider)

#Create x and y position variables to accomodate a potential screen size change later
x=0 #Width
y=100 #Height
checkX =300+x #X for drone check boxes
checkY =75+y #Y for drone check boxes

#set slider ranges
#For drone
minVol = 0
maxVol = 80
startVol = 80

#For metronome
metVolStart = 127
MetStartTemp = 120

#Tempi for the metronome
minTempo = 40
maxTempo = 380

#variable for offsetting checkmark boxes
offSet = 18

#Create display window
d = Display("Interactive Metronome/Drone", 800, 600)

#Define functions
#start metronome
def startMet():
   for i in range(len(metBoxes)):
      if metBoxes[i].isChecked():  #Checks through all the boxes in the list metBoxes and, if checked, plays the sample on a continuous loop.
         metSamples[i].loop()

def stopMet():
   for i in metSamples:
      i.stop()            #Upon pressing the button to stop the metronome, all samples will be stopped.

def setTempoMet(tempo):
   for i in range(len(metSamples)):
      metSamples[i].setTempo(tempo)   #Sets the tempo to coincide with the slider (slider3).
   label2.setText("Tempo: " + str(tempo))  #Update the slider label accordingly.

def setVolumeMet(volume):  #Sets the volume of the metronome to coincide with the slider (slider4).
   global label4, metSamples, metCont, met82, met84, met86, met88
   for i in range(len(metSamples)):
      if metBoxes[i].isChecked():  #Added this conditional because this was the only way the program would allow the volume to change in a predictable way and with no err. Mess.
         metSamples[i].setVolume(volume)
   label4.setText("Volume: " + str(volume)+"        ")  #Update the label accordingly.
   
def playDrone():
   global listOfBoxes, listSamples
   for i in range(len(listOfBoxes)):
      random = randint(0, 5000)
      if listOfBoxes[i].isChecked():
         listSamples[i].play(0, random)
      elif not listOfBoxes[i].isChecked:
         listSamples[i].stop()
         
#function to be called at the change of state for the checkboxes.  
def checkOff(value):
   global listSamples, stopDrone, continueStart, startDrone
   if value and not stopDrone():
      continueStart()
   elif value and continueStart():
      continueStart()
   elif value and startDrone():
      startDrone()
   else:
      startDrone()

#Function to be called when a metronome checkbox changes state.  This is mainly a check to ensure that two boxes aren't checked at the same time.  In the future
   #it might be nice to have the second box remain checked and the first box to be unchecked if the user selects two boxes.  Currently, all boxes become unchecked
      #and all metronome noise ceases.
def checkOffMetCont(value):
   if metContBox.isChecked():
      startMet()
      if metEasy.isChecked() or metMedium.isChecked() or metHard.isChecked() or metVHard.isChecked():
         for i in range(len(metBoxes)):
            metBoxes[i].uncheck()
         stopMet() 
         metContBox.check()
         startMet()
   else:
      stopMet()
def checkOffMetEasy(value):
   if metEasy.isChecked():
      startMet()
      if metContBox.isChecked() or metMedium.isChecked() or metHard.isChecked() or metVHard.isChecked():
         for i in range(len(metBoxes)):
            metBoxes[i].uncheck()
         stopMet()
         metEasy.check()
         startMet()
   else:
      stopMet()
def checkOffMetMed(value):
   if metMedium.isChecked():
      startMet()
      if metEasy.isChecked() or metContBox.isChecked() or metHard.isChecked() or metVHard.isChecked():
         for i in range(len(metBoxes)):
            metBoxes[i].uncheck()
         stopMet()
         metMedium.check()
         startMet()
   else:
      stopMet()
def checkOffMetHard(value):
   if metHard.isChecked():
      startMet()
      if metEasy.isChecked() or metMedium.isChecked() or metContBox.isChecked() or metVHard.isChecked():
         for i in range(len(metBoxes)):
            metBoxes[i].uncheck()
         stopMet()
         metHard.check()
         startMet()
   else:
      stopMet()
def checkOffMetVHard(value):
   if metVHard.isChecked():
      startMet()
      if metEasy.isChecked() or metMedium.isChecked() or metHard.isChecked() or metContBox.isChecked():
         for i in range(len(metBoxes)):
            metBoxes[i].uncheck()
         stopMet()
         metVHard.check()
         startMet()
   else:
      stopMet()
   if not value:
      stopMet()

#Timer to be used in determining the playing of the drones under "random" mode.
t = Timer(delay, playDrone)  

def stopDrone():  #Upon the user pushing the button to stop the drone, all drone sounds cease.
   global t, listSamples
   for i in listSamples:
      i.stop()
   t.stop()
 
def setVolumeDrone(volume):  #Sets volume according to slider (slider2)
   global label3, listSamples
   for i in listSamples:
      i.setVolume(volume)
   label3.setText("Volume: " + str(volume)) #Update the label accordingly.
    
def continueStart():  #This is the function to be called if a continuous drone is required.
   global listOfBoxes, listSamples, stopDrone
   stopDrone()
   for i in range(len(listOfBoxes)):
      if listOfBoxes[i].isChecked():
         listSamples[i].play()
         
def startDrone():  #This is the function to be called if a random drone is required. After starting the pitches, the timer, t, is started.
   global t, listOfBoxes, listSamples, stopDrone
   stopDrone()
   for i in range(len(listOfBoxes)):
      if listOfBoxes[i].isChecked():
         listSamples[i].play(0, 4000)
   t.start() 
#called by s1(slider for changing space between playings).  Sets delay on timer, t.
def timerSet(value):  #Function to be called to control the timer used in startDrone.  Called in slider (slider1)
   global t
   t.setDelay(value)

def clearBox(): #Clears all boxes and stops all drone noises if the uncheck button is selected.
   global listOfBoxes, listSamples
   for i in range(len(listOfBoxes)):
      listOfBoxes[i].uncheck()
      stopDrone()
#Function to be called at the close of the window. This calls two other functions, stopMet() and stopDrone(), which will stop all sounds from playing.
def onClose():
   stopMet()
   stopDrone()

#Load image
metImage = Icon("Metronome Icon.png", d.getWidth(), d.getHeight())
#Load audio files 

#For drone sounds
c4 = AudioSample("C4.wav")
b3 = AudioSample("B3.wav")
bb3 = AudioSample("A#Bb3.wav")
a3 = AudioSample("A3.wav")
ab3 = AudioSample("Ab3.wav")
g3 = AudioSample("G3.wav")
fs3 = AudioSample("F#3.wav")
f3 = AudioSample("F3.wav")
e3 = AudioSample("E3.wav")
eb3 = AudioSample("Eb3.wav")
d3 = AudioSample("D3.wav")
db3 = AudioSample("Db3.wav")
c3 = AudioSample("C3.wav")

#for metronome sounds
metCont = MidiSequence("Metronome continuous.mid")
met82 = MidiSequence("Metronome 8:2.mid")
met84 = MidiSequence("Metronome 8:4.mid")
met86 = MidiSequence("Metronome 8:6.mid")
met88 = MidiSequence("Metronome 8:8.mid")


#create labels
label2 = Label("Tempo: " + str(MetStartTemp) +"       ") #Initialize the label for the metronome tempo
label3 = Label("Volume: " + str(startVol) +"         ") #Initialize the label for the drone volume
label4 = Label("Volume: " + str(metVolStart) +"       ") #Initialize the label for the metronome volume
label2.setFont(Font("SansSerif", Font.BOLD, 12))
label3.setFont(Font("SansSerif", Font.BOLD, 12))
label4.setFont(Font("SansSerif", Font.BOLD, 12))


#define the checkboxes.  Calls the function checkoff() returning a boolean (value).  If the box isn't checked, it returns a FALSE and the drone stops.  This is important
#because it immediatly stops the drone when someone unchecks a box in the middle of playback and stops the timer.  Without this, there is a delay after the unchecking of
#a box and the stopping of the note/timer cycle.    
c4Box = Checkbox("C4", checkOff)
b3Box = Checkbox("B3", checkOff)
bb3Box = Checkbox("Bb3", checkOff)
a3Box = Checkbox("A3", checkOff)
ab3Box = Checkbox("Ab3", checkOff)
g3Box = Checkbox("G3", checkOff)
fs3Box = Checkbox("F#3", checkOff)
f3Box = Checkbox("F3", checkOff)
e3Box = Checkbox("E3", checkOff)
eb3Box = Checkbox("Eb3", checkOff)
d3Box = Checkbox("D3", checkOff)
db3Box = Checkbox("Db3", checkOff)
c3Box = Checkbox("C3", checkOff)
metContBox = Checkbox("Continuous", checkOffMetCont)
metEasy = Checkbox("Easy", checkOffMetEasy)
metMedium = Checkbox("Medium", checkOffMetMed)
metHard = Checkbox("Hard", checkOffMetHard)
metVHard = Checkbox("Very Hard", checkOffMetVHard)


#Parallel lists from which to make functions for checkboxes and audio samples to be played.
listOfBoxes = [c4Box, b3Box, bb3Box, a3Box, ab3Box, g3Box, fs3Box,f3Box, e3Box, eb3Box,d3Box, db3Box, c3Box]
listSamples = [c4,    b3,    bb3,    a3,    ab3,    g3,    fs3,   f3,     e3,    eb3,  d3,    db3,    c3   ]

#As above, but for the metronome samples
metSamples = [metCont, met82, met84, met86, met88]
metBoxes = [metContBox, metEasy, metMedium, metHard, metVHard]

#random number to create random spacing (e.g. the delay in the timer).
random = randint(1,30)

     
droneStartBut = Button("Start Random", startDrone)                                                     
droneStopBut  = Button("Stop Drone", stopDrone)
droneContBut = Button("Start Drone", continueStart)
metStartBut = Button("Start Metronome", startMet)
metStopBut = Button("Stop Metronome", stopMet)
clearAllBut = Button("Clear Boxes", clearBox)



#Create sliders and assign callback functions
#slider(orientation, lower, upper, start, eventHandler
#slider for increasing space between playings
s1 = Slider(HORIZONTAL, delay, (delay*3)+random, delay , timerSet)
slider2 = Slider(HORIZONTAL, minVol, maxVol, maxVol, setVolumeDrone)
slider3 = Slider(HORIZONTAL, minTempo, maxTempo, 120, setTempoMet)
slider4 = Slider(HORIZONTAL, 0, 127, 127, setVolumeMet)




#Add buttons and sliders to window

#For the drone
d.add(droneStartBut, x+200, y+130)
d.add(s1, x+100, y+230)
d.add(slider2, x+100, y+275) #Drone volume
d.add(droneStopBut, x+85, y+160)
d.add(clearAllBut, x+200, y+160)
d.add(droneContBut, x+85, y+130)
d.add(label3, x+150, y+265)#Drone volume label
d.add(c4Box, checkX, checkY)
d.add(b3Box, checkX-40, checkY)
d.add(bb3Box, checkX-85, checkY)
d.add(a3Box, checkX-125, checkY)
d.add(ab3Box, checkX-170, checkY)
d.add(g3Box, checkX-210, checkY)
d.add(fs3Box, checkX-260, checkY)
d.add(f3Box, checkX-offSet, checkY-20)
d.add(e3Box, (checkX-40)-offSet, checkY-20)
d.add(eb3Box, (checkX-85)-offSet, checkY-20)
d.add(d3Box, (checkX-123)-offSet, checkY-20)
d.add(db3Box, (checkX-170)-offSet, checkY-20)
d.add(c3Box, (checkX-210)-offSet, checkY-20)


#For the metronome
d.addOrder(metStartBut,1,x+470, y+130)
d.add(label2, x+570, y+218) #met tempo label
#d.add(label6, x+600, y+200)
d.add(slider3, x+525, y+230) #met tempo slider
d.add(label4, x+570, y+265)#met volume label
d.add(slider4,  x+525, y +275)#Met Volume
d.add(metStopBut, x+620, y+130)
d.add(metContBox, x+555, checkY-20)
d.add(metEasy,x+655, checkY-20)
d.add(metMedium, x+520, checkY)
d.add(metHard, x+605, checkY)
d.add(metVHard, x+670, checkY)


#On close of window, all sounds and timers will stop.
d.onClose(onClose)

#Graphics
sepScreen = Line(430, 150, 430, 450, Color.BLACK, 1)
botScreen = Line(0, 450, 800, 450, Color.BLACK, 2)
botBorder = Icon("Music Border.jpg", 800, 200)
d.setColor(Color(255,255,254))
met1 = Icon("met1.jpg", 100, 100)
met2 = Icon("met2.jpg", 150, 100)
#tune1 = Icon("tune1.jpg", 200, 100)
#d.add(tune1, 100, 30)
d.add(met1, 575, 30)
d.add(met2, 125, 30)
d.add(sepScreen)

#Draw "tick marks" (lines) above the drone frequency slider.
xPos = 105
increment = 1
thickness = 1
for i in range(13):
   
   y1Pos = 320
   y2Pos = 330
   line = Line(xPos, y1Pos, xPos, y2Pos, Color.BLACK, thickness)
   d.add(line)
   increment +=2
   xPos = xPos + increment
   thickness += 1
moreSilence = Label("Silence Length:")
#moreSilence.setForegroundColor(Color.BLUE)
moreSilence.setFont(Font("SansSerif", Font.BOLD, 12))
d.add(moreSilence, 150, 300)
#d.add(sepScreen)
#d.add(botScreen)
d.addOrder(botBorder,5, 0, 400)

