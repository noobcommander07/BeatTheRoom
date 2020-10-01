
import beat_the_room 
import RPi.GPIO as GPIO
import time

class TasterRaetsel(beat_the_room.Puzzle):

    #gpios initialisieren
    def __init__(self, controller):
        self.id = None
        
        GPIO.setmode(GPIO.BCM)

        
        self.id = 0 #platzhalter
        self.ports = [17,18,27,22]
        self.states = [False for i in range(4)]
        self.clickCounts = [0 for i in range(4)]
        self.currentPin = 0
        self.key = [3,5,3,1]

        
        pins = ""
        for i in range(4):
            pins += str(self.ports[i])+", "
        print("init(" + pins + ")")
        #reservier mal paar pins

    def interact(self):
        while not self.solved:
            pin = self.checkClicks()
            if pin != -1:
                if pin == self.currentPin:
                    self.click()
                elif pin == self.currentPin + 1:
                    self.currentPin += 1
                    self.click()
                elif pin == 0:
                    self.currentPin = 0
                    self.clickCounts = [0 for i in range(4)]
                    self.click()
            time.sleep(0.05)

    def deinit(self):
        pins = ""
        for i in range(4):
            pins += str(self.ports[i])+", "
        print("deinitialising(" + pins + ")")
        GPIO.cleanup()

    def click(self):
        self.clickCounts[self.currentPin] += 1
        self.solved = self.isSolved()

    def isSolved(self):
        return self.clickCounts == self.key

    def checkClicks(self):
        for i in range(4):
            print(GPIO.input(self.ports[i]))
            if GPIO.input(self.ports[i]):
                if not self.states[i]:
                    self.state[i] = True
                    return i
            else:
                self.states[i] = False
                
                
        return -1


#test code for testing purposes


test = True
if test:
    Puzzle2 = TasterRaetsel(None)
    Puzzle2.init()
    time.sleep(1)
    Puzzle2.interact()
    print("succsess")
    Puzzle2.deinit()