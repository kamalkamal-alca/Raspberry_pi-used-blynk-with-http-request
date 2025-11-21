import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
import requests
import time

GPIO.setmode(GPIO.BCM)
led1 = 14
led2 = 15
redLED = 12

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

GPIO.setup(redLED,GPIO.OUT)
pi_pwm = GPIO.PWM(redLED,1000)		#create PWM instance with frequency
pi_pwm.start(0)

# Blynk configuration
BLYNK_AUTH_TOKEN = 'mIoXKdO4PIqCvNDFGRQfegO7HFnGMt5c'
BASE_URL = "https://blynk.cloud/external/api/"
HEADERS = {'Content-Type': 'application/json'}

# Temperature sensor
sensor = W1ThermSensor()

def read_tempC():
    temperatureC = sensor.get_temperature()
    temperatureF = temperatureC * 9 / 5.0 + 32
    temperatureC = str(round(temperatureC, 1))
    temperatureF = str(round(temperatureF, 1))
    print("The temperature is %s C" % temperatureC)
    print("The temperature is %s F" % temperatureF)

    # Send temperature data to Blynk using HTTP POST
    url_c = f"{BASE_URL}update?token={BLYNK_AUTH_TOKEN}&v2={temperatureC}"
    url_f = f"{BASE_URL}update?token={BLYNK_AUTH_TOKEN}&v3={temperatureF}"
    requests.get(url_c)
    requests.get(url_f)

# Periodic task: Read temperature every 2 seconds
def periodic_task():
    while True:
        read_tempC()
        time.sleep(2)

# Handle virtual pin writes (V0, V1, V4)
def handle_virtual_pins():
    while True:
        # Read V0 value (LED1 control)
        v0_url = f"{BASE_URL}get?token={BLYNK_AUTH_TOKEN}&pin=V0"
        response_v0 = requests.get(v0_url)
        if response_v0.status_code == 200:
            value_v0 = response_v0.text.strip()
            if value_v0 == '1':
                GPIO.output(led1, GPIO.HIGH)
                print('LED1 HIGH')
            else:
                GPIO.output(led1, GPIO.LOW)
                print('LED1 LOW')

        # Read V1 value (LED2 control)
        v1_url = f"{BASE_URL}get?token={BLYNK_AUTH_TOKEN}&pin=V1"
        response_v1 = requests.get(v1_url)
        if response_v1.status_code == 200:
            value_v1 = response_v1.text.strip()
            if value_v1 == '1':
                GPIO.output(led2, GPIO.HIGH)
                print('LED2 HIGH')
            else:
                GPIO.output(led2, GPIO.LOW)
                print('LED2 LOW')

        # Read V4 value (PWM control)
        v4_url = f"{BASE_URL}get?token={BLYNK_AUTH_TOKEN}&pin=V4"
        response_v4 = requests.get(v4_url)
        if response_v4.status_code == 200:
            value_v4 = response_v4.text.strip()
            pi_pwm.ChangeDutyCycle(float(value_v4))
            print(f"PWM Duty Cycle: {value_v4}")

        time.sleep(1)

# Main loop
if __name__ == "__main__":
    try:
        # Start periodic temperature reading in a separate thread
        import threading
        threading.Thread(target=periodic_task, daemon=True).start()

        # Handle virtual pin writes in the main thread
        handle_virtual_pins()

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        PWM.stop(led)
        PWM.cleanup()
        GPIO.cleanup()
