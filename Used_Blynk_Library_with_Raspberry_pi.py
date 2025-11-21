import BlynkLib
import RPi.GPIO as GPIO
from BlynkTimer import BlynkTimer

from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

BLYNK_AUTH_TOKEN ='mIoXKdO4PIqCvNDFGRQfegO7HFnGMt5c'

GPIO.setmode(GPIO.BCM)
led1 = 14
led2 = 15
redLED = 12

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

GPIO.setup(redLED,GPIO.OUT)
pi_pwm = GPIO.PWM(redLED,1000)		#create PWM instance with frequency
pi_pwm.start(0)

timer = BlynkTimer()
x = 20

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
    
def read_tempC():
    sensor = W1ThermSensor()
    temperatureC = sensor.get_temperature()
    temperatureF = temperatureC * 9/5.0 + 32
    temperatureC = str(round(temperatureC, 1))
    temperatureF = str(round(temperatureF, 1))
    print("The temperature is %s C" % temperatureC)
    print("The temperature is %s F" % temperatureF)
    blynk.virtual_write(2, temperatureC,)
    blynk.virtual_write(3, temperatureF)

timer.set_interval(2, read_tempC) 
		 
@blynk.on("V0")
def v0_write_handler(value):
    if int(value[0]) ==1:
        GPIO.output(led1, GPIO.HIGH)
        print('LED1 HIGH')
    else:
        GPIO.output(led1, GPIO.LOW)
        print('LED1 LOW')

@blynk.on("V1")
def v1_write_handler(value):
    if int(value[0]) ==1:
        GPIO.output(led2, GPIO.HIGH)
        print('LED2 HIGH')
    else:
        GPIO.output(led2, GPIO.LOW)
        print('LED2 LOW')

@blynk.on("V4")
def v4_write_handler(value):
	#i=str(value[0])

	print(value)
	pi_pwm.ChangeDutyCycle(float(value[0]))	

while True:
    blynk.run()
    timer.run() 
