from machine import Pin, PWM
import utime

rows = [Pin(i, Pin.OUT) for i in range(4)]
cols = [Pin(i, Pin.IN, Pin.PULL_DOWN) for i in range(4, 8)]
red_led = Pin(14, Pin.OUT)
green_led = Pin(15, Pin.OUT)

buzzer = PWM(Pin(13))
buzzer.freq(1000)

servo = PWM(Pin(16))
servo.freq(50)

password = ['1', '2', '3', '4']
entered_password = []

keys = [['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']]

def scan_keypad():
    for i, row in enumerate(rows):
        row.value(1)
        for j, col in enumerate(cols):
            if col.value() == 1:
                row.value(0)
                return keys[i][j]
        row.value(0)
    return None

def check_password():
    global entered_password
    if entered_password == password:
        success()
    else:
        alarm()

def success():
    green_led.value(1)
    buzzer.duty_u16(32768)
    utime.sleep(0.5)
    buzzer.duty_u16(0)

    set_servo_angle(servo, 180)
    utime.sleep(3)

    set_servo_angle(servo, 90)

    utime.sleep(1)
    green_led.value(0)


def alarm():
    red_led.value(1)
    for _ in range(5):
        buzzer.duty_u16(32768)
        utime.sleep(0.2)
        buzzer.duty_u16(0)
        utime.sleep(0.2)
    red_led.value(0)

def set_servo_angle(servo_pin, angle, fine_tune=0):
    duty = 500 + int((angle / 180) * 2000) + fine_tune
    servo_pin.duty_u16(int(duty * 65535 / 20000))

def button_press_sound():
    buzzer.duty_u16(32768)
    utime.sleep(0.1)
    buzzer.duty_u16(0)

set_servo_angle(servo, 90)

while True:
    key = scan_keypad()
    if key:
        print("Key Pressed:", key)
        button_press_sound()
        entered_password.append(key)
        utime.sleep(0.5)

        if len(entered_password) == 4:
            check_password()
            entered_password = []

