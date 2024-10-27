import RPi.GPIO as GPIO
import time


class MotorController():
    running = True
    #MOTOR A pin map
    enA = 18
    in1 = 23
    in2 = 24
    #MOTOR B pin map
    in3 = 17
    in4 = 27
    enB = 22

    speedPinA = None
    speedPinB = None

    def __init__(self):
        #SETUP
        GPIO.setmode(GPIO.BCM) #Refrencing RasPi BCM GPIO pins
        #set all refrenced pins to output
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.enA,GPIO.OUT)
        GPIO.setup(self.in3,GPIO.OUT)
        GPIO.setup(self.in4,GPIO.OUT)
        GPIO.setup(self.enB,GPIO.OUT)
        self.speedPinA = GPIO.PWM(self.enA,1000) #initiate pulse-width-modulation pin motor A (this is the speed of motor A)
        self.speedPinA.start(0)
        self.speedPinB = GPIO.PWM(self.enB,1000) #initiate pulse-width-modulation pin motor A (this is the speed of motor A)
        self.speedPinB.start(0)
        #always forward
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)

    def forward(self):
        self.speedPinA.ChangeDutyCycle(35)
        self.speedPinB.ChangeDutyCycle(35)

    def right(self):
        self.speedPinA.ChangeDutyCycle(90)
        self.speedPinB.ChangeDutyCycle(30)

    def left(self):
        self.speedPinA.ChangeDutyCycle(30)
        self.speedPinB.ChangeDutyCycle(90)

    def stop(self):
        self.speedPinA.ChangeDutyCycle(0)
        self.speedPinB.ChangeDutyCycle(0)

    def areRunning(self): #loop constraint
        return self.running

    def exit(self): #shutdown motorcontroller
        GPIO.cleanup()
        self.running = False


if __name__ == '__main__': #test motors
    try:
        motors = MotorController()
        while motors.running():
            motors.right()
            time.sleep(2)
            motors.left()
            time.sleep(2)
            motors.forward()
            time.sleep(2)
    except:
        print ("there was an error. disable this line to debug")
        GPIO.cleanup()
